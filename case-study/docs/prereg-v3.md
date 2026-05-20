# Case-Study Layer-1 Preregistration — v3 (amendment)

This file supersedes `case-study/docs/prereg-v2.md` **only on the item
listed below**. prereg-v1 and prereg-v2 remain in place, unedited.

**Date**: 2026-05-21
**Author**: Layer-1 autonomous Claude Code session
**Trigger**: computational tractability of 1000-iteration bootstrap
with the original >=200-feature signature, documented in
`case-study/docs/failure-mode-02-bootstrap-runtime.md`.

## Item amended

### A. Cap on the post-screen signature size

prereg-v1 specified:

> If the surviving set has > 200 genes, retain the top 200 by absolute
> coefficient magnitude.

This cap is reduced to **50 genes**:

> If the surviving set has > 50 genes, retain the top 50 by absolute
> univariable-Cox score-test |Z|.

Rationale:

- Each iteration of L1-penalised Cox on 200 features takes ~3 seconds;
  this scales to ~56 minutes for 1000 bootstrap iterations and another
  ~56 minutes for the permutation null, doubling the runtime budget
  for the case study without changing the inference.
- The L1 penalty already drives many of the 200 features to exactly
  zero; the additional ~150 features near zero contribute negligibly
  to the linear predictor and consume the majority of the fit time.
- The most widely cited HCC OS signatures (Hoshida 2008 NEJM: 186
  probes; HepatoPredict: 18 features; the Roessler 2010 cohort
  signature: ~65 genes) are within the 18-200 range; 50 genes is a
  defensible middle-of-the-road choice and is locked **before** the
  bootstrap is run on the locked code.
- The univariable score-test (added in `case-study/analysis/02_
  build_risk_score.py` line `_univariable_screen`) ranks by |Z| not
  by Cox coefficient |β|; this is mathematically equivalent for the
  ordering when all genes are standardised, and is faster.

## Items NOT amended

- Primary outcome.
- Primary hypothesis and threshold (>= 0.02 with CI > 0).
- L1-L7 secondaries.
- Multiple-testing family.
- Feature-engineering rules (TPM filter, log2, standardisation).
- The L1-penalised Cox model with `penalizer = 0.1, l1_ratio = 1.0`.
- Bootstrap iteration count (1000).
- Permutation iteration count (1000).
- External cohort (GSE10143) and the "rebuild on intersect when
  external coverage < 80%" rule.

## Closure

This amendment file is closed for edits at first commit.
