# Round 2 — Biostatistics Reviewer

**Round**: 02
**Reviewer**: Biostatistics (per `prompts/03-reviewer-biostat.md`)
**Date**: 2026-05-21
**Reviewed artefacts**: `case-study/manuscript/main.tex` at HEAD post-
commit `d7b9918`, `case-study/data/results/tcga_bootstrap_metrics.json`,
`case-study/data/results/idi_metrics.json`,
`case-study/data/results/calibration_metrics.json`,
`case-study/data/results/dca_metrics.json`,
`case-study/data/results/robustness_metrics.json`,
`case-study/data/results/cv_metrics.json`,
`case-study/data/results/uno_c_sensitivity.json`.

## Overall impression

The Round-1 blockers are resolved. Harrell's C is named explicitly,
with Uno's C as a sensitivity (0.695 vs Harrell 0.714 at the 60-month
truncation; the small bias is consistent with TCGA-LIHC's modest
censoring). Calibration at 1, 3, 5 years is reported with Hosmer-
Lemeshow chi-square + p (0.12, 0.66, 0.38 respectively — all above
0.05, indicating acceptable calibration). The Schoenfeld test for the
stage covariate (p=0.034) is now flagged as a non-PH finding with a
stratified-Cox sensitivity in Discussion. The paired-optimism
estimator is implemented; the CI widening from [0.085, 0.137] to
[0.003, 0.113] is honest. Pencina IDI is reported at all three
landmarks (0.11, 0.14, 0.18).

I am ready to accept; two small items remain.

## Per-Round-1-comment status

| R1 ID | Status | Notes |
|-------|--------|-------|
| 1 (Harrell vs Uno) | resolved | Methods names Harrell's C; Uno sensitivity at tau=60m reported. |
| 2 (calibration plot at landmarks) | resolved | Figure 5 includes calibration plot at 1/3/5 y with HL p reported. |
| 3 (power statement) | resolved | Methods includes Pencina-D'Agostino power statement (~0.80 to detect a true paired-optimism delta of 0.05 at alpha=0.05). |
| 4 (paired-optimism CI) | resolved | Headline CI is now the paired-optimism CI [0.003, 0.113]; the legacy CI is documented in failure-mode-04 and referenced in the manuscript. |
| 5 (stage Schoenfeld non-PH) | resolved | Stratified-Cox sensitivity noted in Discussion; the trs covariate's Schoenfeld p (0.38) is unaffected. |
| 6 (L1-L7 Bonferroni tally) | resolved | Results section explicitly tallies. |
| 7 (Fine-Gray) | resolved | Methods states TCGA-LIHC clinical export used does not separate cancer-specific from any-cause death; competing-risks treatment is therefore not feasible. Honest. |
| 8 (IDI) | resolved | At 5 y, IDI = 0.18; at 1 y, 0.11; at 3 y, 0.14. Reported. |
| 9 (Breslow tie handling) | resolved | One sentence in Methods §2.5. |
| 10 (PCG64 RNG) | resolved | Methods notes "`np.random.default_rng` (PCG64) with seed 20260521". |

## New Round-2 comments

### Comment 1 [LOW] — DCA Brier-score sensitivity at the 5-year landmark

The DCA is reported. As a TRIPOD-aligned complement, the integrated
Brier score (IBS) at the 5-year horizon would round out the
discrimination + calibration + utility set. `lifelines` does not ship
an IBS directly; `scikit-survival`'s `brier_score` does. This is
optional and would extend rather than fix the reporting.

Severity: low.

### Comment 2 [LOW] — Uno C tau choice

The Uno C is reported at tau=60 months. The choice of tau matters
(Uno's C-statistic is generally bounded by the censoring tail at
tau). State that tau=60m is the 5-year landmark used elsewhere in
the manuscript; the sensitivity is robust to tau in {36m, 60m, 84m}.

Severity: low. One sentence in Methods §2.7.

## Verdict

**`accept`**.

All Round-1 blockers and high-severity items are resolved. Round-2
items are low-severity refinements. The statistical machinery now
meets TRIPOD 2015 / TRIPOD+AI 2024 reporting standards within the
constraints of the available public data.
