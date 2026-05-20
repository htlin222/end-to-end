# Layer-2 Audit — Statistical reproducibility log

**Tag**: `case-study-v1.0.0`
**Tolerance**: 1e-6 (relative) for deterministic quantities; 5e-2
(absolute, on CI endpoints) for bootstrap quantities.
**Audit date**: 2026-05-21

This log re-derives the headline statistics in the case-study
manuscript from the regenerated intermediate artefacts produced by the
audit re-execution (see `reexec.md`). The regenerated intermediates
were obtained by running `analysis/01..05` on a clean clone with `uv
sync` at the audit tag.

## Headline numbers from the regenerated `tcga_bootstrap_metrics.json`

```
primary.c_apparent_ajcc          = 0.599817122442904
primary.c_apparent_trs           = 0.713659896455595
primary.c_apparent_combo         = 0.716709905158848
primary.delta_c_apparent         = 0.116892782715944
primary.delta_c_corrected_paired = 0.062783495163101
primary.delta_c_paired_ci_lo     = 0.002682368802595
primary.delta_c_paired_ci_hi     = 0.113185087705740
primary.delta_c_corrected_legacy = 0.059982600570052
primary.delta_c_legacy_ci_lo     = 0.083409177901586
primary.delta_c_legacy_ci_hi     = 0.138765789137924
primary.n_bootstrap_iter_completed = 999

secondary.L1_logrank_quartiles_p  = 2.367950e-14
secondary.L1_logrank_chi2         = 66.5237
secondary.L3_time_dep_auc.auc_12m = 0.7812
secondary.L3_time_dep_auc.auc_36m = 0.7635
secondary.L3_time_dep_auc.auc_60m = 0.8062
secondary.L4_calibration_slope    = 0.7012
secondary.L5_schoenfeld_p_trs     = 0.3797
secondary.L7_permutation_null_p   = 0.018
```

External-cohort metrics (L2 / L6) are `None` on the audit re-run
because the GPL5474 annotation file is missing (see `reexec.md`).
The committed `tcga_bootstrap_metrics_round01.json` file (which is
preserved as a snapshot of the round-01 bootstrap) does carry external
values; those are taken at face value below for the claim-alignment
analysis but cannot be independently regenerated.

## Independent re-derivation

The audit re-fitted Cox models directly from the regenerated
`tcga_risk_scores.tsv` using `lifelines.CoxPHFitter(penalizer=0.0)`
and `lifelines.utils.concordance_index`:

| Quantity                   | Independent | Pipeline JSON | Manuscript | Verdict |
|----------------------------|-------------|---------------|------------|---------|
| n analytic set             | 366         | 366           | 366        | ✓ |
| n OS events                | 130         | 130           | 130        | ✓ |
| n with non-missing stage   | 342         | 342           | 342        | ✓ |
| stage I/II count           | 254         | (cohort)      | 254        | ✓ |
| stage III/IV count         | 88          | (cohort)      | 88         | ✓ |
| Harrell C TRS apparent     | 0.713660    | 0.713660      | (implied)  | ✓ (≤ 1e-6) |
| Harrell C AJCC alone       | 0.599817    | 0.599817      | 0.60       | ✓ |
| Harrell C AJCC + TRS       | 0.716710    | 0.716710      | 0.72       | ✓ |
| Apparent ΔC                | 0.116893    | 0.116893      | 0.117      | ✓ |
| Adjusted Cox TRS HR (per 1 SD) | 6.6644 | 6.6644        | 6.66       | ✓ |
| Adjusted Cox TRS 95% CI   | 3.856 – 11.519 | 3.856 – 11.519 | 3.86 – 11.52 | ✓ |
| Adjusted Cox TRS p        | 1.093e-11   | 1.093e-11     | 1.1e-11    | ✓ |
| Adjusted Cox stage HR      | 1.3812      | 1.3812        | 1.38       | ✓ |
| Adjusted Cox stage p       | 0.003156    | 0.003156      | 0.003      | ✓ |
| 4-strata log-rank χ²       | 66.5237     | 66.5237       | 66.5       | ✓ |
| 4-strata log-rank p        | 2.368e-14   | 2.368e-14     | 2.4e-14    | ✓ |
| Time-dep AUC 12m           | 0.7812      | 0.7812        | 0.78       | ✓ |
| Time-dep AUC 36m           | 0.7635      | 0.7635        | 0.76       | ✓ |
| Time-dep AUC 60m           | 0.8062      | 0.8062        | 0.81       | ✓ |
| Schoenfeld p TRS           | 0.3797      | 0.3797        | 0.38       | ✓ |
| L7 permutation null p      | (matches re-exec) | 0.018   | 0.018      | ✓ |

The independent re-derivation matches the pipeline JSON to floating-
point precision (well within the 1e-6 tolerance) for every
deterministic quantity.

## Subgroup, IDI, DCA, calibration

| Quantity (file) | File value | Manuscript | Verdict |
|---|---|---|---|
| Stage I/II subgroup TRS HR (`robustness_metrics.json:subgroup_stage_early_I_II.trs_hr`) | 7.5958 | 7.60 | ✓ |
| Stage I/II subgroup TRS 95% CI | 3.689 – 15.642 | 3.69 – 15.64 | ✓ |
| Stage I/II subgroup TRS p | 3.77e-08 | 3.8e-08 | ✓ |
| Stage III/IV subgroup TRS HR | 7.2597 | 7.26 | ✓ |
| Stage III/IV subgroup TRS 95% CI | 3.070 – 17.167 | 3.07 – 17.17 | ✓ |
| Stage III/IV subgroup TRS p | 6.35e-06 | 6.3e-06 | ✓ |
| 5-fold CV C combo (mean) | 0.7060 | 0.706 | ✓ |
| 5-fold CV C combo (SD) | 0.0571 | 0.057 | ✓ |
| 5-fold CV C AJCC (mean) | 0.6001 | 0.600 | ✓ |
| 5-fold CV C AJCC (SD) | 0.0941 | 0.094 | ✓ |
| Hosmer-Lemeshow p @ 12m (`robustness_metrics.json`) | 0.1196 | 0.12 | ✓ |
| Hosmer-Lemeshow p @ 36m | 0.6591 | 0.66 | ✓ |
| Hosmer-Lemeshow p @ 60m | 0.3819 | 0.38 | ✓ |
| IDI 12m (`idi_metrics.json`) | 0.1111, CI [0.068, 0.156] | 0.111, CI 0.068 – 0.156 | ✓ |
| IDI 36m | 0.1402, CI [0.0921, 0.1841] | 0.140, CI 0.092 – 0.184 | ✓ |
| IDI 60m | 0.1781, CI [0.1268, 0.2280] | 0.178, CI 0.127 – 0.228 | ✓ |
| DCA combo NB @ p_t=0.20 (`dca_metrics.json`) | 0.3636 | 0.364 | ✓ |
| DCA AJCC alone NB @ p_t=0.20 | 0.3569 | 0.357 | ✓ |

The IDI and DCA numbers reproduce, but the Schoenfeld report has a
**minor pipeline-vs-file discrepancy**: `robustness_metrics.json` has
`schoenfeld.trs_p = 0.2571`, while `tcga_bootstrap_metrics.json`
records `secondary.L5_schoenfeld_p_trs = 0.3797`. The two scripts
compute Schoenfeld on different model specifications
(`03_subgroup_and_robustness.py` runs Schoenfeld on the
stage-adjusted bivariable Cox, whereas `02_build_risk_score.py` runs
it on a univariable Cox of TRS alone). The manuscript cites 0.38
(univariable). Both are present in the artefact ledger and the
manuscript-cited value matches `02_build_risk_score.py`'s output.

## Bootstrap CI alignment (the headline)

The manuscript abstract states (lines 64-67):

> "the apparent ΔC-index of `AJCC pathologic stage + HCC-TRS` over
> `AJCC alone` was 0.117; after Harrell-Lee-Mark optimism correction
> over 1000 case-bootstrap iterations with full-pipeline refitting,
> the optimism-corrected ΔC was 0.060 (95% bootstrap CI 0.085 –
> 0.137)."

The regenerated `tcga_bootstrap_metrics.json` (and the round-01
snapshot) record **two** estimators:

- **paired-optimism (the methods section names this as the headline)**:
  ΔC = 0.0628, 95% CI = **[0.0027, 0.1132]**.
- **round-1 legacy estimator (AJCC apparent held fixed)**:
  ΔC = 0.0600, 95% CI = **[0.0834, 0.1388]**.

The committed `tcga_bootstrap_metrics_round01.json` records
ΔC = 0.0600, 95% CI = [0.0846, 0.1369] — these are the **legacy**
estimator's numbers from the round-01 bootstrap, slightly different
from the round-02 legacy numbers in `tcga_bootstrap_metrics.json`
because the round-02 estimator re-ran the bootstrap with a different
permutation accounting (see `failure-mode-04`).

The abstract's reported point estimate **0.060** matches the legacy
estimator, and the abstract's reported CI **[0.085, 0.137]** matches
the **round-01 legacy** CI (0.0846, 0.1369). But the manuscript's
methods section (lines 251-261) explicitly names the paired-optimism
estimator as the headline (the legacy estimator is "reported for
traceability" only). The paired-optimism CI is **[0.003, 0.113]** —
its lower bound is 30× smaller than the abstract's "0.085".

This is a substantive within-manuscript inconsistency. The abstract's
"the optimism-corrected ΔC was 0.060 (95% bootstrap CI 0.085 –
0.137)" reads as if it is the headline, but the headline estimator
per the methods is paired-optimism, whose point estimate is 0.063
(not 0.060) and whose CI lower bound is 0.003 (not 0.085). The
strength of the primary-hypothesis claim ("ΔC ≥ 0.02 with CI lower
bound > 0") is materially different between the two CIs: 0.085 clears
the threshold by ~4×, whereas 0.003 clears the threshold by ~30%.

Independent re-bootstrap (1000 iterations, seed 20260521,
full-pipeline refit) inside the audit-controlled `02_build_risk_score.py`
re-execution produced the exact paired-optimism numbers
(`delta_c_corrected_paired = 0.062783495`, CI = [0.002682369,
0.113185088]), reproducing to floating-point precision; so the
bootstrap **distribution is reproducible**, but the **abstract reports
a different estimator's numbers than the methods section names as
headline**.

## Stage-stratified Cox claim

The manuscript Results (lines 433-437) states:

> "a stage-stratified Cox (stratifying by stage 1-2 vs 3-4) was fit;
> HCC-TRS retained its independent effect with HR per 1-SD of 7.34
> (95% CI 4.04–13.33, p = 1.9e-10), comparable to the additive-model
> estimate."

The committed `stage_stratified_cox.tsv` (produced by
`03_subgroup_and_robustness.py` line 233) records `trs` HR = 6.66,
not 7.34. Inspection of the writing code (lines 228-233 of
`03_subgroup_and_robustness.py`) confirms that the saved model is
actually a **stage-adjusted** Cox (both `trs` and `stage_num` as
linear covariates), **not** a true `strata`-stratified Cox. The
manuscript-cited HR=7.34 (CI 4.04 – 13.33, p = 1.9e-10) does not
appear in any committed result file; `grep -rn "7\.34\|4\.04\|13\.33"
case-study/data/results/` returns no hits. The cited HR therefore
cannot be traced to a regenerable computation.

## Verdict per quantity

- **Deterministic statistics (C-index, log-rank, Cox HR, AUC, slopes,
  IDI, DCA, HL p, CV)**: reproduce within 1e-6.
- **Paired-optimism bootstrap CI (the named headline)**: reproduces
  within 1e-9 from the regenerated bootstrap.
- **Legacy-estimator bootstrap CI**: reproduces within the round-1 vs
  round-2 estimator difference (≤ 0.002 on CI endpoints, within the
  5e-2 tolerance).
- **External cohort (L2, L6)**: not reproducible from the pipeline on
  a clean clone (probe-to-gene annotation file gap).
- **Stage-stratified HR (manuscript 7.34)**: untraceable to any
  committed artefact; the saved file records 6.66 from a stage-
  adjusted (not stratified) model.
