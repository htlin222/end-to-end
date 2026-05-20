# Case-Study Layer-1 Preregistration

This file preregisters the **Layer-1-internal** analytic design of the
case study. It is distinct from `../../docs/prereg.md`, which
preregisters the Layer-3 external-validation design that the human
operator runs against GSE14520 and GSE76427. Layer 1 has no access to
those two cohorts.

**Date of preregistration**: 2026-05-21
**Author**: Layer-1 autonomous Claude Code session (Opus 4.7, 1M context)
**Commit hash when this file is committed**: recorded by git
**Status**: closed for edits at first commit; supersession via
`prereg-v2.md` only.

## Sub-claim

A transcriptome-derived **HCC overall-survival risk score (HCC-TRS)**
trained on TCGA-LIHC primary HCC tumours, when added to AJCC pathologic
stage as an additive covariate in a Cox proportional-hazards model,
improves Harrell's C-index for overall survival over AJCC pathologic
stage alone.

## Primary outcome (Layer-1-internal)

**Variable**: ΔC-index defined as

```
ΔC = C(AJCC + HCC-TRS) - C(AJCC alone)
```

evaluated by **1000-iteration optimism-corrected case-bootstrap** on
TCGA-LIHC primary HCC tumour samples with overall-survival information
available.

**Statistic**: Harrell's C-index using `lifelines.utils.concordance_index`
(equivalent to `survival::concordance` with default tie handling).

**Optimism correction**: per Harrell, Lee, Mark (Stat Med 1996), the
apparent C minus the average (bootstrap C on bootstrap sample - bootstrap
C on original sample), reported with 95% percentile bootstrap CI from
the 1000 iterations.

## Primary hypothesis

H1: optimism-corrected ΔC-index >= 0.02 in TCGA-LIHC.

(0.02 is set tighter than the Layer-3 0.03 threshold to reflect within-
cohort optimism; Layer 3's bar is the clinically meaningful one. Layer
1's bar is "the model has any signal beyond AJCC at all".)

## Null hypothesis and rejection threshold

H0: ΔC-index <= 0 in TCGA-LIHC.

Reject H0 iff the 95% bootstrap CI lower bound is > 0.

A reject decision is reported as positive Layer-1 evidence and triggers
external-cohort evaluation in the non-reserved GEO cohort. A non-reject
decision is reported as negative Layer-1 evidence and the manuscript
draft documents that the score is uninformative under the prespecified
test. **No threshold tuning, no cohort swap, no metric swap** is
permitted post-hoc.

## Secondary outcomes (Layer-1-internal)

| ID  | Outcome                                                                                                      | Test                            |
|-----|--------------------------------------------------------------------------------------------------------------|---------------------------------|
| L1  | Stratified log-rank p between HCC-TRS quartiles in TCGA-LIHC                                                 | log-rank with 3 df              |
| L2  | Stratified log-rank p between HCC-TRS median-split high vs low in the non-reserved GEO cohort                | log-rank with 1 df              |
| L3  | Time-dependent AUC at 1, 3, 5 years for AJCC + HCC-TRS vs AJCC alone in TCGA-LIHC                            | inverse-prob-of-censoring AUC   |
| L4  | Calibration slope at 1, 3, 5 years for AJCC + HCC-TRS in TCGA-LIHC                                           | Cox calibration slope           |
| L5  | Schoenfeld global p-value for HCC-TRS in the TCGA-LIHC Cox model                                             | proportional-hazards test       |
| L6  | C-index of AJCC + HCC-TRS in the non-reserved GEO cohort, using TCGA-locked coefficients                     | Harrell C with 1000-iter bs CI  |
| L7  | Permutation null p-value for ΔC-index, 1000 label shuffles                                                   | permutation test                |

## Feature engineering (locked)

1. Input matrix: TCGA-LIHC primary tumour STAR-counts converted to TPM
   per the GDC harmonised pipeline. Genes filtered to protein-coding
   per GENCODE v36; genes retained if TPM >= 1 in >= 50% of primary-
   tumour samples.
2. Log transform: `log2(TPM + 1)`.
3. No batch-effect correction within TCGA (single project, single
   pipeline). Quantile-normalisation between TCGA and the GEO cohort is
   applied before external scoring; the normaliser is fit on TCGA only.

## Feature selection (locked)

Within the training fold of each bootstrap iteration:

1. Univariable Cox per gene; retain genes with BH-adjusted p < 0.05.
2. If the surviving set has > 200 genes, retain the top 200 by absolute
   coefficient magnitude.
3. Standardise (z-score) per gene.

## Model (locked)

L1-penalised Cox regression (`CoxnetSurvivalAnalysis` from
scikit-survival if available; otherwise lifelines' `CoxPHFitter` with
`penalizer=0.1, l1_ratio=1.0`). The penalty strength `lambda` is chosen
by 5-fold internal CV within the training fold by maximising the
partial-likelihood-based C-index.

The trained linear predictor is the HCC-TRS for any held-out sample.

## Risk strata (locked, prespecified before any KM curve is drawn)

- TCGA-LIHC: HCC-TRS quartiles (Q1-Q4).
- GEO cohort: HCC-TRS median split (high vs low).

The thresholds are computed *on the TCGA training fold* and frozen.

## Multiple-testing family

The Layer-1 primary test is a single confirmatory test. The seven
Layer-1 secondaries (L1-L7) are a Bonferroni family with threshold
0.05 / 7 = 0.0071.

## Sample handling rules

- Only primary tumour samples (TCGA sample type code 01) are kept.
- Recurrent tumour (02) and adjacent normal (11) are excluded.
- Patients with `vital_status` missing or `days_to_last_followup`
  missing AND `vital_status = "Alive"` are excluded.
- Patients with OS time = 0 days are excluded (data-entry artefact).
- Stage missing or coded "[Not Available]" / "[Discrepancy]" /
  "Stage X" are *not* dropped from the cohort but are dropped from
  models that include AJCC stage; this is reported.

## Software stack

- Python 3.12 (uv-managed; lockfile pinned).
- `pandas`, `numpy`, `scipy`, `scikit-learn`, `lifelines`,
  `statsmodels`. `scikit-survival` if it installs; otherwise lifelines
  fallback documented.
- Seed: 20260521. Set on `numpy.random`, `random`, and the model RNG.

## What this preregistration does not bind

- The chosen non-reserved GEO cohort. The selection rule is prespecified
  (>=80 tumours, OS available, stage available, >= 10k overlapping
  protein-coding genes) but the identity is not locked, because cohort
  availability changes over time. The chosen cohort is recorded as the
  first in this list to pass all four checks, evaluated in order:
  GSE54236, GSE36376, GSE57957, GSE63898, GSE39791.
- Manuscript wording. Reviewer rounds revise the manuscript freely.

## Honesty constraints

1. No cohort swap. If the chosen GEO cohort fails after the analysis is
   run, the failure is reported; we do not try another cohort.
2. No metric swap. Harrell C is the locked primary metric.
3. No outcome promotion. Anything not in this prereg is exploratory.
4. No post-hoc thresholding. Quartiles / median splits are computed on
   training-fold thresholds frozen before KM curves are inspected.
5. Failures are documented in
   `reviewer-logs/round-NN/failure-mode-*.md` and resolved by new
   commits, not by rewriting history.
