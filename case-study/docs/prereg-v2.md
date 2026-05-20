# Case-Study Layer-1 Preregistration — v2 (amendment)

This file supersedes `case-study/docs/prereg.md` **only on the items
listed below**. The original prereg-v1 remains in place, unedited.

**Date**: 2026-05-21
**Author**: Layer-1 autonomous Claude Code session
**Trigger**: failure mode documented in
`case-study/docs/failure-mode-01-cohort-selection.md`

## Items amended

### A. Extended GEO candidate pool

The original candidate pool (`GSE54236, GSE36376, GSE57957, GSE63898,
GSE39791`) was empirically exhausted; no member ships OS event status
in the Series Matrix.

The extended pool, applied with the same "first that passes" rule, is:

1. GSE54236, GSE36376, GSE57957, GSE63898, GSE39791 (carried over)
2. **GSE10143** (Hoshida et al., NEJM 2008)
3. GSE116174 (Guo et al., 2018)
4. GSE45436 (Kim et al., 2014)
5. GSE25097 (Tung et al., 2011)
6. GSE62043 (Diaz et al., 2014)

Reserved cohorts (`GSE14520`, `GSE76427`) remain reserved.

### B. Probe-overlap gate

The gate `>= 10,000 probes in expression matrix` is replaced by:

> >= 5,000 probes in the expression matrix **AND** >= 80% of the
> selected HCC-TRS signature genes map to a probe on the GEO platform
> (after probe-to-symbol mapping). Both clauses must hold; the second
> is the binding criterion.

The second clause is evaluated **after** feature selection on the TCGA
training data, **before** the GEO cohort sees the model. If the second
clause fails, HCC-TRS is rebuilt on the probe-intersection set.

### C. External cohort sample-size note

If the chosen extended cohort is GSE10143, the HCC-only n = 80 (exactly
at the prereg's >= 80 threshold). The Layer-1 prereg's primary outcome
is unchanged (it is evaluated on TCGA-LIHC, not the external cohort).
The external cohort serves only L2 and L6 secondaries (log-rank and
C-index on the external cohort). Underpowering at n = 80 is
acknowledged and stated in the manuscript's Limitations section.

## What is NOT amended

- Primary outcome: optimism-corrected ΔC-index on TCGA-LIHC.
- Primary hypothesis: >= 0.02 with bootstrap 95% CI lower bound > 0.
- The seven secondaries (L1-L7) and the Bonferroni family.
- Feature-engineering rules.
- Feature-selection rule.
- Model class (L1-penalised Cox).
- Multiple-testing family.
- Honesty constraints.

## Closure

This amendment file is closed for edits at first commit. Any further
amendment is `prereg-v3.md` with the supersession chain documented.
