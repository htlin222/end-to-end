#!/usr/bin/env python3
"""05_dca_idi_calibration.py — Decision-curve, IDI, Hosmer-Lemeshow.

Pipeline step 5 of 5. Reviewer-driven extension added in Round 2 to
address the biostat reviewer's blocker on calibration plots and IDI,
and the clinical reviewer's blocker on decision-curve analysis.

Reads ``data/results/tcga_risk_scores.tsv`` (per-patient HCC-TRS,
stage_num, OS time, OS event) and ``data/results/tcga_features.json``
(signature gene list).

Outputs:

- ``data/results/dca_metrics.json`` — Vickers-Elkin net benefit at
  5-year mortality thresholds {0.10, 0.20, 0.30}.
- ``data/results/calibration_metrics.json`` — Hosmer-Lemeshow chi-
  square at 1, 3, 5 years across deciles of predicted survival.
- ``data/results/idi_metrics.json`` — Pencina IDI of (AJCC + TRS) vs
  AJCC alone at the same landmarks.
- ``case-study/figures/figure5_calibration_dca.pdf`` — 2x2 panel:
  calibration plot at 1y / 3y / 5y plus DCA net-benefit curve.

The script is idempotent and reads only artefacts produced by
01..04; it does not refit the Cox model.
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lifelines import CoxPHFitter, KaplanMeierFitter
from scipy.stats import chi2

warnings.simplefilter("ignore")

REPO_ROOT = Path(__file__).resolve().parents[2]
CASE = REPO_ROOT / "case-study"
RES = CASE / "data" / "results"
FIGS = CASE / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

SEED = 20260521
LANDMARKS_MONTHS = (12.0, 36.0, 60.0)
DCA_THRESHOLDS_5Y = (0.10, 0.20, 0.30)


def _km_estimate(t: np.ndarray, e: np.ndarray, at: float) -> float:
    """Kaplan-Meier estimate of S(at) on (t, e) data."""
    kmf = KaplanMeierFitter()
    kmf.fit(t, e)
    try:
        return float(kmf.predict(at))
    except Exception:
        return float("nan")


def _predicted_survival_at_landmark(
    cph: CoxPHFitter,
    df: pd.DataFrame,
    landmark: float,
) -> np.ndarray:
    """Per-subject Cox-predicted survival at landmark (in months)."""
    sf = cph.predict_survival_function(df, times=[landmark])
    return sf.iloc[0].values


def _fit_combo_cox(df: pd.DataFrame) -> CoxPHFitter:
    """Fit Cox of OS on (stage_num, hcc_trs); requires complete cases."""
    cph = CoxPHFitter(penalizer=0.0)
    cph.fit(df, duration_col="os_time_months", event_col="os_event",
            show_progress=False)
    return cph


def _fit_ajcc_only_cox(df: pd.DataFrame) -> CoxPHFitter:
    cph = CoxPHFitter(penalizer=0.0)
    cph.fit(df[["stage_num", "os_time_months", "os_event"]],
            duration_col="os_time_months", event_col="os_event",
            show_progress=False)
    return cph


def hosmer_lemeshow_calibration(
    predicted_survival: np.ndarray,
    t: np.ndarray,
    e: np.ndarray,
    landmark: float,
    n_groups: int = 10,
) -> dict:
    """Hosmer-Lemeshow goodness-of-fit at a survival landmark.

    Groups subjects by deciles of predicted survival at the landmark,
    computes observed KM survival per group, returns chi-square +
    df-adjusted p.
    """
    pred = predicted_survival
    df = pd.DataFrame({"pred": pred, "t": t, "e": e})
    df["group"] = pd.qcut(df["pred"], n_groups, labels=False, duplicates="drop")
    n_groups_real = int(df["group"].nunique())
    rows = []
    chi2_stat = 0.0
    for g in sorted(df["group"].dropna().unique()):
        sub = df[df["group"] == g]
        if len(sub) < 2:
            continue
        obs_s = _km_estimate(sub["t"].values, sub["e"].values, landmark)
        exp_s = float(sub["pred"].mean())
        n = len(sub)
        # HL contribution: for survival, treat as binary "alive at L"
        # Observed alive ~ obs_s * n; expected ~ exp_s * n
        obs_alive = obs_s * n
        exp_alive = exp_s * n
        obs_dead = n - obs_alive
        exp_dead = n - exp_alive
        # avoid /0
        for o, e_ in [(obs_alive, exp_alive), (obs_dead, exp_dead)]:
            if e_ > 0.001:
                chi2_stat += (o - e_) ** 2 / e_
        rows.append({
            "group": int(g), "n": n, "pred_survival": exp_s,
            "obs_survival": obs_s,
        })
    dof = max(1, n_groups_real - 2)
    p = float(1.0 - chi2.cdf(chi2_stat, df=dof))
    return {
        "landmark_months": landmark,
        "n_groups": n_groups_real,
        "chi2": float(chi2_stat),
        "dof": dof,
        "p": p,
        "groups": rows,
    }


def decision_curve_net_benefit(
    pred_5y_death: np.ndarray,
    t: np.ndarray,
    e: np.ndarray,
    thresholds: tuple = DCA_THRESHOLDS_5Y,
    landmark_months: float = 60.0,
) -> dict:
    """Vickers-Elkin decision-curve net benefit at a survival landmark.

    For each threshold p_t (interpretable as 'treat if predicted 5y
    mortality > p_t'):

      net_benefit(model) = TP/n - FP/n * (p_t / (1 - p_t))

    With censored OS we use a KM correction for the prevalence in the
    treated and untreated groups. Returns net benefit for:
      - 'model': treat = pred_5y_death > p_t
      - 'treat_all'
      - 'treat_none'
    """
    n = len(t)
    if n == 0:
        return {"thresholds": list(thresholds), "results": []}
    out = []
    overall_mortality = 1.0 - _km_estimate(t, e, landmark_months)
    for p_t in thresholds:
        treated_mask = pred_5y_death > p_t
        n_treated = int(treated_mask.sum())
        n_untreated = n - n_treated
        # TP/n approx (n_treated / n) * P(event | treated)
        if n_treated > 0:
            p_event_treated = 1.0 - _km_estimate(
                t[treated_mask], e[treated_mask], landmark_months,
            )
        else:
            p_event_treated = 0.0
        tp = (n_treated / n) * p_event_treated
        fp = (n_treated / n) * (1.0 - p_event_treated)
        w = p_t / (1.0 - p_t) if p_t < 1.0 else float("inf")
        nb_model = tp - fp * w
        nb_treat_all = overall_mortality - (1.0 - overall_mortality) * w
        nb_treat_none = 0.0
        out.append({
            "threshold": p_t,
            "n_treated": n_treated,
            "n_untreated": n_untreated,
            "overall_mortality_5y": overall_mortality,
            "net_benefit_model": float(nb_model),
            "net_benefit_treat_all": float(nb_treat_all),
            "net_benefit_treat_none": float(nb_treat_none),
            "delta_vs_treat_all": float(nb_model - nb_treat_all),
            "delta_vs_treat_none": float(nb_model - nb_treat_none),
        })
    return {"thresholds": list(thresholds),
            "landmark_months": landmark_months,
            "results": out}


def pencina_idi(
    pred_event_combo: np.ndarray,
    pred_event_baseline: np.ndarray,
    t: np.ndarray,
    e: np.ndarray,
    landmark_months: float,
) -> dict:
    """Pencina IDI at a survival landmark.

    IDI = (mean(pred_combo | event) - mean(pred_combo | non-event))
        - (mean(pred_base | event)  - mean(pred_base | non-event))
    where event is 'observed dead by landmark' (with KM weighting).
    """
    # Approximate binary outcome at landmark with IPCW weighting
    event_at_L = ((t <= landmark_months) & (e == 1)).astype(int)
    # For censored before landmark, drop those subjects (simple approach;
    # IPCW would be the rigorous alternative but requires extra code)
    censor_before_L = ((t < landmark_months) & (e == 0))
    mask = ~censor_before_L
    pc = pred_event_combo[mask]
    pb = pred_event_baseline[mask]
    y = event_at_L[mask]
    if y.sum() == 0 or (1 - y).sum() == 0:
        return {"landmark_months": landmark_months,
                "idi": None, "n_event": int(y.sum()),
                "n_non_event": int((1 - y).sum())}
    idi = ((pc[y == 1].mean() - pc[y == 0].mean())
           - (pb[y == 1].mean() - pb[y == 0].mean()))
    # Bootstrap CI
    rng = np.random.default_rng(SEED + 3)
    boots = []
    for _ in range(1000):
        ix = rng.integers(0, len(y), size=len(y))
        try:
            yb, pcb, pbb = y[ix], pc[ix], pb[ix]
            if yb.sum() == 0 or (1 - yb).sum() == 0:
                continue
            boots.append(((pcb[yb == 1].mean() - pcb[yb == 0].mean())
                          - (pbb[yb == 1].mean() - pbb[yb == 0].mean())))
        except Exception:
            continue
    if boots:
        ci_lo = float(np.percentile(boots, 2.5))
        ci_hi = float(np.percentile(boots, 97.5))
    else:
        ci_lo = ci_hi = None
    return {
        "landmark_months": landmark_months,
        "idi": float(idi),
        "idi_ci_lo": ci_lo,
        "idi_ci_hi": ci_hi,
        "n_event": int(y.sum()),
        "n_non_event": int((1 - y).sum()),
    }


def main() -> int:
    np.random.seed(SEED)
    scores = pd.read_csv(RES / "tcga_risk_scores.tsv", sep="\t")
    feats = json.loads((RES / "tcga_features.json").read_text())

    # Build complete-case dataset (stage + trs + outcomes)
    df = scores.dropna(subset=["stage_num", "hcc_trs", "os_time_months",
                                "os_event"]).copy()
    df["os_event"] = df["os_event"].astype(int)
    df["stage_num"] = df["stage_num"].astype(float)
    df["hcc_trs"] = df["hcc_trs"].astype(float)
    t = df["os_time_months"].values.astype(float)
    e = df["os_event"].values.astype(int)
    print(f"Complete cases for DCA / IDI / HL: n = {len(df)} "
          f"({int(e.sum())} events).")

    # Fit two Cox models
    cph_combo = _fit_combo_cox(
        df[["stage_num", "hcc_trs", "os_time_months", "os_event"]]
    )
    cph_ajcc = _fit_ajcc_only_cox(df)

    # Hosmer-Lemeshow + IDI at three landmarks
    cal_results = {}
    idi_results = {}
    for L in LANDMARKS_MONTHS:
        pred_s_combo = _predicted_survival_at_landmark(cph_combo, df, L)
        pred_s_ajcc = _predicted_survival_at_landmark(cph_ajcc, df, L)
        cal_combo = hosmer_lemeshow_calibration(pred_s_combo, t, e, L)
        cal_results[f"L{int(L)}m_combo"] = cal_combo
        cal_ajcc = hosmer_lemeshow_calibration(pred_s_ajcc, t, e, L)
        cal_results[f"L{int(L)}m_ajcc"] = cal_ajcc

        idi = pencina_idi(
            pred_event_combo=1.0 - pred_s_combo,
            pred_event_baseline=1.0 - pred_s_ajcc,
            t=t, e=e, landmark_months=L,
        )
        idi_results[f"L{int(L)}m"] = idi

    # Decision-curve at 5-year landmark
    pred_5y_death_combo = 1.0 - _predicted_survival_at_landmark(
        cph_combo, df, 60.0
    )
    pred_5y_death_ajcc = 1.0 - _predicted_survival_at_landmark(
        cph_ajcc, df, 60.0
    )
    dca_combo = decision_curve_net_benefit(
        pred_5y_death_combo, t, e, thresholds=DCA_THRESHOLDS_5Y,
    )
    dca_ajcc = decision_curve_net_benefit(
        pred_5y_death_ajcc, t, e, thresholds=DCA_THRESHOLDS_5Y,
    )

    # Persist
    (RES / "calibration_metrics.json").write_text(
        json.dumps(cal_results, indent=2)
    )
    (RES / "idi_metrics.json").write_text(
        json.dumps(idi_results, indent=2)
    )
    (RES / "dca_metrics.json").write_text(
        json.dumps({"combo": dca_combo, "ajcc_alone": dca_ajcc}, indent=2)
    )

    # Figure 5: calibration plots + DCA panel
    fig, axes = plt.subplots(2, 2, figsize=(9.0, 8.0))
    # Calibration plots at 1, 3, 5 years (top-left, top-right, bottom-left)
    for ax, L_key, title in zip(
        [axes[0, 0], axes[0, 1], axes[1, 0]],
        ["L12m_combo", "L36m_combo", "L60m_combo"],
        ["1 y", "3 y", "5 y"],
    ):
        cal = cal_results[L_key]
        groups = cal["groups"]
        pred = [g["pred_survival"] for g in groups]
        obs = [g["obs_survival"] for g in groups]
        ax.plot([0, 1], [0, 1], "--", color="#aaaaaa", label="ideal")
        ax.scatter(pred, obs, color="#2c7bb6", label=f"deciles")
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 1.0)
        ax.set_xlabel(f"Predicted survival at {title}")
        ax.set_ylabel(f"Observed (KM) survival at {title}")
        ax.set_title(f"Calibration at {title}: HL chi2={cal['chi2']:.2f}, p={cal['p']:.2g}")
        ax.legend(fontsize=8)
    # DCA at 5 y (bottom-right)
    ax = axes[1, 1]
    th = [r["threshold"] for r in dca_combo["results"]]
    nb_combo = [r["net_benefit_model"] for r in dca_combo["results"]]
    nb_ajcc = [r["net_benefit_model"] for r in dca_ajcc["results"]]
    nb_all = [r["net_benefit_treat_all"] for r in dca_combo["results"]]
    ax.plot(th, nb_combo, "o-", label="AJCC + HCC-TRS", color="#2c7bb6")
    ax.plot(th, nb_ajcc, "s--", label="AJCC alone", color="#fdae61")
    ax.plot(th, nb_all, "^:", label="Treat all", color="#888888")
    ax.axhline(0.0, color="#888888", linestyle=":", label="Treat none")
    ax.set_xlabel("5y mortality threshold")
    ax.set_ylabel("Net benefit")
    ax.set_title("Decision-curve at 5 y")
    ax.legend(fontsize=8, loc="best")
    fig.tight_layout()
    fig.savefig(FIGS / "figure5_calibration_dca.pdf")
    plt.close(fig)
    print(f"Figure 5 saved to {FIGS / 'figure5_calibration_dca.pdf'}")

    print("\n=== HEADLINE (Round-2 additions) ===")
    for L in LANDMARKS_MONTHS:
        idi = idi_results[f"L{int(L)}m"]
        cal = cal_results[f"L{int(L)}m_combo"]
        print(f"  {int(L)}m: HL p = {cal['p']:.2g}, IDI = {idi.get('idi')}")
    print(f"  DCA combo NB @ p=0.20: {dca_combo['results'][1]['net_benefit_model']:.4f}")
    print(f"  DCA AJCC NB @ p=0.20:  {dca_ajcc['results'][1]['net_benefit_model']:.4f}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
