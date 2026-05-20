# Layer-1 Session Plan

**Authored by**: Layer-1 autonomous Claude Code session (Opus 4.7, 1M
context). Snapshot date 2026-05-20 (kickoff). This file is committed
before any analytic code runs and is *not* edited retroactively; later
plan revisions are appended as `session-plan-revision-NN.md`.

## Mandate recap

Domain: refine HCC overall-survival stratification beyond AJCC pathologic
stage using TCGA-LIHC plus one non-reserved GEO cohort.

Hard exclusions: GSE14520 and GSE76427 are reserved for Layer 3.

## Sub-claim (committed before code runs)

> A transcriptome-derived **HCC overall-survival risk score (HCC-TRS)**
> derived from TCGA-LIHC primary HCC tumours, when added to AJCC
> pathologic stage as an additive covariate in a Cox proportional-hazards
> model, improves Harrell's C-index for overall survival relative to AJCC
> pathologic stage alone, **and** the improvement reproduces under
> 1000-iteration case-bootstrap with re-fitting in TCGA-LIHC, **and** the
> ranking direction reproduces in one non-reserved GEO cohort that
> reports overall survival.

The Layer-1 primary endpoint is therefore the *internal* ΔC-index of
"AJCC + HCC-TRS" minus "AJCC alone", evaluated by 1000-iteration optimism-
corrected bootstrap on TCGA-LIHC and externally reproduced (direction +
log-rank stratified test) in one non-reserved GEO cohort.

The Layer-3 ΔC-index against GSE14520 / GSE76427 remains the
operator's confirmatory test under `docs/prereg.md` and is *not*
something Layer 1 evaluates.

## Statistical method (committed before code runs)

1. **Feature universe**: protein-coding genes expressed in >= 50% of
   TCGA-LIHC primary tumour samples at TPM >= 1. (Hard-coded; not
   tuned.)
2. **Univariable screen**: within the training fold only, fit
   univariable Cox per gene against OS, retain genes with FDR-BH
   adjusted p < 0.05 in the training fold.
3. **Multivariable model**: penalised Cox regression (L1, glmnet-style
   via scikit-survival or lifelines + sklearn `CoxnetSurvivalAnalysis`
   if scikit-survival is installable; otherwise lifelines' Cox with L2
   penaliser plus a forward-selection wrapper). Penalty `lambda`
   selected by 5-fold CV inside the training fold.
4. **Risk score**: linear predictor `r_i = X_i^T beta_hat`. Score is
   computed in any held-out sample using the same gene list and
   coefficients.
5. **Internal validation**: 1000-iteration case-bootstrap, refit the
   *entire* feature-selection + model-fit pipeline on each bootstrap
   sample, evaluate on the out-of-bag sample. Report optimism-corrected
   C-index per Harrell.
6. **External (within Layer 1) validation**: apply locked TCGA-LIHC
   coefficients (or a re-fit on locked TCGA-LIHC gene set) to the
   non-reserved GEO cohort. Report C-index and stratified log-rank
   between HCC-TRS high vs low (median split, prespecified).

Tooling choice: Python (lifelines + scikit-survival if available;
sklearn for CV; statsmodels for diagnostic tests).

## Choice of non-reserved GEO cohort (committed before download)

Allowed candidates per Layer-1 mandate (>80 samples, OS data): GSE54236,
GSE36376, GSE57957, GSE63898, GSE39791.

**Selection rule, prespecified**: I will check, in this order, whether
each cohort meets all of (a) total tumour samples >= 80; (b) overall-
survival time and event status available in either the GEO Series Matrix
or a companion publication's supplement; (c) microarray expression data
on at least 10000 protein-coding genes that overlap our TCGA TPM
feature set; (d) clinical fields include AJCC TNM stage or BCLC stage
for the baseline.

The first cohort that passes all four checks becomes the Layer-1
external cohort. Subsequent cohorts are *not* used for headline
analyses to avoid multi-cohort selection bias.

Result of the selection is recorded in
`case-study/data/results/cohort-selection.json` before any model is
fitted.

## Target journal

Working choice: **JCO Clinical Cancer Informatics** (JCO CCI). Rationale:
clinical-prediction submissions are in scope; word count tolerant of
methods detail; TRIPOD-aligned reporting requirements match the
analysis; reasonable acceptance probability for a single-author single-
cohort case study. Distilled into `case-study/manuscript/JOURNAL.md`
before the manuscript draft is started.

Alternative if scope-fit fails: *Briefings in Bioinformatics* (methods
emphasis) or *npj Precision Oncology* (clinical-translation emphasis).

## Deliverable schedule

1. Commit session plan, JOURNAL.md, case-study prereg, analysis stub.
2. Download TCGA-LIHC (GDC public API).
3. Choose non-reserved GEO cohort per the selection rule above.
4. Run `01_prepare_data.py` through `04_figures.py`.
5. Draft `case-study/manuscript/main.tex`.
6. Dispatch reviewer round 1 (four subagents).
7. Revise; iterate rounds 2-N until unanimous ACCEPT.
8. Tag `case-study-v1.0.0` locally.

## Failure modes anticipated

- TCGA-LIHC download size or rate-limit failures: documented and
  retried; if blocked, an alternative recount endpoint is used.
- GEO cohort lacks OS in the Series Matrix: fall back to companion
  supplement; if all candidates lack OS, record as a failure mode and
  proceed with internal-bootstrap-only Layer-1 evidence.
- L1-penalised Cox does not converge: fall back to univariable-screen
  + multivariable Cox without penalisation (clearly documented as a
  pivot).
- Proportional-hazards assumption violated for HCC-TRS: report
  Schoenfeld test; if violated, add a stratified Cox or a time-varying
  interaction term and report both.

## Out of scope for Layer 1

- GSE14520, GSE76427: reserved external-validation cohorts. Not read,
  not downloaded, no metadata inspection.
- Layer-2 audit: separate session.
- Layer-3 validation: operator step.
- Edits to `manuscript/`, `docs/`, top-level files: not permitted by
  the kickoff prompt.
