#!/usr/bin/env python3
"""04_figures.py — Produce the four manuscript figures.

Figures (all PDF):

- ``case-study/figures/figure1_km_quartiles.pdf`` — KM curves by HCC-TRS
  quartile in TCGA-LIHC.
- ``case-study/figures/figure2_forest.pdf`` — Forest plot of the
  stage-adjusted Cox hazard ratios + subgroup HRs.
- ``case-study/figures/figure3_calibration_auc.pdf`` — Time-dependent
  AUC at 1, 3, 5 years and calibration plot for HCC-TRS + AJCC.
- ``case-study/figures/figure4_external.pdf`` — KM by HCC-TRS median
  split in GSE10143 (Hoshida 2008 cohort), with C-index + log-rank p.
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
from lifelines import KaplanMeierFitter

warnings.simplefilter("ignore")

REPO_ROOT = Path(__file__).resolve().parents[2]
CASE = REPO_ROOT / "case-study"
RES = CASE / "data" / "results"
FIGS = CASE / "figures"
FIGS.mkdir(parents=True, exist_ok=True)


def _km_panel(ax, t, e, group, labels, palette=None):
    kmf = KaplanMeierFitter()
    for i, g in enumerate(sorted(np.unique(group))):
        mask = group == g
        if mask.sum() == 0:
            continue
        kmf.fit(t[mask], e[mask], label=labels[i] if i < len(labels) else str(g))
        c = (palette or {}).get(g, None)
        kmf.plot(ax=ax, ci_show=True, color=c)
    ax.set_xlabel("Months since diagnosis")
    ax.set_ylabel("Overall survival probability")


def figure1():
    sc = pd.read_csv(RES / "tcga_risk_scores.tsv", sep="\t")
    metrics = json.loads((RES / "tcga_bootstrap_metrics.json").read_text())
    t = sc["os_time_months"].values.astype(float)
    e = sc["os_event"].values.astype(int)
    q = sc["quartile"].astype(str).values
    qmap = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4, "nan": np.nan}
    qnum = np.array([qmap.get(s, np.nan) for s in q])
    mask = ~np.isnan(qnum)
    fig, ax = plt.subplots(figsize=(6.0, 4.6))
    palette = {1.0: "#2c7bb6", 2.0: "#abd9e9", 3.0: "#fdae61", 4.0: "#d7191c"}
    _km_panel(ax, t[mask], e[mask], qnum[mask],
              labels=["Q1 (lowest TRS)", "Q2", "Q3", "Q4 (highest TRS)"],
              palette=palette)
    ax.set_title("TCGA-LIHC: KM by HCC-TRS quartile")
    p = metrics["secondary"]["L1_logrank_quartiles_p"]
    ax.text(0.02, 0.06, f"4-strata log-rank p = {p:.2e}", transform=ax.transAxes)
    fig.tight_layout()
    fig.savefig(FIGS / "figure1_km_quartiles.pdf")
    plt.close(fig)


def figure2():
    rob = json.loads((RES / "robustness_metrics.json").read_text())
    rows = [
        ("HCC-TRS (stage-adjusted)", rob["stage_adjusted_cox"]["trs_hr"],
         rob["stage_adjusted_cox"]["trs_hr_ci_lo"],
         rob["stage_adjusted_cox"]["trs_hr_ci_hi"]),
        ("AJCC stage (mutually adjusted)", rob["stage_adjusted_cox"]["stage_hr"],
         np.nan, np.nan),
        ("HCC-TRS subgroup: stage I/II", rob["subgroup_stage_early_I_II"]["trs_hr"],
         rob["subgroup_stage_early_I_II"]["trs_hr_ci_lo"],
         rob["subgroup_stage_early_I_II"]["trs_hr_ci_hi"]),
        ("HCC-TRS subgroup: stage III/IV", rob["subgroup_stage_late_III_IV"]["trs_hr"],
         rob["subgroup_stage_late_III_IV"]["trs_hr_ci_lo"],
         rob["subgroup_stage_late_III_IV"]["trs_hr_ci_hi"]),
    ]
    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    y = np.arange(len(rows))[::-1]
    for i, (label, hr, lo, hi) in enumerate(rows):
        yy = y[i]
        ax.plot([hr], [yy], "o", color="#222222")
        if not np.isnan(lo) and not np.isnan(hi):
            ax.plot([lo, hi], [yy, yy], "-", color="#444444")
    ax.axvline(1.0, color="#aaaaaa", linestyle="--")
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in rows])
    ax.set_xlabel("Hazard ratio (OS)")
    ax.set_xscale("log")
    ax.set_title("HCC-TRS stage-adjusted and subgroup HRs (TCGA-LIHC)")
    fig.tight_layout()
    fig.savefig(FIGS / "figure2_forest.pdf")
    plt.close(fig)


def figure3():
    metrics = json.loads((RES / "tcga_bootstrap_metrics.json").read_text())
    auc = metrics["secondary"]["L3_time_dep_auc"]
    cal = metrics["secondary"]["L4_calibration_slope"]
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.6))
    months = [12, 36, 60]
    values = [auc.get(f"auc_{m}m") for m in months]
    axes[0].bar([str(m) for m in months],
                 [v if v is not None else 0 for v in values],
                 color="#4c72b0")
    axes[0].set_xlabel("Landmark (months)")
    axes[0].set_ylabel("Time-dependent AUC")
    axes[0].set_ylim(0.5, 1.0)
    axes[0].set_title("Discrimination over time")
    for i, v in enumerate(values):
        if v is not None:
            axes[0].text(i, v + 0.01, f"{v:.2f}", ha="center")
    # Calibration: slope as a single bar plus reference line
    axes[1].bar(["HCC-TRS"], [cal], color="#dd8452")
    axes[1].axhline(1.0, color="#aaaaaa", linestyle="--", label="ideal slope = 1")
    axes[1].set_ylim(0.0, max(2.0, cal + 0.5))
    axes[1].set_ylabel("Calibration slope")
    axes[1].set_title("Calibration of HCC-TRS")
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(FIGS / "figure3_calibration_auc.pdf")
    plt.close(fig)


def figure4():
    ext = pd.read_csv(RES / "external_geo_scores.tsv", sep="\t")
    metrics = json.loads((RES / "tcga_bootstrap_metrics.json").read_text())
    e_res = metrics["external"]
    t = ext["os_time_months"].values.astype(float)
    e = ext["os_event"].values.astype(int)
    high = ext["high_trs"].values.astype(int)
    fig, ax = plt.subplots(figsize=(6.0, 4.6))
    _km_panel(ax, t, e, high,
              labels=["HCC-TRS low (≤ median)", "HCC-TRS high (> median)"],
              palette={0: "#4c72b0", 1: "#c44e52"})
    p = e_res.get("median_split_logrank_p")
    c = e_res.get("c_index")
    ci_lo = e_res.get("c_index_ci_lo")
    ci_hi = e_res.get("c_index_ci_hi")
    ax.set_title(f"External validation: KM by HCC-TRS median split ({e_res.get('accession')})")
    ax.text(0.02, 0.06,
            f"C-index = {c:.2f} ({ci_lo:.2f}-{ci_hi:.2f}); "
            f"log-rank p = {p:.2f}; n = {e_res.get('n_samples')}",
            transform=ax.transAxes)
    fig.tight_layout()
    fig.savefig(FIGS / "figure4_external.pdf")
    plt.close(fig)


def main() -> int:
    print("Generating figure 1 (KM by TCGA quartile) ...")
    figure1()
    print("Generating figure 2 (forest) ...")
    figure2()
    print("Generating figure 3 (AUC / calibration) ...")
    figure3()
    print("Generating figure 4 (external KM) ...")
    figure4()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
