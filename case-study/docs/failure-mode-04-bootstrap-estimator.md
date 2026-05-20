# Failure mode 04 — Bootstrap-optimism estimator deviation

**Date**: 2026-05-21
**Authored by**: Layer-1 autonomous Claude Code session
**Status**: documented; resolved by `02_build_risk_score.py`
patch in round-01 → round-02 revision.

## What happened

In the first `02_build_risk_score.py` (commit `816cb92` and earlier),
the bootstrap distribution recorded for the ΔC-index was:

    delta_c_boot_b = c_combo_b - c_apparent_ajcc

where `c_combo_b` is the bootstrap-fitted AJCC + HCC-TRS model's
C-index evaluated on the original cohort, and `c_apparent_ajcc` is
the AJCC-alone C-index computed once on the original (apparent) data.

This is **not** the standard Harrell-Lee-Mark optimism-corrected ΔC
estimator. The textbook approach is the **paired-optimism** form:

    optimism_b = (C_b^{in-sample} - C_b^{out-of-sample})
    delta_c_corrected = delta_c_apparent - mean(optimism_b)

with the ΔC formed from the **same** bootstrap-fitted AJCC-only and
bootstrap-fitted combo models, both evaluated in-sample and on-sample-
out-of-bag. The CI is then the percentile of
`(delta_c_apparent - optimism_b)` across iterations.

Holding `c_apparent_ajcc` fixed produces a CI that is **narrower than
it should be** because the variability in the AJCC-alone term is
suppressed.

## Honesty contract response

The fix is a code patch to `_bootstrap_optimism` that:

1. For each bootstrap iteration, refit both AJCC-alone and AJCC + TRS
   Cox models on the bootstrap sample.
2. Evaluate both on the bootstrap sample (in-sample) and the original
   sample (out-of-sample).
3. Record `optimism_combo_b - optimism_ajcc_b` per iteration.
4. Report `delta_c_apparent - mean(...)` as the corrected ΔC and the
   percentile CI of `delta_c_apparent - (optimism_combo_b -
   optimism_ajcc_b)`.

Round-1 reviewer 2 (methods) and reviewer 3 (biostat) both flagged
this. The fix is implemented in the round-02 commit; the round-1
metrics are preserved in
`case-study/data/results/tcga_bootstrap_metrics_round01.json`
for traceability, and the round-2 metrics overwrite
`tcga_bootstrap_metrics.json` per the standard naming.

## Expected magnitude of change

- Apparent ΔC = 0.117 is unchanged (it does not depend on the
  bootstrap).
- Optimism-corrected ΔC will move slightly because the optimism
  estimator now includes the AJCC term's optimism (typically small,
  since AJCC alone has low optimism).
- CI will **widen** because the bootstrap variance now includes the
  AJCC term.

Best estimate (pre-rerun): corrected ΔC moves from 0.060 to
approximately 0.055-0.075; CI widens from [0.085, 0.137] to
approximately [0.04, 0.16]. The lower CI bound should still be > 0;
the primary hypothesis is still expected to be confirmed but with
honest uncertainty.

## What is preserved

- Per-iteration random seeds (same RNG sequence).
- All other endpoints (L1-L7).
- The 50-gene cap (prereg-v3).
- The intersect-rebuilding rule (prereg-v2).
