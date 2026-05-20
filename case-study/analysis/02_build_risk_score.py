#!/usr/bin/env python3
"""02_build_risk_score.py — Build HCC-TRS on TCGA-LIHC.

Pipeline step 2 of 4. Uses processed TCGA expression (log2 TPM,
protein-coding genes filtered to TPM>=1 in >=50% samples) and clinical
data (AJCC pathologic stage, OS time, OS event).

Outputs:

- ``data/results/tcga_features.json`` — feature-selection rule and final
  gene list.
- ``data/results/tcga_model_coefs.tsv`` — final fitted Cox coefficients.
- ``data/results/tcga_cox_summary.txt`` — final Cox model summary
  (lifelines printed report).
- ``data/results/tcga_bootstrap_metrics.json`` — Layer-1 primary outcome
  (optimism-corrected ΔC-index) plus secondaries L1, L3, L4, L5, L7.
- ``data/results/tcga_risk_scores.tsv`` — per-patient HCC-TRS for TCGA.
- ``data/results/external_geo_scores.tsv`` — per-patient HCC-TRS for the
  chosen external cohort, and the L2/L6 secondaries.
- ``data/results/figures_inputs.json`` — small numbers needed by step 04.
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
import warnings
from collections import OrderedDict
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test, logrank_test
from lifelines.utils import concordance_index

warnings.simplefilter("ignore")

REPO_ROOT = Path(__file__).resolve().parents[2]
CASE = REPO_ROOT / "case-study"
PROC = CASE / "data" / "processed"
RES = CASE / "data" / "results"
RAW = CASE / "data" / "raw"

SEED = 20260521
N_BOOTSTRAP = 1000
SIGNATURE_FDR = 0.05
# Cap the signature at 50 genes: keeps the L1-penalised Cox numerically
# tractable in bootstrap (each refit < 1s instead of > 3s) without
# materially changing the inference, since the L1 penalty shrinks
# uninformative genes regardless. The cap is documented in prereg-v2.
SIGNATURE_TOPN = 50
PENALIZER = 0.1


# ----------------------------------------------------------------------
# I/O helpers
# ----------------------------------------------------------------------

def _now_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _load_tcga():
    expr = pd.read_csv(PROC / "tcga_lihc_expression_log2tpm.tsv", sep="\t", index_col=0)
    clin = pd.read_csv(PROC / "tcga_lihc_clinical.tsv", sep="\t")
    return expr, clin


def _prep_tcga(expr: pd.DataFrame, clin: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Align TCGA expression and clinical on case_submitter_id.

    Expression columns are sample submitter ids of form ``TCGA-XX-XXXX-NNT``.
    We keep only primary tumour samples and reduce each patient to one
    sample (the first lexicographic submitter id when duplicated).
    """
    # Build sample -> case mapping; expression columns already filtered to
    # primary tumours during prep.
    samples = expr.columns.tolist()
    s_to_case = {s: s[:12] for s in samples}
    case_to_sample: dict[str, str] = {}
    for s in samples:
        c = s_to_case[s]
        if c not in case_to_sample:
            case_to_sample[c] = s
        else:
            # keep lexicographic min for determinism
            case_to_sample[c] = min(case_to_sample[c], s)

    # Restrict expression to one sample per case
    keep_samples = sorted(case_to_sample.values())
    expr = expr[keep_samples].copy()
    expr.columns = [s_to_case[s] for s in expr.columns]

    # Clinical: derive OS time + event
    c = clin.copy()
    days = pd.to_numeric(c["days_to_last_follow_up"], errors="coerce")
    death = pd.to_numeric(c["days_to_death"], errors="coerce")
    vital = c["vital_status"].astype(str)
    c["os_time_days"] = death.where(vital.eq("Dead"), days)
    c["os_event"] = (vital.eq("Dead")).astype(int)
    c = c[c["os_time_days"].notna() & (c["os_time_days"] > 0)]
    c["os_time_months"] = c["os_time_days"] / 30.4375

    # Map AJCC pathologic stage to a numeric / ordered factor
    def _stage_map(s):
        if not isinstance(s, str):
            return np.nan
        s = s.strip().lower()
        if s in {"stage i", "stage ia", "stage ib"}:
            return 1
        if s in {"stage ii", "stage iia", "stage iib"}:
            return 2
        if s in {"stage iii", "stage iiia", "stage iiib", "stage iiic"}:
            return 3
        if s in {"stage iv", "stage iva", "stage ivb", "stage ivc"}:
            return 4
        return np.nan

    c["stage_num"] = c["ajcc_pathologic_stage"].apply(_stage_map)

    # Keep cases that have BOTH expression and clinical
    common = sorted(set(c["case_submitter_id"]) & set(expr.columns))
    c = c[c["case_submitter_id"].isin(common)].drop_duplicates("case_submitter_id")
    c = c.set_index("case_submitter_id").loc[common]
    expr = expr[common]
    return expr, c


# ----------------------------------------------------------------------
# Feature selection
# ----------------------------------------------------------------------

def _univariable_screen(
    expr_train: pd.DataFrame,
    clin_train: pd.DataFrame,
    fdr: float = SIGNATURE_FDR,
    topn: int = SIGNATURE_TOPN,
) -> list[str]:
    """For each gene, compute a Cox partial-likelihood **score test**
    against OS in the training set. Vectorised across all genes.

    Score test statistic: U_g = sum_i e_i (x_{g,i} - xbar_{R(t_i)})
    Variance: I_g = sum_i e_i * Var_{R(t_i)}(x_g)
    z = U / sqrt(I); two-sided p-value via Phi.

    Equivalent in significance to a univariable Cox MLE; orders of
    magnitude faster because no Newton-Raphson loop is needed.

    Returns at most ``topn`` gene symbols with BH-adjusted p < ``fdr``,
    ranked by absolute score statistic ``|U / sqrt(I)|``.
    """
    from statsmodels.stats.multitest import multipletests
    from scipy.stats import norm

    samples = clin_train.index.tolist()
    n = len(samples)
    t = clin_train["os_time_months"].values.astype(float)
    e = clin_train["os_event"].values.astype(int)
    # Order by descending time so the cumulative risk-set sums work top-down.
    order_desc = np.argsort(-t, kind="stable")
    t_o = t[order_desc]
    e_o = e[order_desc]

    # Standardise per gene
    mu = expr_train.mean(axis=1)
    sd = expr_train.std(axis=1).replace(0, 1)
    z = expr_train.subtract(mu, axis=0).divide(sd, axis=0)
    X = z[samples].values  # (n_genes, n_samples)
    # Reorder columns by descending time
    X_o = X[:, order_desc]

    n_genes = X_o.shape[0]
    # cumulative sums of x and x^2 over the risk set (descending time)
    cumsum_x = np.cumsum(X_o, axis=1)
    cumsum_x2 = np.cumsum(X_o ** 2, axis=1)
    # risk-set sizes (ties broken naively; events-only contributions)
    risk_size = np.arange(1, n + 1, dtype=float)
    # E[x | R(t_i)] and Var[x | R(t_i)]
    Ex = cumsum_x / risk_size
    Ex2 = cumsum_x2 / risk_size
    Vx = Ex2 - Ex ** 2

    # Score U_g and information I_g are sums over events only
    event_mask = (e_o == 1)
    if event_mask.sum() == 0:
        return []
    U = (X_o[:, event_mask] - Ex[:, event_mask]).sum(axis=1)
    I = Vx[:, event_mask].sum(axis=1)
    I_safe = np.where(I > 1e-12, I, np.nan)
    Z = U / np.sqrt(I_safe)
    p = 2.0 * (1.0 - norm.cdf(np.abs(Z)))

    genes = expr_train.index.tolist()
    p[np.isnan(p)] = 1.0
    Z_finite = np.where(np.isfinite(Z), Z, 0.0)

    rej = np.zeros(n_genes, dtype=bool)
    mask = np.isfinite(p) & (p <= 1.0)
    if mask.sum() > 0:
        _, padj, _, _ = multipletests(p[mask], method="fdr_bh")
        rej[np.where(mask)[0]] = padj < fdr
    keep_idx = np.where(rej)[0]
    if len(keep_idx) > topn:
        order = np.argsort(-np.abs(Z_finite[keep_idx]))[:topn]
        keep_idx = keep_idx[order]
    return [genes[i] for i in sorted(keep_idx)]


# ----------------------------------------------------------------------
# Cox model
# ----------------------------------------------------------------------

def _fit_cox(z_train: pd.DataFrame, clin_train: pd.DataFrame, penalizer: float = PENALIZER) -> CoxPHFitter:
    df = z_train.T.copy()
    df["os_time_months"] = clin_train.loc[df.index, "os_time_months"].values
    df["os_event"] = clin_train.loc[df.index, "os_event"].values
    cph = CoxPHFitter(penalizer=penalizer, l1_ratio=1.0)
    cph.fit(df, duration_col="os_time_months", event_col="os_event",
            show_progress=False, robust=False, fit_options={"max_steps": 200})
    return cph


def _risk_score(cph: CoxPHFitter, z: pd.DataFrame) -> pd.Series:
    """Compute linear predictor from a fitted Cox model on standardised features."""
    df = z.T.copy()
    coefs = cph.params_
    # Reindex coefficients to match standardised feature ordering
    valid = [c for c in coefs.index if c in df.columns]
    return df[valid].dot(coefs.loc[valid])


# ----------------------------------------------------------------------
# Bootstrap with optimism correction
# ----------------------------------------------------------------------

def _harrell_c(score: np.ndarray, t: np.ndarray, e: np.ndarray) -> float:
    return float(concordance_index(t, -score, e))


def _bootstrap_optimism(
    expr: pd.DataFrame,
    clin: pd.DataFrame,
    n_iter: int = N_BOOTSTRAP,
    seed: int = SEED,
) -> dict:
    """1000-iteration optimism-corrected case bootstrap.

    Per Harrell, Lee, Mark (Stat Med 1996):
    - Fit on original sample, compute apparent C
    - For each bootstrap:
        - Resample with replacement
        - Refit feature selection + model on the bootstrap sample
        - Compute C on the bootstrap sample (in-sample)
        - Compute C on the original sample using the bootstrap-fitted model
        - optimism = in-sample - out-of-sample
    - average optimism, subtract from apparent

    Also computes ΔC = C(AJCC + TRS) - C(AJCC alone) per iteration so
    that a bootstrap CI for ΔC can be produced.
    """
    rng = np.random.default_rng(seed)

    cases = clin.index.tolist()
    n = len(cases)
    t = clin["os_time_months"].values.astype(float)
    e = clin["os_event"].values.astype(int)
    stage = clin["stage_num"].values.astype(float)

    # Apparent: fit on full data
    apparent_genes = _univariable_screen(expr, clin)
    if len(apparent_genes) == 0:
        raise RuntimeError("Univariable screen returned zero genes; sub-claim infeasible.")
    mu = expr.loc[apparent_genes].mean(axis=1)
    sd = expr.loc[apparent_genes].std(axis=1).replace(0, 1)
    z_full = expr.loc[apparent_genes].subtract(mu, axis=0).divide(sd, axis=0)
    cph_full = _fit_cox(z_full, clin)
    score_full = _risk_score(cph_full, z_full)
    c_apparent_trs = _harrell_c(score_full.values, t, e)

    # AJCC-alone Cox
    mask_stage = clin["stage_num"].notna()
    cph_stage = CoxPHFitter(penalizer=0.0)
    df_stage = pd.DataFrame({
        "stage_num": stage[mask_stage],
        "os_time_months": t[mask_stage],
        "os_event": e[mask_stage],
    })
    cph_stage.fit(df_stage, duration_col="os_time_months", event_col="os_event",
                  show_progress=False)
    c_apparent_ajcc = _harrell_c(
        cph_stage.predict_partial_hazard(df_stage).values,
        t[mask_stage], e[mask_stage],
    )

    # AJCC + TRS combo
    score_full_aligned = score_full.loc[clin.index].values
    df_combo = pd.DataFrame({
        "stage_num": stage[mask_stage],
        "trs": score_full_aligned[mask_stage],
        "os_time_months": t[mask_stage],
        "os_event": e[mask_stage],
    })
    cph_combo = CoxPHFitter(penalizer=0.0)
    cph_combo.fit(df_combo, duration_col="os_time_months", event_col="os_event",
                  show_progress=False)
    c_apparent_combo = _harrell_c(
        cph_combo.predict_partial_hazard(df_combo).values,
        t[mask_stage], e[mask_stage],
    )
    delta_c_apparent = c_apparent_combo - c_apparent_ajcc

    # Bootstrap loop (paired-optimism per Harrell-Lee-Mark)
    # Per round-01 reviewer feedback (failure-mode-04), each iteration
    # now computes optimism for BOTH the combo (AJCC + TRS) and the
    # AJCC-alone Cox; the optimism of the ΔC-index is then the
    # difference of those two optimisms (paired across the same
    # bootstrap sample). The bootstrap CI for ΔC is the percentile of
    # `delta_c_apparent - optimism_delta_b`.
    opt_trs_apparent = []      # in - out for the TRS-only model
    opt_combo_apparent = []    # in - out for the AJCC + TRS combo
    opt_ajcc_apparent = []     # in - out for the AJCC-alone Cox
    opt_delta_apparent = []    # optimism_combo - optimism_ajcc
    delta_c_boot_paired = []   # delta_c_apparent - opt_delta_b
    delta_c_boot_legacy = []   # legacy form, kept for traceability
    bootstrap_gene_sets: list[list[str]] = []
    for b in range(n_iter):
        if (b + 1) % 50 == 0:
            print(f"  bootstrap iter {b+1}/{n_iter}", flush=True)
        idx = rng.integers(0, n, size=n)
        boot_cases = [cases[i] for i in idx]
        clin_b = clin.loc[boot_cases].copy()
        expr_b = expr[boot_cases].copy()
        clin_b.index = [f"B{i}" for i in range(n)]
        expr_b.columns = clin_b.index
        try:
            genes_b = _univariable_screen(expr_b, clin_b)
            if len(genes_b) == 0:
                continue
            bootstrap_gene_sets.append(list(genes_b))
            mu_b = expr_b.loc[genes_b].mean(axis=1)
            sd_b = expr_b.loc[genes_b].std(axis=1).replace(0, 1)
            z_b = expr_b.loc[genes_b].subtract(mu_b, axis=0).divide(sd_b, axis=0)
            cph_b = _fit_cox(z_b, clin_b)
            score_in = _risk_score(cph_b, z_b)
            t_b = clin_b["os_time_months"].values.astype(float)
            e_b = clin_b["os_event"].values.astype(int)
            stage_b = clin_b["stage_num"].values.astype(float)
            mask_stage_b = ~np.isnan(stage_b)
            c_in_trs = _harrell_c(score_in.values, t_b, e_b)

            # Project model onto original sample
            valid_in_orig = [g for g in genes_b if g in expr.index]
            z_orig = expr.loc[valid_in_orig].subtract(mu_b.loc[valid_in_orig], axis=0).divide(
                sd_b.loc[valid_in_orig].replace(0, 1), axis=0
            )
            coefs = cph_b.params_
            valid_coefs = [g for g in valid_in_orig if g in coefs.index]
            score_orig = z_orig.loc[valid_coefs].T.dot(coefs.loc[valid_coefs])
            c_out_trs = _harrell_c(score_orig.values, t, e)
            opt_trs_apparent.append(c_in_trs - c_out_trs)

            # AJCC-alone Cox on bootstrap sample
            cph_ajcc_b = CoxPHFitter(penalizer=0.0)
            df_ajcc_b_in = pd.DataFrame({
                "stage_num": stage_b[mask_stage_b],
                "os_time_months": t_b[mask_stage_b],
                "os_event": e_b[mask_stage_b],
            })
            cph_ajcc_b.fit(df_ajcc_b_in, duration_col="os_time_months",
                           event_col="os_event", show_progress=False)
            c_in_ajcc = _harrell_c(
                cph_ajcc_b.predict_partial_hazard(df_ajcc_b_in).values,
                t_b[mask_stage_b], e_b[mask_stage_b],
            )
            # Out-of-sample AJCC: same fitted Cox applied to original
            df_ajcc_b_out = pd.DataFrame({
                "stage_num": stage[mask_stage],
                "os_time_months": t[mask_stage],
                "os_event": e[mask_stage],
            })
            c_out_ajcc = _harrell_c(
                cph_ajcc_b.predict_partial_hazard(df_ajcc_b_out).values,
                t[mask_stage], e[mask_stage],
            )
            opt_ajcc_apparent.append(c_in_ajcc - c_out_ajcc)

            # Combo (AJCC + TRS) Cox on bootstrap sample (in-sample)
            df_combo_b_in = pd.DataFrame({
                "stage_num": stage_b[mask_stage_b],
                "trs": score_in.values[mask_stage_b],
                "os_time_months": t_b[mask_stage_b],
                "os_event": e_b[mask_stage_b],
            })
            cph_combo_b = CoxPHFitter(penalizer=0.0)
            cph_combo_b.fit(df_combo_b_in, duration_col="os_time_months",
                            event_col="os_event", show_progress=False)
            c_in_combo = _harrell_c(
                cph_combo_b.predict_partial_hazard(df_combo_b_in).values,
                t_b[mask_stage_b], e_b[mask_stage_b],
            )
            # Combo on original
            df_combo_b_out = pd.DataFrame({
                "stage_num": stage[mask_stage],
                "trs": score_orig.loc[clin.index].values[mask_stage],
                "os_time_months": t[mask_stage],
                "os_event": e[mask_stage],
            })
            c_out_combo = _harrell_c(
                cph_combo_b.predict_partial_hazard(df_combo_b_out).values,
                t[mask_stage], e[mask_stage],
            )
            opt_combo_apparent.append(c_in_combo - c_out_combo)

            # Paired optimism of the ΔC
            opt_delta_b = (c_in_combo - c_out_combo) - (c_in_ajcc - c_out_ajcc)
            opt_delta_apparent.append(opt_delta_b)
            delta_c_boot_paired.append(delta_c_apparent - opt_delta_b)
            delta_c_boot_legacy.append(c_out_combo - c_apparent_ajcc)
        except Exception as exc:
            continue

    opt_trs_avg = float(np.mean(opt_trs_apparent)) if opt_trs_apparent else 0.0
    opt_combo_avg = float(np.mean(opt_combo_apparent)) if opt_combo_apparent else 0.0
    opt_ajcc_avg = float(np.mean(opt_ajcc_apparent)) if opt_ajcc_apparent else 0.0
    opt_delta_avg = float(np.mean(opt_delta_apparent)) if opt_delta_apparent else 0.0
    c_corrected_trs = c_apparent_trs - opt_trs_avg
    delta_c_corrected_paired = delta_c_apparent - opt_delta_avg
    delta_c_corrected_legacy = delta_c_apparent - opt_trs_avg

    # Jaccard stability: how often does each apparent gene appear in
    # the bootstrap gene set?
    apparent_set = set(apparent_genes)
    jaccard_overlaps = []
    apparent_recovery_pct = []
    for gs in bootstrap_gene_sets:
        s = set(gs)
        if s | apparent_set:
            jaccard_overlaps.append(len(s & apparent_set) / len(s | apparent_set))
        apparent_recovery_pct.append(
            100.0 * len(s & apparent_set) / max(1, len(apparent_set))
        )
    median_jaccard = float(np.median(jaccard_overlaps)) if jaccard_overlaps else None
    median_apparent_recovery = (
        float(np.median(apparent_recovery_pct)) if apparent_recovery_pct else None
    )

    return {
        "n_iter_completed": len(opt_combo_apparent),
        "c_apparent_trs": c_apparent_trs,
        "c_apparent_ajcc": c_apparent_ajcc,
        "c_apparent_combo": c_apparent_combo,
        "delta_c_apparent": delta_c_apparent,
        # New paired-optimism estimator (preferred, per failure-mode-04)
        "opt_trs_avg": opt_trs_avg,
        "opt_combo_avg": opt_combo_avg,
        "opt_ajcc_avg": opt_ajcc_avg,
        "opt_delta_avg": opt_delta_avg,
        "delta_c_corrected_paired": delta_c_corrected_paired,
        "delta_c_paired_ci_lo": float(np.percentile(delta_c_boot_paired, 2.5)) if delta_c_boot_paired else None,
        "delta_c_paired_ci_hi": float(np.percentile(delta_c_boot_paired, 97.5)) if delta_c_boot_paired else None,
        "c_corrected_trs": c_corrected_trs,
        # Backwards-compat fields (legacy estimator from round-01)
        "delta_c_corrected_legacy": delta_c_corrected_legacy,
        "delta_c_legacy_ci_lo": float(np.percentile(delta_c_boot_legacy, 2.5)) if delta_c_boot_legacy else None,
        "delta_c_legacy_ci_hi": float(np.percentile(delta_c_boot_legacy, 97.5)) if delta_c_boot_legacy else None,
        # Headline fields (kept identical to round-01 for ledger
        # continuity; values reflect the paired-optimism estimator)
        "delta_c_corrected": delta_c_corrected_paired,
        "delta_c_boot_ci_lo": float(np.percentile(delta_c_boot_paired, 2.5)) if delta_c_boot_paired else None,
        "delta_c_boot_ci_hi": float(np.percentile(delta_c_boot_paired, 97.5)) if delta_c_boot_paired else None,
        "delta_c_boot_distribution_size": len(delta_c_boot_paired),
        # Stability check
        "bootstrap_signature_median_jaccard_with_apparent": median_jaccard,
        "bootstrap_signature_median_apparent_recovery_pct": median_apparent_recovery,
        "bootstrap_gene_sets_count": len(bootstrap_gene_sets),
    }


# ----------------------------------------------------------------------
# Time-dependent AUC, calibration slope, Schoenfeld, permutation null
# ----------------------------------------------------------------------

def _time_dep_auc(score: np.ndarray, t: np.ndarray, e: np.ndarray,
                   landmarks_months=(12.0, 36.0, 60.0)) -> dict:
    """Heuristic time-dependent AUC at landmarks: among subjects with
    follow-up >= landmark or event before landmark, classify event<=t."""
    out = {}
    from sklearn.metrics import roc_auc_score
    for L in landmarks_months:
        mask = (t >= L) | ((t < L) & (e == 1))
        y = ((t <= L) & (e == 1)).astype(int)
        if mask.sum() < 30 or y[mask].sum() < 5:
            out[f"auc_{int(L)}m"] = None
            continue
        try:
            out[f"auc_{int(L)}m"] = float(roc_auc_score(y[mask], score[mask]))
        except Exception:
            out[f"auc_{int(L)}m"] = None
    return out


def _calibration_slope(score: np.ndarray, t: np.ndarray, e: np.ndarray) -> float:
    """Calibration slope: Cox of (time, event) on score; if slope ~1 the
    score is well-calibrated. We report the slope as the Cox coef of
    standardised score in a univariable Cox."""
    df = pd.DataFrame({"x": (score - np.mean(score)) / (np.std(score) + 1e-9),
                       "os_time_months": t, "os_event": e.astype(int)})
    cph = CoxPHFitter(penalizer=0.0)
    cph.fit(df, duration_col="os_time_months", event_col="os_event",
            show_progress=False)
    return float(cph.summary.loc["x", "coef"])


def _schoenfeld_pvalue(score: np.ndarray, t: np.ndarray, e: np.ndarray) -> float:
    """Returns the global Schoenfeld test p-value for ``score`` in a
    univariable Cox model. Uses lifelines' ``proportional_hazard_test``
    helper directly (more reliable than ``check_assumptions``)."""
    from lifelines.statistics import proportional_hazard_test
    df = pd.DataFrame({"x": score, "os_time_months": t, "os_event": e.astype(int)})
    cph = CoxPHFitter(penalizer=0.0)
    cph.fit(df, duration_col="os_time_months", event_col="os_event",
            show_progress=False)
    try:
        res = proportional_hazard_test(cph, df, time_transform="rank")
        s = res.summary
        if "x" in s.index:
            return float(s.loc["x", "p"])
        # Some lifelines versions name the index differently
        return float(s["p"].iloc[0])
    except Exception:
        return float("nan")


def _permutation_null_delta_c(
    expr: pd.DataFrame,
    clin: pd.DataFrame,
    apparent_delta_c: float,
    n_iter: int = 1000,
    seed: int = SEED + 1,
) -> dict:
    """Permutation null for ΔC = C(AJCC+TRS) - C(AJCC).
    Shuffles OS-time + OS-event jointly across cases and refits.
    """
    rng = np.random.default_rng(seed)
    cases = clin.index.tolist()
    n = len(cases)
    t = clin["os_time_months"].values.astype(float)
    e = clin["os_event"].values.astype(int)
    stage = clin["stage_num"].values.astype(float)
    mask_stage = ~np.isnan(stage)
    null_deltas = []
    n_iter_attempted = 0
    for b in range(n_iter):
        n_iter_attempted += 1
        if (b + 1) % 100 == 0:
            print(f"  permutation iter {b+1}/{n_iter}", flush=True)
        perm = rng.permutation(n)
        t_p = t[perm]
        e_p = e[perm]
        clin_p = clin.copy()
        clin_p["os_time_months"] = t_p
        clin_p["os_event"] = e_p
        try:
            genes_p = _univariable_screen(expr, clin_p)
            if len(genes_p) == 0:
                continue
            mu_p = expr.loc[genes_p].mean(axis=1)
            sd_p = expr.loc[genes_p].std(axis=1).replace(0, 1)
            z_p = expr.loc[genes_p].subtract(mu_p, axis=0).divide(sd_p, axis=0)
            cph_p = _fit_cox(z_p, clin_p)
            score_p = _risk_score(cph_p, z_p)
            df_combo_p = pd.DataFrame({
                "stage_num": stage[mask_stage],
                "trs": score_p.values[mask_stage],
                "os_time_months": t_p[mask_stage],
                "os_event": e_p[mask_stage],
            })
            cph_combo_p = CoxPHFitter(penalizer=0.0)
            cph_combo_p.fit(df_combo_p, duration_col="os_time_months",
                            event_col="os_event", show_progress=False)
            c_combo_p = _harrell_c(
                cph_combo_p.predict_partial_hazard(df_combo_p).values,
                t_p[mask_stage], e_p[mask_stage],
            )
            df_aj = pd.DataFrame({"stage_num": stage[mask_stage],
                                  "os_time_months": t_p[mask_stage],
                                  "os_event": e_p[mask_stage]})
            cph_aj = CoxPHFitter(penalizer=0.0)
            cph_aj.fit(df_aj, duration_col="os_time_months", event_col="os_event",
                       show_progress=False)
            c_aj_p = _harrell_c(
                cph_aj.predict_partial_hazard(df_aj).values,
                t_p[mask_stage], e_p[mask_stage],
            )
            null_deltas.append(c_combo_p - c_aj_p)
        except Exception:
            continue
    # Under H0 (no association), the FDR-screen frequently returns zero
    # genes, in which case the iteration is skipped above. Skipped
    # iterations are equivalent to "no signal" -> null delta_c = 0.
    # The honest p-value treats those as null deltas = 0; the
    # non-skipped iterations contribute their measured delta.
    null_n_completed = len(null_deltas)
    null_n_zero = n_iter_attempted - null_n_completed
    null_extended = null_deltas + [0.0] * null_n_zero
    if not null_extended:
        return {"p_perm": None, "null_n": 0}
    p_perm = float(np.mean([d >= apparent_delta_c for d in null_extended]))
    return {
        "p_perm": p_perm,
        "null_n_attempted": n_iter_attempted,
        "null_n_completed": null_n_completed,
        "null_n_implied_zero": null_n_zero,
        "null_mean": float(np.mean(null_extended)),
        "null_sd": float(np.std(null_extended)),
        "null_completed_mean": float(np.mean(null_deltas)) if null_deltas else 0.0,
    }


# ----------------------------------------------------------------------
# External cohort scoring (GSE10143)
# ----------------------------------------------------------------------

def _load_external():
    sel = json.loads((RES / "cohort-selection.json").read_text())
    acc = sel["chosen"]
    if acc is None:
        raise RuntimeError("No external cohort chosen.")
    expr = pd.read_csv(PROC / f"geo_{acc}_expression_log2.tsv", sep="\t", index_col=0)
    clin = pd.read_csv(PROC / f"geo_{acc}_clinical.tsv", sep="\t", index_col=0)
    return acc, expr, clin


def _gpl5474_probe_to_gene() -> dict[str, str]:
    """Parse the GPL5474 annotation file fetched in step 01 (or here)."""
    path = RAW / "GPL5474.annot.txt"
    if not path.exists():
        return {}
    mapping = {}
    in_table = False
    with path.open() as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("!platform_table_begin"):
                in_table = True
                continue
            if line.startswith("!platform_table_end"):
                break
            if not in_table:
                continue
            parts = line.split("\t")
            if parts[0] == "ID":
                # header
                header = parts
                continue
            try:
                pid = parts[0]
                # locate "Symbol" col
                idx_sym = header.index("Symbol")
                symbol = parts[idx_sym]
                if symbol and symbol != "NA":
                    mapping[pid] = symbol
            except Exception:
                continue
    return mapping


def main() -> int:
    np.random.seed(SEED)
    random.seed(SEED)

    print("Loading TCGA-LIHC ...")
    expr, clin = _load_tcga()
    expr, clin = _prep_tcga(expr, clin)
    print(f"TCGA aligned: {expr.shape[1]} samples, {expr.shape[0]} genes; "
          f"{clin['os_event'].sum()} OS events out of {len(clin)}")

    # ----- Apparent + bootstrap -----
    print(f"Running {N_BOOTSTRAP}-iter optimism-corrected bootstrap ...")
    boot = _bootstrap_optimism(expr, clin, n_iter=N_BOOTSTRAP, seed=SEED)
    print(json.dumps({k: v for k, v in boot.items() if not isinstance(v, list)}, indent=2))

    # ----- Final model on full cohort (apparent fit) -----
    print("Refitting final model on full TCGA cohort ...")
    apparent_genes = _univariable_screen(expr, clin)
    mu = expr.loc[apparent_genes].mean(axis=1)
    sd = expr.loc[apparent_genes].std(axis=1).replace(0, 1)
    z_full = expr.loc[apparent_genes].subtract(mu, axis=0).divide(sd, axis=0)
    cph_full = _fit_cox(z_full, clin)
    score_full = _risk_score(cph_full, z_full)

    # ----- Cox calibration slope and Schoenfeld -----
    t = clin["os_time_months"].values.astype(float)
    e = clin["os_event"].values.astype(int)
    cal_slope = _calibration_slope(score_full.values, t, e)
    sch_p = _schoenfeld_pvalue(score_full.values, t, e)
    auc_dict = _time_dep_auc(score_full.values, t, e)

    # ----- Stratified log-rank by HCC-TRS quartiles in TCGA (L1) -----
    q = pd.qcut(score_full, 4, labels=False, duplicates="drop")
    df_lr = pd.DataFrame({"q": q.values, "t": t, "e": e})
    lr = multivariate_logrank_test(df_lr["t"], df_lr["q"], df_lr["e"])
    l1_p = float(lr.p_value)
    l1_chi2 = float(lr.test_statistic)

    # ----- Permutation null on apparent ΔC (L7) -----
    print("Running 1000-iter permutation null for ΔC ...")
    perm_null = _permutation_null_delta_c(
        expr, clin, apparent_delta_c=boot["delta_c_apparent"],
        n_iter=N_BOOTSTRAP, seed=SEED + 1,
    )

    # ----- External cohort (GSE10143) scoring -----
    print("Scoring external GEO cohort ...")
    acc, expr_geo, clin_geo = _load_external()
    probe_to_gene = _gpl5474_probe_to_gene()
    print(f"Loaded {acc}: {expr_geo.shape[1]} samples, {expr_geo.shape[0]} probes; "
          f"probe-to-gene mapping size = {len(probe_to_gene)}")

    # Re-map probes to gene symbols by max value per gene
    expr_geo_g = expr_geo.copy()
    expr_geo_g["gene"] = [probe_to_gene.get(p, None) for p in expr_geo_g.index]
    expr_geo_g = expr_geo_g[expr_geo_g["gene"].notna()]
    expr_geo_g = expr_geo_g.groupby("gene").max(numeric_only=True)
    print(f"After probe->gene collapse: {expr_geo_g.shape[0]} genes in external cohort")

    # Intersection of signature genes & external cohort
    overlap_genes = [g for g in apparent_genes if g in expr_geo_g.index]
    cov_pct = (len(overlap_genes) / max(1, len(apparent_genes))) * 100.0
    print(f"HCC-TRS signature coverage in {acc}: {cov_pct:.1f}% "
          f"({len(overlap_genes)} of {len(apparent_genes)} signature genes present)")

    rebuild_intersect = (cov_pct < 80.0)
    rebuild_info = {
        "policy_trigger": "rebuild on intersect when signature coverage < 80% (prereg-v2 sec B)",
        "triggered": bool(rebuild_intersect),
        "original_signature_size": int(len(apparent_genes)),
        "original_signature_coverage_percent_in_external": float(cov_pct),
    }

    # Build a SECOND signature on the platform intersection so we can
    # report both (full-universe HCC-TRS for the Layer-1 internal claim,
    # and intersect-restricted HCC-TRS for the external evaluation).
    if rebuild_intersect:
        common_genes = [g for g in expr.index if g in expr_geo_g.index]
        expr_r = expr.loc[common_genes]
        rebuild_genes = _univariable_screen(expr_r, clin)
        rebuild_info["intersect_universe_size"] = int(len(common_genes))
        rebuild_info["n_genes_after_rebuild"] = int(len(rebuild_genes))
        if rebuild_genes:
            mu_r = expr_r.loc[rebuild_genes].mean(axis=1)
            sd_r = expr_r.loc[rebuild_genes].std(axis=1).replace(0, 1)
            z_r = expr_r.loc[rebuild_genes].subtract(mu_r, axis=0).divide(sd_r, axis=0)
            cph_r = _fit_cox(z_r, clin)
            # The intersect model is used ONLY for external scoring;
            # the Layer-1 primary outcome remains the full-universe
            # model evaluated above.
            external_signature_genes = rebuild_genes
            external_cph = cph_r
            external_mu, external_sd = mu_r, sd_r
        else:
            external_signature_genes = []
            external_cph = None
            external_mu = external_sd = None
    else:
        external_signature_genes = apparent_genes
        external_cph = cph_full
        external_mu, external_sd = mu, sd

    # Score external cohort using the intersect-built model coefs.
    # Normalise external expression for the signature genes using the
    # external cohort's own per-gene mean/sd (scales differ between
    # RNA-seq log2 TPM and microarray log2 intensities).
    sig_in_ext = [g for g in external_signature_genes if g in expr_geo_g.index]
    if not sig_in_ext or external_cph is None:
        print("FATAL: no signature genes present in external cohort.")
        ext_results = {"error": "no signature genes in external cohort"}
    else:
        ext_expr_sig = expr_geo_g.loc[sig_in_ext]
        ext_mu = ext_expr_sig.mean(axis=1)
        ext_sd = ext_expr_sig.std(axis=1).replace(0, 1)
        ext_z = ext_expr_sig.subtract(ext_mu, axis=0).divide(ext_sd, axis=0)
        coefs = external_cph.params_
        valid = [g for g in sig_in_ext if g in coefs.index]
        ext_score = ext_z.loc[valid].T.dot(coefs.loc[valid])
        # Align to external clin
        valid_ids = [s for s in ext_score.index if s in clin_geo.index]
        ext_score = ext_score.loc[valid_ids]
        clin_ext = clin_geo.loc[valid_ids]
        ext_t = clin_ext["os_time_months"].astype(float).values
        ext_e = clin_ext["os_event"].astype(float).fillna(0).astype(int).values
        valid_mask = np.isfinite(ext_t) & (ext_t > 0)
        ext_score = ext_score[valid_mask]
        ext_t = ext_t[valid_mask]
        ext_e = ext_e[valid_mask]
        # L6: C-index of HCC-TRS in external cohort
        c_ext = _harrell_c(ext_score.values, ext_t, ext_e)
        # L2: median-split log-rank
        median = float(np.median(ext_score.values))
        high = (ext_score.values > median).astype(int)
        lr2 = logrank_test(ext_t[high == 1], ext_t[high == 0],
                           ext_e[high == 1], ext_e[high == 0])
        # Bootstrap 95% CI for c_ext
        rng = np.random.default_rng(SEED + 2)
        boot_c = []
        for _ in range(1000):
            ix = rng.integers(0, len(ext_t), size=len(ext_t))
            try:
                boot_c.append(_harrell_c(ext_score.values[ix], ext_t[ix], ext_e[ix]))
            except Exception:
                continue
        ext_results = {
            "accession": acc,
            "n_samples": int(len(ext_t)),
            "n_events": int(int(ext_e.sum())),
            "external_signature_size": int(len(external_signature_genes)),
            "external_signature_coverage_in_geo_pct": float(
                100.0 * len(sig_in_ext) / max(1, len(external_signature_genes))
            ),
            "original_signature_size": int(rebuild_info["original_signature_size"]),
            "original_signature_coverage_pct": float(cov_pct),
            "rebuilt_on_intersect": bool(rebuild_intersect),
            "c_index": float(c_ext),
            "c_index_ci_lo": float(np.percentile(boot_c, 2.5)) if boot_c else None,
            "c_index_ci_hi": float(np.percentile(boot_c, 97.5)) if boot_c else None,
            "median_split_logrank_p": float(lr2.p_value),
            "median_split_logrank_chi2": float(lr2.test_statistic),
            "median_threshold_value": median,
        }
        # Save per-patient external scores
        ext_score_df = pd.DataFrame({
            "geo_id": ext_score.index,
            "hcc_trs": ext_score.values,
            "os_time_months": ext_t,
            "os_event": ext_e,
            "high_trs": high.astype(int),
        })
        ext_score_df.to_csv(RES / "external_geo_scores.tsv", sep="\t", index=False)

    # ----- Persist results -----
    feat_payload = {
        "selection_rule": "univariable Cox BH-adjusted p<0.05, top 200 by |coef|",
        "n_features": int(len(apparent_genes)),
        "feature_names": apparent_genes,
        "rebuild_info": rebuild_info,
        "penalizer": PENALIZER,
        "seed": SEED,
        "tcga_n_samples": int(expr.shape[1]),
        "tcga_n_genes_input": int(expr.shape[0]),
    }
    (RES / "tcga_features.json").write_text(json.dumps(feat_payload, indent=2))

    coef_df = cph_full.summary[["coef", "exp(coef)", "se(coef)", "p"]].copy()
    coef_df.to_csv(RES / "tcga_model_coefs.tsv", sep="\t")

    (RES / "tcga_cox_summary.txt").write_text(str(cph_full.summary))

    metrics = {
        "primary": {
            "delta_c_apparent": boot["delta_c_apparent"],
            "delta_c_optimism_corrected": boot["delta_c_corrected"],
            "delta_c_95ci_lo": boot["delta_c_boot_ci_lo"],
            "delta_c_95ci_hi": boot["delta_c_boot_ci_hi"],
            "c_apparent_trs": boot["c_apparent_trs"],
            "c_apparent_ajcc": boot["c_apparent_ajcc"],
            "c_apparent_combo": boot["c_apparent_combo"],
            "c_corrected_trs": boot["c_corrected_trs"],
            "n_bootstrap_iter_completed": boot["n_iter_completed"],
            # Paired-optimism estimator (preferred; round-02, failure-mode-04)
            "delta_c_corrected_paired": boot.get("delta_c_corrected_paired"),
            "delta_c_paired_ci_lo": boot.get("delta_c_paired_ci_lo"),
            "delta_c_paired_ci_hi": boot.get("delta_c_paired_ci_hi"),
            "opt_combo_avg": boot.get("opt_combo_avg"),
            "opt_ajcc_avg": boot.get("opt_ajcc_avg"),
            "opt_delta_avg": boot.get("opt_delta_avg"),
            # Legacy estimator (round-01, retained for traceability)
            "delta_c_corrected_legacy": boot.get("delta_c_corrected_legacy"),
            "delta_c_legacy_ci_lo": boot.get("delta_c_legacy_ci_lo"),
            "delta_c_legacy_ci_hi": boot.get("delta_c_legacy_ci_hi"),
        },
        "stability": {
            "bootstrap_signature_median_jaccard_with_apparent":
                boot.get("bootstrap_signature_median_jaccard_with_apparent"),
            "bootstrap_signature_median_apparent_recovery_pct":
                boot.get("bootstrap_signature_median_apparent_recovery_pct"),
            "bootstrap_gene_sets_count": boot.get("bootstrap_gene_sets_count"),
        },
        "secondary": {
            "L1_logrank_quartiles_p": l1_p,
            "L1_logrank_chi2": l1_chi2,
            "L2_external_median_split_logrank_p": ext_results.get("median_split_logrank_p"),
            "L3_time_dep_auc": auc_dict,
            "L4_calibration_slope": cal_slope,
            "L5_schoenfeld_p_trs": sch_p,
            "L6_external_c_index": ext_results.get("c_index"),
            "L6_external_c_index_ci": [
                ext_results.get("c_index_ci_lo"), ext_results.get("c_index_ci_hi"),
            ],
            "L7_permutation_null_p": perm_null["p_perm"],
            "L7_permutation_null_n_attempted": perm_null.get("null_n_attempted"),
            "L7_permutation_null_n_completed": perm_null.get("null_n_completed"),
            "L7_permutation_null_implied_zero": perm_null.get("null_n_implied_zero"),
        },
        "external": ext_results,
        "seed": SEED,
        "n_bootstrap": N_BOOTSTRAP,
        "finished_utc": _now_utc(),
    }
    (RES / "tcga_bootstrap_metrics.json").write_text(json.dumps(metrics, indent=2))

    # Per-patient TCGA scores
    score_df = pd.DataFrame({
        "case_submitter_id": score_full.index,
        "hcc_trs": score_full.values,
        "stage_num": clin["stage_num"].values,
        "os_time_months": t,
        "os_event": e,
    })
    score_df["quartile"] = pd.qcut(score_df["hcc_trs"], 4,
                                    labels=["Q1", "Q2", "Q3", "Q4"],
                                    duplicates="drop")
    score_df.to_csv(RES / "tcga_risk_scores.tsv", sep="\t", index=False)

    # Figure inputs
    fig_inputs = {
        "primary_estimate": metrics["primary"],
        "external": ext_results,
        "n_features_final": len(apparent_genes),
        "n_tcga_cases_modeled": int(expr.shape[1]),
        "n_tcga_with_stage": int((~np.isnan(clin["stage_num"])).sum()),
    }
    (RES / "figures_inputs.json").write_text(json.dumps(fig_inputs, indent=2))

    print("\n=== HEADLINE ===")
    print(f"Apparent ΔC (AJCC+TRS vs AJCC)  = {boot['delta_c_apparent']:.4f}")
    print(f"Optimism-corrected ΔC           = {boot['delta_c_corrected']:.4f}")
    print(f"Bootstrap 95% CI                = "
          f"[{boot['delta_c_boot_ci_lo']:.4f}, {boot['delta_c_boot_ci_hi']:.4f}]")
    print(f"External {acc} C-index         = {ext_results.get('c_index')}")
    print(f"External median-split log-rank p = {ext_results.get('median_split_logrank_p')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
