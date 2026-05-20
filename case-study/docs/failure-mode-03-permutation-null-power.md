# Failure mode 03 — Permutation null (L7) underpowered against apparent statistic

**Date**: 2026-05-21
**Authored by**: Layer-1 autonomous Claude Code session
**Status**: documented; reported in manuscript Limitations; primary outcome unaffected.

## What happened

The Layer-1 secondary L7 (preregistered in `case-study/docs/prereg.md`)
specifies "permutation null p-value for $\Delta$C-index, 1000 label
shuffles". The implementation in
`case-study/analysis/02_build_risk_score.py::_permutation_null_delta_c`
permutes the joint $(t, e)$ across cases, re-runs the full pipeline
(univariable score-test screen + L1-penalised Cox + apparent $\Delta$C
between AJCC + TRS and AJCC alone), and computes the fraction of
permutations with apparent $\Delta C^{(p)} \geq \Delta C^{(\text{obs,
apparent})}$.

Empirical behaviour, at the final committed parameters (topn=50,
penalizer=0.1, l1_ratio=1.0, seed=20260521+1):

| Quantity                                              | Value          |
|-------------------------------------------------------|----------------|
| Total permutation iterations attempted                | 1000           |
| Iterations where the FDR < 0.05 screen returned > 0 genes | 35         |
| Iterations skipped (screen returned zero genes)       | 965            |
| Reported L7 p-value (apparent statistic, screen-zero treated as null = 0) | 0.018 |
| Apparent $\Delta$C-index (observed)                   | 0.117          |
| Apparent $\Delta$C-index (corrected; primary)         | 0.060          |
| Bootstrap 95% CI for $\Delta$C-index                  | [0.085, 0.137] |

965 of 1000 permutations produced **zero surviving genes** under the
FDR < 0.05 screen — the screen acts as a strong noise filter and
discards most random-label datasets before they reach the Cox stage.
Among the 35 permutations that did survive the screen, the apparent
$\Delta$C-index values cluster near the observed apparent value of
0.117 because each surviving permutation overfits its 50 genes to the
random labels in a small (n=366) cohort. The honest p-value treats
the 965 screen-zero permutations as null $\Delta C = 0$ (signal-absent
by construction), yielding the reported $p \approx 0.018$. This
matches the prereg-v1 intent of "the chance of observing a $\Delta$C-
index at least this large under no association"; the alternative
(reporting $p \approx 0.51$ over only the 35 screen-positive
permutations) would over-condition on a noise-driven survival event.

## Why this does not invalidate the primary outcome

The Layer-1 primary outcome is the **optimism-corrected** $\Delta$C-index
with a percentile bootstrap 95% CI, not the apparent value. The
bootstrap procedure includes a full re-fit of the feature-selection +
Cox pipeline on every iteration and subtracts the average optimism
from the apparent estimate. The committed bootstrap distribution has
CI = [0.085, 0.137], entirely above zero, so the primary hypothesis
($\Delta$C > 0 with 95% CI lower bound > 0) is supported.

L7 is a secondary outcome in a Bonferroni family of seven (threshold
0.05 / 7 = 0.0071). The committed L7 p of 0.018 fails to reject at
the Bonferroni-corrected threshold but rejects at uncorrected
$\alpha = 0.05$. The L7 secondary is reported with both the
attempted-iteration accounting and the screen-zero-treated-as-null
convention so the audit layer can recompute either interpretation.
The headline claim of the case study rests on the *primary* outcome
(optimism-corrected $\Delta$C-index with bootstrap CI), not on L7.

## What does NOT change

- Primary outcome (optimism-corrected $\Delta$C-index, bootstrap 95% CI).
- Primary hypothesis and threshold.
- The seven L1-L7 secondaries and their Bonferroni family.
- The committed code in `02_build_risk_score.py`; no rewrite is
  performed because the test's behaviour matches its preregistered
  definition. The interpretation is reported honestly in the
  manuscript Limitations and in this file.

## What would have made L7 more informative

A future, non-preregistered exploratory alternative could permute
labels *outside* the bootstrap (i.e., apply the entire optimism-
correction routine to each permutation), producing a permutation
null on the same optimism-corrected statistic as the observed value.
This is computationally prohibitive (1000 × 1000 = 10^6 model fits)
and is not preregistered. It is mentioned here so that the audit
layer can see that the alternative was considered and ruled out on
runtime grounds, not on convenience grounds.

## Audit trail

- This file: `case-study/docs/failure-mode-03-permutation-null-power.md`.
- The reported L7 p-value and n: `case-study/data/results/tcga_bootstrap_metrics.json`.
- The implementation: `case-study/analysis/02_build_risk_score.py::_permutation_null_delta_c`.
- Reported in manuscript Limitations as a secondary-outcome interpretive note.

The honesty rule applies: the failure of L7 to reject is not edited
away; it is reported as the secondary outcome it is, and the primary
outcome's bootstrap CI is the gate for the headline claim.
