# Round 1 — Biostatistics Reviewer

**Round**: 01
**Reviewer**: Biostatistics (per `prompts/03-reviewer-biostat.md`)
**Date**: 2026-05-21
**Reviewed artefacts**: `case-study/manuscript/main.tex`,
`case-study/data/results/tcga_bootstrap_metrics.json`,
`case-study/data/results/robustness_metrics.json`,
`case-study/data/results/cv_metrics.json`,
`case-study/analysis/02_build_risk_score.py`.

## Overall impression

The headline statistical machinery is mostly defensible: Cox model
with L1 penalty, 1000-iteration optimism-corrected bootstrap, score-
test screen with BH-FDR. The Schoenfeld test was reported.
Permutation null is honestly reported as underpowered against
apparent statistics. **However**, several TRIPOD-aligned items are
missing or wrongly computed.

## Comments

### Comment 1 [BLOCKER] — Harrell vs Uno's C-index distinction not stated

The manuscript says "Harrell's C-index" but `lifelines.utils.
concordance_index` is **Harrell's C** with default tie-handling. Two
issues:

(a) Harrell's C is known to be biased upward under censoring; Uno's
C-statistic (Uno 2011) is the modern alternative for prediction
models. The choice should be stated and defended.
(b) The manuscript writes `concordance_index(t, -score, e)`. The
negative sign on the score is correct for "high score = high risk =
shorter survival", but the convention should be stated explicitly in
the Methods.

Severity: blocker. Required: name the C-statistic used; note the bias
direction; consider reporting Uno's C as a sensitivity analysis. Add
one paragraph.

### Comment 2 [BLOCKER] — Calibration plot at fixed landmarks is required

The manuscript reports a single "calibration slope" of 0.70 from a
univariable Cox of standardised score on OS. This is **not** a
calibration plot. TRIPOD-aligned reporting for a prognostic model
requires a calibration plot at fixed landmark times (1, 3, 5 years
in this case) showing predicted vs observed survival probability in
deciles or quintiles, with the Hosmer-Lemeshow chi-square at each
landmark.

The Layer-3 prereg (`docs/prereg.md` S3/S4/S5) requires Hosmer-Lemeshow
deciles at the same landmarks. The Layer-1 manuscript should follow
the same protocol for its own development cohort.

Severity: blocker. Required: a calibration plot panel in Figure 3 (or
a new Figure 5), with HL p at 1, 3, 5 y.

### Comment 3 [HIGH] — Sample size and power for the apparent ΔC=0.12 claim

The Layer-1 prereg threshold is corrected ΔC >= 0.02. The achieved
estimate is 0.060 with CI [0.085, 0.137]. The reported sample size of
n=366 with 130 events gives ~ 90% power to detect a true delta-C of
0.05 at alpha 0.05, per Pencina & D'Agostino's formula. State the
power calculation in the Methods. The reported CI is appropriately
wide; that's fine.

Severity: high. Required: one-paragraph power statement in Methods,
referencing the formula.

### Comment 4 [HIGH] — Bootstrap optimism CI: methodological clarification

The reported CI for ΔC is the percentile-based CI of the bootstrap
distribution of `c_combo_b - c_apparent_ajcc`. As the methods reviewer
notes (Comment 2 in `methods.md`), this is **not** the standard
Harrell-Lee-Mark estimator. The strict TRIPOD interpretation would
report ΔC_corrected = ΔC_apparent - mean(optimism_combo - optimism_ajcc),
and the CI would be the percentile of (ΔC_apparent - optimism) across
bootstrap iterations. As-is, the CI underestimates uncertainty.

Severity: high. Required: re-run with the correct paired-optimism
formula, OR document the deviation transparently in Methods.

### Comment 5 [HIGH] — Schoenfeld global test: only one covariate reported

The manuscript reports Schoenfeld p for the HCC-TRS covariate (p=0.38).
`robustness_metrics.json` shows the **stage** covariate has Schoenfeld
p=0.034, suggesting non-proportional hazards for AJCC stage in the
stage-adjusted model. This is a clinically relevant finding (HCC
stage's hazard ratio changes over time as advanced-stage patients die
early then plateau) and should be reported in the Results, with a
sensitivity analysis using a stratified Cox or a time-varying coefficient
for stage.

Severity: high.

### Comment 6 [MEDIUM] — Bonferroni correction across seven secondaries: state which ones pass

The prereg's Bonferroni threshold is 0.05/7 = 0.0071. The Results
section should explicitly say which of L1-L7 are significant after
correction. Quick tally from the metrics file:

- L1: p = 2.4e-14 → passes
- L2: p = 0.13 → fails
- L3: AUCs, no formal test
- L4: calibration slope, no formal test
- L5: p = 0.38 → fails (but this is desirable for PH; rewording needed)
- L6: C-index point estimate + CI, no formal test
- L7: p = 0.018 → does NOT pass corrected (passes uncorrected)

State this in the Results.

Severity: medium.

### Comment 7 [MEDIUM] — Competing-risks treatment: Fine-Gray as sensitivity

For HCC, transplant and non-cancer death are competing events. The
Methods uses any-cause OS. A Fine-Gray sub-distribution hazards
sensitivity analysis (with cancer-specific death as event, transplant
as competing) would address this. If not feasible (no cancer-specific
death flag in TCGA), state so explicitly.

Severity: medium.

### Comment 8 [MEDIUM] — IDI / NRI in addition to ΔC-index

For prognostic-model additive claims ("AJCC + TRS > AJCC alone"),
Pencina IDI (integrated discrimination improvement) is the
complementary statistic and is required for TRIPOD-aligned reporting.
Layer-3 prereg S7 specifies IDI. Layer-1 should report it on TCGA.

Severity: medium.

### Comment 9 [LOW] — RGB tie handling in the score test

The vectorised score test computes cumulative sums after sorting by
descending time. If multiple events occur at the same time
(tied-event), the standard partial-likelihood treats ties by Efron's
or Breslow's correction. The script's implementation does not
distinguish — implicit Breslow. State this; ties exist in TCGA-LIHC
(several events on the same recorded day). Either:

(a) Document Breslow tie handling, OR
(b) Re-run with Efron and confirm no material change.

Severity: low.

### Comment 10 [LOW] — Bootstrap seed and resume-from-checkpoint

The seed is 20260521 and is stated. Reasonable. Mention that the
bootstrap RNG is `np.random.default_rng(seed)`, which is the modern
PCG64 generator (deterministic across NumPy versions).

Severity: low.

## Verdict

**`major-revision`**.

Comments 1-2 (Harrell-vs-Uno disclosure; calibration plot) are
blockers because a TRIPOD-compliant prognostic-model paper cannot be
submitted without an explicit calibration plot at landmarks and a
named C-statistic. Comments 3-5 are high-severity and re-doable
within a revision cycle.
