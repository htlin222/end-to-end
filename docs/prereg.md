# Preregistration — Case-Study Meta-Experiment

This preregistration locks the *external-validation* design of the case
study (Layer 3 in `docs/design.md`). It does **not** preregister Layer 1's
internal choices, because Layer 1 is the autonomous pipeline whose
behaviour the Viewpoint is studying.

**Date of preregistration**: 2026-05-21
**Commit hash when this file is committed**: recorded automatically by git
**Operator**: Hsieh-Ting Lin (ORCID 0009-0002-3974-4528)

## What is being preregistered

The Layer-3 external validation that the operator (the only human in the
pipeline) will run against whatever risk-score formula Layer 1's autonomous
pipeline produces. The cohorts, the metrics, the null hypothesis, the
effect-size threshold, and the multiple-testing family are all fixed
**before** Layer 1 begins.

## What is *not* being preregistered

- Layer 1's selected sub-claim, statistical method, or feature set. Layer 1
  is autonomous; if its choices were constrained from outside, the
  Viewpoint's argument would collapse.
- The text of either manuscript. Both manuscripts are products of the
  pipeline (Layer 1 for the case-study manuscript; the operator + Claude
  for the Viewpoint manuscript) and follow their own integrity rules in
  `docs/design.md`.

## Primary outcome

**Variable**: ΔC-index defined as

```
C-index(AJCC pathologic stage + Layer-1-produced risk score r)
  - C-index(AJCC pathologic stage alone)
```

computed for overall survival in the pooled external validation set
(`GSE14520` + `GSE76427`).

**Statistic**: Harrell's C-index, computed with the `survival` package's
default tie-handling.

**Confidence interval**: 1000-iteration bootstrap, 95% percentile method.

## Primary hypothesis

ΔC-index >= 0.03, the threshold commonly used in TRIPOD-aligned prognostic-
model reports as a minimum clinically meaningful prognostic improvement.

## Null hypothesis and rejection threshold

H0: ΔC-index = 0.

Reject H0 iff the 95% bootstrap CI lower bound is > 0.

A reject decision is reported as **positive case-study finding**. A non-
reject decision is reported as **null case-study finding** and the Viewpoint
discusses it; under no circumstance is the cohort set, the metric, or the
threshold modified post-hoc to flip the decision.

## Pre-specified secondary outcomes

All secondaries share the same Layer-3 input (the Layer-1 risk score),
applied to the same two cohorts, and are reported regardless of the primary
outcome.

| ID  | Outcome                                                                                | Test                          |
|-----|----------------------------------------------------------------------------------------|-------------------------------|
| S1  | Cohort-specific ΔC-index in GSE14520 alone                                             | Bootstrap 95% CI              |
| S2  | Cohort-specific ΔC-index in GSE76427 alone                                             | Bootstrap 95% CI              |
| S3  | Calibration slope at 1 year for the Layer-1 risk score, pooled                         | Hosmer-Lemeshow with deciles  |
| S4  | Calibration slope at 3 years for the Layer-1 risk score, pooled                        | Hosmer-Lemeshow with deciles  |
| S5  | Calibration slope at 5 years for the Layer-1 risk score, pooled                        | Hosmer-Lemeshow with deciles  |
| S6  | Decision-curve net benefit at 5-year mortality thresholds {0.1, 0.2, 0.3}              | Vickers-Elkin DCA             |
| S7  | Integrated discrimination improvement (IDI) over AJCC stage alone                      | Pencina IDI with bootstrap CI |

## Exploratory analyses

The following are explicitly labelled exploratory and may not be promoted
to a primary or secondary finding regardless of result:

- `GSE54236` (Villa et al, 2016) treated as a third validation cohort.
- Subgroup analyses by viral aetiology (HBV / HCV / non-viral) where
  metadata permits.
- Comparison between the Layer-1 risk score and the published HCC immune-
  subtype classifier of Sia et al, 2017.

## Multiple-testing family

The pre-specified family is the **seven secondary outcomes**. Bonferroni-
corrected significance threshold for each secondary: 0.05 / 7 = 0.0071.

The primary outcome is **not** included in the correction family; it is the
single confirmatory test.

## Stop rules

- The Layer-3 validation is a single-shot analysis. It is not iterated.
- If a data-integrity failure occurs (e.g., a GEO cohort is found to have
  no overlapping clinical-feature support for the Layer-1 risk score), it
  is recorded as a Layer-1 failure mode in
  `reviewer-logs/audit/findings.md` and the analysis proceeds with the
  remaining cohorts. If both cohorts fail, the primary outcome is
  unreportable and that fact is the headline finding.

## Honesty constraints binding the operator

1. **No cohort swap.** GSE14520 and GSE76427 are the preregistered external
   validation cohorts. They cannot be replaced after Layer 1's risk score
   is known.
2. **No metric swap.** Harrell's C-index is the preregistered primary
   metric. It cannot be replaced with C-statistic, Uno's C, or any
   integrated-AUC variant after Layer 1's risk score is known.
3. **No threshold tuning.** The 0.03 clinical-significance threshold and
   the 0.05 alpha are fixed.
4. **No outcome promotion.** Exploratory results stay exploratory.

## Baseline-choice note (AJCC vs BCLC)

The Viewpoint title and `docs/design.md` describe the domain prompt as
"survival stratification beyond BCLC stage". TCGA-LIHC clinical files
record **AJCC pathologic stage**, not BCLC, and the GEO cohorts above also
lack BCLC. The Layer-3 baseline therefore uses AJCC pathologic stage; this
substitution is a known limitation of using public-data-only TCGA-LIHC for
an HCC stratification claim. Layer 1 was *not* informed of this
substitution; the operator made it at Layer 3 design time and records it
here.

## Sample sizes (informational, not preregistered)

- GSE14520: approximately 242 HCC tumour samples, OS data available.
- GSE76427: approximately 115 HCC tumour samples, OS data available.
- Pooled n approximately 357 with OS events. Power to detect ΔC-index =
  0.03 at alpha = 0.05 with the 1000-iteration bootstrap is approximately
  0.6 under pessimistic effect-correlation assumptions. Power is
  acknowledged as modest; under-powering is itself a discussion item in
  the case-study manuscript.

## After-action

The Layer-3 results are recorded in
`case-study/data/results/layer3_validation.json` with:

- primary outcome estimate and CI
- every secondary outcome estimate and CI
- every exploratory outcome estimate and CI, labelled exploratory
- the seed used for the bootstrap
- the version of the Layer-1 risk-score code that was being evaluated

The Layer-3 commit message references this preregistration commit by SHA.
