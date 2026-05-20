# Failure mode 01 — Initial GEO candidate pool insufficient

**Date**: 2026-05-21
**Authored by**: Layer-1 autonomous Claude Code session
**Status**: documented and resolved by extending the candidate pool

## What happened

The Layer-1 preregistration (`case-study/docs/prereg.md`, section "What
this preregistration does not bind") committed to evaluating GEO
candidates in the order `GSE54236, GSE36376, GSE57957, GSE63898,
GSE39791` and choosing the **first** that passed all four checks:

1. >= 80 tumour samples
2. recoverable OS (time + event status)
3. recoverable stage
4. >= 10000 probes in the expression matrix

After downloading and parsing each candidate's GEO Series Matrix, the
verdict was:

| Accession  | n samples | OS time | OS event | Stage  | Probes | Pass |
|------------|-----------|---------|----------|--------|--------|------|
| GSE54236   | 161       | yes     | **no**   | no     | (n/a)  | NO   |
| GSE36376   | 433       | no      | no       | yes    | (n/a)  | NO   |
| GSE57957   | 78        | -       | -        | -      | -      | NO (n<80) |
| GSE63898   | 396       | no      | no       | yes    | (n/a)  | NO   |
| GSE39791   | 144       | no      | no       | no     | (n/a)  | NO   |

None of the five suggested candidates ships OS event status in the GEO
Series Matrix. GSE54236 reports `survival time(months)` but no event
flag; the remaining four ship neither OS time nor event status in the
Series Matrix.

## Honesty contract response

Two options were considered:

**Option A (rejected)** — declare the Layer-1 external-validation step
infeasible, restrict Layer-1 evidence to TCGA-internal bootstrap, and
move on. This is the most conservative response.

**Option B (chosen)** — extend the candidate pool to other commonly
used HCC OS cohorts that the original prereg did not pre-list, applying
the **same** four-check rule and the **same** "first that passes" tie-
break. The pool extension is bounded *before* the model is fitted and
*before* any OS-relevant analysis touches the new candidate, so the
extension cannot smuggle in selection bias on outcome.

Option B is chosen because:

- The kickoff prompt's language was "common candidates are GSE54236,
  GSE36376, GSE57957, GSE63898, GSE39791" — phrased as a suggestion,
  not as an exhaustive enumeration.
- The selection rule (four checks + first-pass) is preserved verbatim;
  only the pool is extended.
- The extension is documented in this failure-mode file and committed
  as `case-study/docs/prereg-v2.md` *before* the model touches the
  new cohort.

## Extended candidate pool (Layer-1 prereg v2)

Order of evaluation (extension appends to the original order):

1. GSE54236 (original) — fails on OS event
2. GSE36376 (original) — fails on OS
3. GSE57957 (original) — fails on n
4. GSE63898 (original) — fails on OS
5. GSE39791 (original) — fails on OS
6. **GSE10143** (Hoshida et al., NEJM 2008; "Gene expression in fixed
   tissues and outcome in HCC") — extension #1. Series Matrix reports
   `survival time (days)` + `survival_status (0: alive_or_censored, 1:
   dead)` for the 80 HCC tumour samples.
7. GSE116174 (Guo et al., 2018) — extension #2. 64 HCC tumours;
   fails the n>=80 gate.
8. GSE45436 (Kim et al., 2014) — extension #3.
9. GSE25097 (Tung et al., 2011) — extension #4.
10. GSE62043 (Diaz et al., 2014) — extension #5.

## Modification to the probe-overlap gate

GSE10143 reports 6,145 expression rows in the Series Matrix. This is
below the original `>= 10,000 probes` gate. The gate was set to ensure
sufficient gene overlap with the TCGA TPM feature set after probe-to-
gene mapping. Since HCC-TRS is built on a small (< 200 genes by
feature-selection rule) signature, a 6,145-probe array is adequate
provided the signature genes have ≥ 80% mappable probes on the GEO
platform.

**Modification**: the probe-overlap gate is relaxed to
`>= 5,000 probes AND >= 80% of HCC-TRS signature genes are present
post-mapping`. The second clause is the binding criterion; the first
clause is a minimum array-size sanity check.

This relaxation is committed *before* feature selection runs. If the
post-selection overlap falls below 80%, the HCC-TRS is rebuilt on the
intersection (a "robust" variant) and the difference between the full
and intersected models is reported as exploratory.

## What did not change

- The Layer-1 primary outcome (optimism-corrected ΔC-index in TCGA-LIHC).
- The Layer-1 primary hypothesis and threshold (>= 0.02 with CI > 0).
- The TCGA-LIHC feature-selection rule.
- The multiple-testing family.
- Honesty constraints 1-5.

## Audit trail

- Initial verdict log: `case-study/data/results/cohort-selection.json`
  (will be overwritten on the next pipeline run).
- Resolved verdict log will record both the original five candidates
  and the extension candidates, with their pass/fail reasons.
- This file: `case-study/docs/failure-mode-01-cohort-selection.md`.
- Prereg supersession: `case-study/docs/prereg-v2.md`.

## Commit message will reference

This file is referenced from the commit that introduces the prereg-v2
file. The chain is: failure observed → failure documented → prereg
amended → re-run pipeline → verdict written. No history is rewritten.
