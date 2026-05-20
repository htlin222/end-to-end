# Round 2 — Methods Reviewer

**Round**: 02
**Reviewer**: Methods (per `prompts/03-reviewer-methods.md`)
**Date**: 2026-05-21
**Reviewed artefacts**: `case-study/manuscript/main.tex` at HEAD post-
commit `d7b9918`,
`case-study/analysis/02_build_risk_score.py`,
`case-study/analysis/03_subgroup_and_robustness.py`,
`case-study/analysis/05_dca_idi_calibration.py`,
`case-study/data/results/tcga_bootstrap_metrics.json`,
`case-study/docs/failure-mode-04-bootstrap-estimator.md`.

## Overall impression

Substantial response to Round-1 comments. The paired-optimism estimator
is implemented; the 50-gene cap is documented; the standardisation
contract is explicit; the bootstrap-feature stability is now reported.
The widening of the CI from [0.085, 0.137] to [0.003, 0.113] is the
correct consequence of the methodological fix and the manuscript reports
this honestly.

## Per-Round-1-comment status

| R1 ID | Status | Notes |
|-------|--------|-------|
| 1 (standardisation contract) | resolved | One-paragraph note in Methods §2.4, explicit. |
| 2 (paired-optimism estimator) | resolved | Implementation matches the formula in failure-mode-04; CI widens to [0.003, 0.113]; primary hypothesis still met but with narrow margin. Honest. |
| 3 (score-test vs Cox MLE) | resolved | Methods cites Cox partial-likelihood score test; equivalence justification stated. |
| 4 (Jaccard stability) | resolved | Median Jaccard 0.20, 34% apparent recovery reported. **This is low**; see Comment 1 below. |
| 5 (multiple-testing family) | resolved | Methods now states "primary outcome is single confirmatory test; seven secondaries are Bonferroni family". |
| 6 (one sample per case) | resolved | Methods §2.1 names lexicographic-minimum rule. |
| 7 (CV calibration slope) | resolved | Reported in Results. |
| 8 (diagnoses-row selection) | resolved | Methods §2.1. |
| 9 (uv.lock at tag) | deferred | To be verified at case-study-v1.0.0 tag time. |

All Round-1 high-severity comments are resolved or deferred to the tag
boundary. Two new observations:

## New Round-2 comments

### Comment 1 [MEDIUM, was R1-#4 follow-up] — Signature instability deserves a Discussion paragraph

The median Jaccard of bootstrap gene sets vs apparent is 0.20, and the
median apparent-recovery is 34%. This means a typical bootstrap
iteration recovers only ~17 of the 50 apparent genes — the signature
is **fold-dependent**. The optimism-corrected ΔC of 0.063 captures the
performance hit from this instability, so the headline number is
honest, but the manuscript should add a one-paragraph Limitations
note acknowledging that **the gene identity of \HCCRTS is fold-
dependent** and that the score's prognostic utility is driven by a
broader transcriptomic-program signal rather than a specific 50-gene
panel. This sharpens the clinical-translation caveat.

Severity: medium.

### Comment 2 [LOW] — Time-dependent AUC implementation detail

The `_time_dep_auc` function in `02_build_risk_score.py` uses a
heuristic landmark AUC (subjects with t >= L OR event-by-L). For
strict comparability to TRIPOD-aligned papers using Uno (Stat Med 2007)
inverse-probability-of-censoring weighting, mention this approximation
in Methods. The numbers (0.78/0.76/0.81) are not biased materially at
30%+ event rates but the disclosure is required.

Severity: low. Required: one sentence in Methods §2.7.

## Verdict

**`accept`**, conditional on Comment 1 being addressed in the
Discussion's Limitations paragraph in the next minor revision cycle.

The Round-1 blocker and high-severity items are resolved; the new
Round-2 items are low/medium and do not require a re-run. I would
recommend accept now and minor-revision at the editor's discretion.

For the purposes of round closure (per `prompts/03-reviewer-methods.md`
acceptance criterion: "no new high-severity issue is observed"), I
treat this as accept with the explicit understanding that Comment 1
will be folded into Round-3 revisions.
