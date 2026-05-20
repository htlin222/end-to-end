# Failure mode 02 — Bootstrap-runtime budget overrun

**Date**: 2026-05-21
**Authored by**: Layer-1 autonomous Claude Code session
**Status**: documented and resolved by prereg-v3 (signature cap 200 → 50)

## What happened

The Layer-1 primary outcome (1000-iteration optimism-corrected
bootstrap of ΔC-index in TCGA-LIHC) and the L7 permutation null (1000
iteration permutation test) together exceeded a usable runtime budget
when the post-screen signature was capped at 200 genes per prereg-v1.

Empirical profiling on the production environment:

- Univariable score-test screen across 11,674 protein-coding genes:
  ~0.2 s per pass (vectorised).
- L1-penalised Cox fit on 200 standardised features (lifelines
  `CoxPHFitter`, `penalizer=0.1, l1_ratio=1.0`): ~3.1 s per fit.
- Per bootstrap iteration: ~3.4 s → 1000 iters = ~56 minutes.
- Per permutation iteration: ~3.4 s → 1000 iters = ~56 minutes.
- Total budget: ~112 minutes for two locked endpoints + auxiliary
  diagnostics.

## Honesty contract response

The bottleneck is the L1-penalised Cox fit, not the screen.

Two options were considered:

**Option A (rejected)** — keep `topn=200` and accept the runtime, with
the L1 penalty doing most of the shrinkage. The cost is operational
(>2 hour pipeline) and risks the audit re-execution clock.

**Option B (chosen)** — cap the signature at the top 50 genes by
univariable |Z|, then let L1-penalised Cox shrink within that 50.
Documented as a one-line amendment in `prereg-v3.md`, committed
**before** the bootstrap is re-run.

Option B is chosen because:

- Layer-1 honesty contract explicitly permits post-commit amendments
  that are documented as superseding prereg entries and committed
  before the affected code path runs.
- The 50-feature cap is conservative for HCC OS signatures from the
  literature (Hoshida 2008 NEJM used ~186 probes, but the
  HepatoPredict / Roessler 2010 / Boyault 2007 signatures are
  18-65 genes).
- The L1 penalty already drives most of the 150 surplus features to
  zero. The fit time saved is real; the inference change is small.

## What did not change

- Primary outcome definition.
- Primary hypothesis threshold.
- Bootstrap or permutation iteration counts.
- Feature-engineering, normalisation, or model class.

## Audit trail

- This file: `case-study/docs/failure-mode-02-bootstrap-runtime.md`.
- Prereg supersession: `case-study/docs/prereg-v3.md`.
- The code change: `case-study/analysis/02_build_risk_score.py`
  line `SIGNATURE_TOPN = 50`.
