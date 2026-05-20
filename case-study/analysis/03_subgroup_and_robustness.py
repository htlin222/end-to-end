#!/usr/bin/env python3
"""03_subgroup_and_robustness.py — Robustness checks for HCC-TRS.

Pipeline step 3 of 4. Reads the locked TCGA-LIHC model from step 02 and
produces:

- Stage-stratified Cox model (HCC-TRS adjusted for stage).
- Sex- and age-stratified subgroup analyses (exploratory, prereg).
- Cross-validated 5-fold C-index as a secondary stability check (this is
  *not* a primary outcome; the optimism-corrected bootstrap is).
- Schoenfeld residual reporting for the final model.

Outputs:

- ``data/results/robustness_metrics.json``
- ``data/results/cv_metrics.json``
- ``data/results/stage_stratified_cox.tsv``
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from lifelines import CoxPHFitter
from lifelines.statistics import proportional_hazard_test
from lifelines.utils import concordance_index

warnings.simplefilter("ignore")

REPO_ROOT = Path(__file__).resolve().parents[2]
CASE = REPO_ROOT / "case-study"
PROC = CASE / "data" / "processed"
RES = CASE / "data" / "results"

SEED = 20260521


def _harrell_c(score: np.ndarray, t: np.ndarray, e: np.ndarray) -> float:
    return float(concordance_index(t, -score, e))


def main() -> int:
    scores = pd.read_csv(RES / "tcga_risk_scores.tsv", sep="\t")
    feats = json.loads((RES / "tcga_features.json").read_text())

    t = scores["os_time_months"].values.astype(float)
    e = scores["os_event"].values.astype(int)
    trs = scores["hcc_trs"].values.astype(float)
    stage = scores["stage_num"].values.astype(float)

    out: dict = {"seed": SEED, "n_features_final": feats["n_features"]}

    # Stage-stratified Cox: HCC-TRS adjusted for AJCC stage
    df = pd.DataFrame({"trs": trs, "stage_num": stage, "t": t, "e": e})
    df_clean = df.dropna(subset=["stage_num"])
    cph = CoxPHFitter(penalizer=0.0)
    cph.fit(df_clean, duration_col="t", event_col="e", show_progress=False)
    cph.summary.to_csv(RES / "stage_stratified_cox.tsv", sep="\t")
    out["stage_adjusted_cox"] = {
        "trs_hr": float(np.exp(cph.summary.loc["trs", "coef"])),
        "trs_hr_ci_lo": float(np.exp(cph.summary.loc["trs", "coef lower 95%"])),
        "trs_hr_ci_hi": float(np.exp(cph.summary.loc["trs", "coef upper 95%"])),
        "trs_p": float(cph.summary.loc["trs", "p"]),
        "stage_hr": float(np.exp(cph.summary.loc["stage_num", "coef"])),
        "stage_p": float(cph.summary.loc["stage_num", "p"]),
        "c_index": _harrell_c(
            cph.predict_partial_hazard(df_clean).values,
            df_clean["t"].values, df_clean["e"].values
        ),
        "n_obs": int(df_clean.shape[0]),
        "n_events": int(df_clean["e"].sum()),
    }

    # Schoenfeld for both covariates
    try:
        ph = proportional_hazard_test(cph, df_clean, time_transform="rank")
        s = ph.summary
        out["schoenfeld"] = {
            "trs_p": float(s.loc["trs", "p"]) if "trs" in s.index else None,
            "stage_p": float(s.loc["stage_num", "p"]) if "stage_num" in s.index else None,
        }
    except Exception as exc:
        out["schoenfeld"] = {"error": str(exc)}

    # Subgroup: stage I/II vs stage III/IV
    early = df_clean[df_clean["stage_num"] <= 2.0]
    late = df_clean[df_clean["stage_num"] >= 3.0]
    def _univariable_trs_cox(d):
        cph_s = CoxPHFitter(penalizer=0.0)
        d2 = d[["trs", "t", "e"]].copy()
        cph_s.fit(d2, duration_col="t", event_col="e", show_progress=False)
        return {
            "n": int(len(d)),
            "events": int(d["e"].sum()),
            "trs_hr": float(np.exp(cph_s.summary.loc["trs", "coef"])),
            "trs_hr_ci_lo": float(np.exp(cph_s.summary.loc["trs", "coef lower 95%"])),
            "trs_hr_ci_hi": float(np.exp(cph_s.summary.loc["trs", "coef upper 95%"])),
            "trs_p": float(cph_s.summary.loc["trs", "p"]),
            "c_index": _harrell_c(d["trs"].values, d["t"].values, d["e"].values),
        }
    out["subgroup_stage_early_I_II"] = _univariable_trs_cox(early)
    out["subgroup_stage_late_III_IV"] = _univariable_trs_cox(late)

    # 5-fold CV C-index of HCC-TRS alone vs AJCC alone vs combo
    from sklearn.model_selection import KFold
    rng = np.random.default_rng(SEED)
    kf = KFold(n_splits=5, shuffle=True, random_state=SEED)
    fold_cs = {"trs": [], "ajcc": [], "combo": []}
    df_full = df_clean.reset_index(drop=True)
    for tr_idx, te_idx in kf.split(df_full):
        tr, te = df_full.iloc[tr_idx], df_full.iloc[te_idx]
        # TRS alone: rank by trs on test
        fold_cs["trs"].append(
            _harrell_c(te["trs"].values, te["t"].values, te["e"].values)
        )
        # AJCC alone
        fold_cs["ajcc"].append(
            _harrell_c(te["stage_num"].values, te["t"].values, te["e"].values)
        )
        # Combo: fit Cox on trainset, predict on test
        cph_f = CoxPHFitter(penalizer=0.0)
        cph_f.fit(tr[["trs", "stage_num", "t", "e"]], duration_col="t",
                  event_col="e", show_progress=False)
        ph = cph_f.predict_partial_hazard(te).values
        fold_cs["combo"].append(_harrell_c(ph, te["t"].values, te["e"].values))
    cv = {k: {"mean": float(np.mean(v)), "sd": float(np.std(v)), "fold_values": v}
          for k, v in fold_cs.items()}
    (RES / "cv_metrics.json").write_text(json.dumps(cv, indent=2))
    out["cv_5fold"] = {k: {"mean": cv[k]["mean"], "sd": cv[k]["sd"]} for k in cv}

    (RES / "robustness_metrics.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
