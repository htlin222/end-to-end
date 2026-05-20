# Round 1 — Methods Reviewer

**Round**: 01
**Reviewer**: Methods (per `prompts/03-reviewer-methods.md`)
**Date**: 2026-05-21
**Reviewed artefacts**: `case-study/manuscript/main.tex`,
`case-study/analysis/01_prepare_data.py`,
`case-study/analysis/02_build_risk_score.py`,
`case-study/analysis/03_subgroup_and_robustness.py`,
`case-study/analysis/04_figures.py`, `case-study/docs/prereg.md`,
`case-study/docs/prereg-v2.md`, `case-study/docs/prereg-v3.md`,
`case-study/docs/failure-mode-{01,02,03}-*.md`,
`case-study/data/results/tcga_bootstrap_metrics.json`.

## Overall impression

The manuscript clearly preregisters the analytic design (with three
documented amendments), follows the Harrell-Lee-Mark optimism-correction
protocol, and uses a vectorised univariable Cox score-test screen
followed by L1-penalised Cox. The pipeline refits **inside** the
bootstrap (not just the final Cox), which is the right thing and a
common point of weakness in transcriptomic-signature papers. The
external cohort GSE10143 is reported transparently as a null result
under the prespecified direction-definition. The honest reporting of
the L7 permutation-null failure mode (965/1000 screen-zero iterations)
is unusual and welcome.

That said, this is a draft and several methodological items need
attention before I would sign off on `accept`.

## Comments

### Comment 1 [HIGH] — Standardisation leakage across train/test in optimism-corrected bootstrap

The bootstrap loop in `_bootstrap_optimism` refits the univariable
screen and the L1-penalised Cox on each bootstrap sample, which is
correct. **However**, when applying the bootstrap-fitted model back to
the **original** sample (the optimism step), the standardisation
parameters `mu_b, sd_b` are computed on the bootstrap sample
(`expr_b.loc[genes_b].mean/std`) and then used to standardise the
original sample's expression for the gene set `genes_b`. This is the
intended behaviour for the optimism step, but the manuscript text in
the Methods section ("Standardise (z-score) per gene") does not say
explicitly **where** the standardisation parameters come from on each
fold. I want this stated unambiguously in the Methods, with one
sentence on the bootstrap-vs-apparent standardisation contract.

Severity: high. Required: one-paragraph Methods note. Suggested
wording: "Per-gene standardisation parameters $\mu_g, \sigma_g$ are
computed on the bootstrap sample only; the same parameters are then
used to standardise the original sample's expression matrix before
applying the bootstrap-fitted Cox coefficients."

### Comment 2 [HIGH] — Apparent ΔC computed once on full data, but optimism averages a different quantity

In `_bootstrap_optimism`, `delta_c_apparent` is computed once on the
full sample (lines after the apparent fit). The bootstrap loop, in
contrast, records `delta_c_boot.append(c_combo_b - c_apparent_ajcc)`
where `c_combo_b` is the C-index of the **bootstrap-fitted** AJCC+TRS
combo evaluated on the original sample and `c_apparent_ajcc` is the
**apparent** AJCC-alone C-index. That mixes two estimators in one
quantity: the bootstrap distribution of `c_combo_b - c_apparent_ajcc`
is **not** the bootstrap distribution of `delta_c` in the standard
Harrell-Lee-Mark sense, which would be `c_combo_b - c_ajcc_b`
(bootstrap-refit AJCC-alone on the bootstrap sample, evaluated on the
original). The CI you report is therefore narrower than it should be.

Severity: high. Required: rerun the bootstrap with `c_ajcc_b - c_ajcc_orig`
properly tracked, OR explicitly defend the reported CI as a "ΔC of
TRS contribution holding AJCC apparent estimate fixed" quantity (with
a Methods-section caveat).

### Comment 3 [MEDIUM] — Univariable score-test screen vs Cox MLE: justify the equivalence

The script `_univariable_screen` uses a Cox partial-likelihood
**score test** instead of fitting MLE Cox per gene. The rationale
(speed) is sound, but the **score test** and the **likelihood-ratio
or Wald test** of a fitted Cox can disagree at marginal genes,
especially when ties are present (TCGA-LIHC has ties at days_to_event
because dates were measured in days). The Wald/MLE Cox is what the
Hoshida 2008 paper and most HCC signature papers used. Either:

(a) Re-run the screen with `CoxPHFitter` MLE and confirm the same 50
genes are selected; or
(b) Add a sentence to Methods stating that the score test is
asymptotically equivalent under H0 and document that you spot-checked
agreement on a 50-gene sample.

Severity: medium. Required: one of (a) or (b).

### Comment 4 [MEDIUM] — Stability of the 50-gene set across bootstrap iterations

The manuscript reports the **apparent** 50-gene signature. The
honest stability check is "what fraction of the apparent 50 genes
survive in each bootstrap iteration's 50-gene set?" — i.e., the
Steyerberg-style stability of the feature selection. This is a one-
line addition to the bootstrap loop and a one-sentence Methods note;
without it, the reader cannot know whether the apparent signature is
fold-dependent.

Severity: medium. Required: report median Jaccard overlap of bootstrap
gene sets vs apparent, and median bootstrap signature size.

### Comment 5 [MEDIUM] — Multiple-testing family does not include the primary outcome

The prereg states the seven secondaries (L1-L7) are the Bonferroni
family. The primary outcome (optimism-corrected ΔC-index) is excluded
from correction "as the single confirmatory test". Convention in
TRIPOD-aligned reporting is to either (a) include the primary in the
family, or (b) explicitly state the rationale for excluding it.

Currently the Methods do (b) implicitly. State it explicitly in one
sentence: "The primary outcome is the single confirmatory test; the
seven secondaries are the Bonferroni-correction family."

Severity: medium. Required: one sentence in Methods §2.7 (Secondary
outcomes).

### Comment 6 [MEDIUM] — Sample-rule documentation: one sample per case rule

`_prep_tcga` collapses multiple primary-tumour aliquots per case to
the lexicographic-minimum sample submitter id. This is a defensible
deterministic choice, but the manuscript Methods does not say "one
sample per case, chosen by lexicographic-minimum sample id". This is
a TRIPOD reporting requirement (sample-selection rule). Add it.

Severity: medium.

### Comment 7 [LOW] — Calibration slope of 0.70 in the apparent fit

The Methods reports calibration slope = 0.70 (against ideal = 1.0).
This is consistent with mild over-fit at the apparent fit. The
manuscript text correctly notes that the optimism-corrected primary
endpoint mitigates this. **However**, a recalibrated score (intercept-
plus-slope re-estimated on a held-out fold) would give a more
informative calibration claim. The 5-fold CV results in
`cv_metrics.json` are present; report calibration slope from CV too.

Severity: low. Optional but improves the manuscript.

### Comment 8 [LOW] — TCGA-LIHC clinical-attribute ambiguity at the diagnoses[] level

`_gdc_clinical_via_api` selects the diagnosis row whose
`ajcc_pathologic_stage` is non-null preferentially. This is defensible
but worth noting in the Methods (one sentence): "Where TCGA recorded
multiple diagnoses rows per case (typically primary plus recurrence),
the stage-bearing diagnosis was retained."

Severity: low.

### Comment 9 [LOW] — Reproducibility statement: pin uv lock or pip freeze

The Methods says "all versions pinned in `uv.lock`". Confirm that the
`uv.lock` file is committed at the case-study-v1.0.0 tag and that the
manuscript explicitly references it. (I see lifelines 0.30.3 mentioned;
that's the right idea, but TRIPOD requires a stronger statement.)

Severity: low.

## Verdict

**`major-revision`**.

The Comment-2 issue (the bootstrap ΔC distribution is not the standard
Harrell-Lee-Mark statistic) requires a real reanalysis or a documented
defence. Comment 1 (standardisation contract in the optimism step) is
required for the Methods to be reproducible by a Layer-2 audit.
Comments 3-9 are individually low-to-medium severity but together
they affect TRIPOD compliance.

I would gladly recommend `accept` after these are addressed.
