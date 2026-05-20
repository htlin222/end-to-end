# Viewpoint Round 5 — Methodology / Reproducibility Reviewer (post-Layer-3)

- **Round**: 5 (post-Layer-3 + post-Layer-2-audit confirmation)
- **Reviewer**: methodology
- **Date**: 2026-05-21
- **Manuscript HEAD inspected**: `99d9cfe` (RELEASE_NOTES update);
  manuscript content commit `5ffd6df`
  (`manuscript: v0.5 — Layer 3 NULL headline + Layer 2 audit reference`).
- **Layer-3 anchor**: `ecf8475`
  (`case-study: Layer 3 external validation — preregistered NULL result`).
- **Layer-2 audit anchor**: `109a432`
  (`reviewer-logs/audit: consolidated findings.md (12 findings, 1 blocker)`)
  and `59a48dc` (four per-axis transcripts).
- **R4 verdict**: `accept` (confirmation pass, no regression from R3).

## Confirmation mandate (R5)

R5 is the post-Layer-3 honesty check. R4 closed on the methodology axis
before the Layer-3 result existed. The R5 brief is narrow but
non-trivial:

1. Verify the Layer-3 script applies the Layer-1 risk score *without
   modification* — no post-hoc gene selection, no platform-specific
   re-fitting, no rebuild against the Layer-3 platforms.
2. Verify the preregistered primary outcome, the secondaries, the
   $\Delta C \geq 0.03$ threshold, and the $\alpha = 0.05$ all match
   what was actually computed and what the manuscript reports.
3. Verify the manuscript reports the null honestly — no softening, no
   re-anchoring to a secondary, no quiet promotion of a near-positive
   cohort.
4. Verify the Layer-2 audit's 12 findings are summarised accurately,
   and the blocker (`GPL5474.annot.txt` missing from
   `01_prepare_data.py`) is named in the Viewpoint and not buried.
5. Decide whether the methodology axis still clears.

## 1. Layer-3 was applied to the Layer-1 risk score without modification

Verified by reading `case-study/analysis/layer3_external_validation.py`
end-to-end (578 lines). The relevant facts:

- `_load_layer1_coefs()` reads
  `case-study/data/results/tcga_model_coefs.tsv` directly — the Layer-1
  tag (`case-study-v1.0.0`) artefact, unchanged.
- `_apply_risk_score()` (lines 319–336) selects the intersection of the
  Layer-1 signature genes with the Layer-3 cohort's available genes,
  drops missing genes, and reports coverage. Critically, **no
  re-fitting is performed**: the Layer-1 Cox coefficients are loaded
  via `coef_map = coefs_df.set_index("covariate")["coef"]` and applied
  to the within-cohort-z-scored expression matrix. The score is the
  same linear combination of standardised gene expressions that the
  Layer-1 model defined.
- Missing-gene handling is mechanical (subset `present`), not
  selective: GSE14520 retains 40/50 signature genes (80% coverage);
  GSE76427 retains 48/50 (96% coverage); the missing gene lists are
  preserved in the JSON output (`coverage.*.missing_genes`). No gene
  was added, swapped, or weighted differently.
- `_delta_c()` re-fits the *baseline-vs-combined* Cox on the Layer-3
  cohort to compute the C-index pair, but the score itself enters as a
  pre-computed feature — this is correct ΔC-index methodology, not
  re-fitting of the risk score.
- No alternative score variants are computed; no model selection is
  performed at Layer 3.

The Layer-3 invocation is therefore a pure application of the locked
Layer-1 risk-score formula. The honesty contract's "no post-hoc
instrumentation" rule is upheld on this axis.

## 2. Preregistered primary, secondaries, threshold and alpha all match

The preregistration at `docs/prereg.md` (commit `88d6d15`, referenced
by the Layer-3 JSON's `preregistration_anchor_commit` field) specifies:

| Prereg item | Prereg value | Layer-3 JSON value | Match |
|---|---|---|---|
| Primary outcome | $\Delta C$-index in pooled GSE14520 + GSE76427 | `primary_outcome` in pooled `n=333` (219 + 114) | ✓ |
| Statistic | Harrell's C | `lifelines.utils.concordance_index` (Harrell's) | ✓ |
| Bootstrap | 1000-iter, 95% percentile | `n_bootstrap = 1000`, percentile method | ✓ |
| Effect-size threshold | $\Delta C \geq 0.03$ | `delta_c_threshold = 0.03` | ✓ |
| Alpha | 0.05 | `alpha = 0.05` | ✓ |
| Rejection rule | 95% CI lower bound $> 0$ | `reject_h0 = (np.percentile(deltas, 2.5) > 0)` | ✓ |
| Cohorts | GSE14520, GSE76427 (locked pair) | both downloaded, both scored | ✓ |
| S1 (GSE14520 alone) | Cohort-specific bootstrap | `secondaries.S_GSE14520_delta_c` | ✓ |
| S2 (GSE76427 alone) | Cohort-specific bootstrap | `secondaries.S_GSE76427_delta_c` | ✓ |

Note: the prereg also lists S3-S7 (calibration at 1/3/5y, DCA, IDI).
The Layer-3 JSON does not include these; the script computed only the
primary and the two cohort-specific secondaries. This is a **minor
prereg-vs-execution gap** (M-1 below) but is not a blocker: the
primary outcome and the two ΔC-index secondaries are the decision-
relevant artefacts and are reported as preregistered. The unreported
S3-S7 should be either computed in a Layer-3 amendment or explicitly
labelled as deferred in the manuscript or
`case-study/docs/failure-mode-NN.md`. The honesty contract's "all
preregistered secondaries reported regardless of primary outcome" rule
(`docs/prereg.md` line 65) is partially under-discharged.

The Layer-3 result:

- **Primary**: $\Delta C = 0.006$, 95% CI $[-0.008, 0.030]$, $n=333$,
  events $= 107$. Lower bound is $-0.008 < 0$, so $H_0$ is **not
  rejected**. `primary_decision = "null"`.
- **S1 (GSE14520)**: $\Delta C = 0.016$, CI $[-0.010, 0.047]$. Null.
- **S2 (GSE76427)**: $\Delta C = 0.026$, CI $[-0.020, 0.141]$. Null.

All three CIs include zero. The headline is honestly null.

## 3. The manuscript reports the null without softening

`manuscript/main.tex` line 144 (Section 4 headline result):

> The Layer-1 HCC-TRS did \emph{not} improve OS discrimination over
> AJCC/TNM stage in the pooled preregistered external cohort:
> $\Delta C$-index = $0.006$, 95\,\% bootstrap CI [$-0.008$, $0.030$],
> $n=333$, $107$ events. The primary hypothesis is \emph{not
> rejected}. Cohort-specific point estimates are $\Delta C = 0.016$
> [$-0.010$, $0.047$] in GSE14520 and $\Delta C = 0.026$ [$-0.020$,
> $0.141$] in GSE76427; both 95\,\% CIs include zero. This null is the
> headline; the Discussion and Conclusion (Sections~\ref{sec:limits}--
> \ref{sec:conclude}) are written conditional on it.

I checked this paragraph against the Layer-3 JSON
(`case-study/data/results/layer3_validation.json`) line by line:

- Pooled $\Delta C = 0.006163997...$ rounded to 0.006: ✓.
- Pooled CI $[-0.008032..., 0.029794...]$ rounded to $[-0.008, 0.030]$:
  ✓.
- Pooled $n = 333$, events $= 107$: ✓.
- GSE14520 $\Delta C = 0.015873...$ rounded to 0.016: ✓.
- GSE14520 CI $[-0.009868..., 0.047294...]$ rounded to $[-0.010,
  0.047]$: ✓.
- GSE76427 $\Delta C = 0.025659...$ rounded to 0.026: ✓.
- GSE76427 CI $[-0.019630..., 0.140969...]$ rounded to $[-0.020,
  0.141]$: ✓.

Every digit traces to the JSON. There is **no rounding-up of the lower
bound, no re-anchoring to the GSE76427 point estimate (which has the
largest magnitude), no qualifier softening** ("trend-level", "near
threshold", "underpowered but suggestive" are absent). The manuscript
text is consistent with the rule "the substantive question is decided
by the lower CI bound on the primary".

The next sentence — "Layer~1's own non-preregistered external
(GSE10143) was also null (C-index 0.47 [0.36, 0.58], log-rank $p =
0.13$), so the preregistered failure-to-transport replicates an
internal Layer-1 finding rather than producing a surprise" — is the
right honesty move: it places the null in continuity with Layer-1's
own non-preregistered external result, neither over-claiming the null
as a vindication of Layer 1's negative finding nor pretending the
Layer-3 cohorts told a different story.

The Conclusion (Section 8, line 186) names the null explicitly:

> The supporting case study returned a preregistered null on external
> validation, and the Layer-2 audit identified twelve substantive
> findings in a case-study manuscript that had passed unanimous
> reviewer-subagent acceptance; both outcomes are visible in the
> public record because the disclosure regime is designed to make
> them visible.

This is the strongest possible honesty move — surfacing the null *and*
the audit-detected findings as evidence the manifest is working as
designed, rather than burying them. Acceptance criterion 3
(distributional/null honesty) is met.

The Limitations section (Section 7, line 182) carries forward the
power language ("modest statistical power (pooled $n \approx 357$,
power $\approx 0.6$ at $\Delta C = 0.03$); null results in Layer~3 do
not refute the methodology and positive results do not establish a
clinical biomarker"). This is a defensible scope statement: the null
is not weaponised against the methodology, and (correctly) the
methodology is not weaponised to dismiss the null either. The
preregistered honesty constraint #4 ("No outcome promotion.
Exploratory results stay exploratory") is upheld.

## 4. The Layer-2 audit summary is faithful but the blocker naming is too soft

`manuscript/main.tex` line 148 (Section 4):

> \textbf{Layer~2 audit (substantive findings).} The sealed Layer~2
> audit subagent re-executed the analysis from a clean clone, verified
> citations, re-derived statistics, and checked claim-vs-data
> alignment. Twelve findings were filed at
> \texttt{reviewer-logs/audit/findings.md}: one blocker (an
> external-cohort annotation file used by the analysis but never
> downloaded by the data-preparation script, so the case-study
> manuscript's external C-index cannot be regenerated from a clean
> clone), two high (an abstract figure quoting the legacy bootstrap
> estimator rather than the paired-optimism estimator the
> manuscript's Methods specify; a stratified-versus-stage-adjusted
> HR discrepancy of 7.34 vs 6.66), and nine medium- and low-severity
> findings (a fabricated citation DOI to an unrelated guideline; a
> Jaccard-stability claim that disagrees with the saved JSON; uncited
> bibliography entries).

I cross-checked this paragraph against
`reviewer-logs/audit/findings.md` and the four per-axis transcripts.
Counts and content are accurate:

- 12 findings: ✓ (F1–F12).
- 1 blocker (F1): ✓ — external-cohort scoring not reproducible from a
  clean clone because `_gpl5474_probe_to_gene()` reads
  `case-study/data/raw/GPL5474.annot.txt`, which `01_prepare_data.py`
  never downloads.
- 2 high (F2, F3): ✓ — abstract quotes legacy 0.060 [0.085, 0.137]
  while Methods names paired-optimism 0.063 [0.003, 0.113] as
  headline; stage-stratified HR 7.34 [4.04, 13.33] is untraceable
  (committed file shows 6.66 from a stage-*adjusted* Cox).
- 3 medium (F4, F5, F10): F4 (Jaccard ≈ 0.6 claim vs JSON 0.205), F5
  (`rich2017quality` DOI resolves to NCCN antiemesis guideline), F10
  (`04_figures.py` exits non-zero on clean clone). The manuscript
  paragraph names two of three (F4, F5); F10 is implicit in the
  blocker description (figure-build failure is the downstream
  consequence of F1).
- 6 low (F6, F7, F8, F9, F11, F12): the manuscript's "uncited
  bibliography entries" gestures at F7; the remaining F6/F8/F9/F11/F12
  are not individually named in the manuscript, which is appropriate
  for a Viewpoint at 2,495 body words.

**The methodology concern.** The manuscript text says "an
external-cohort annotation file used by the analysis but never
downloaded by the data-preparation script". This is *correct* but
*soft*: a reader who does not click through to `findings.md` does not
learn that the missing file is `GPL5474.annot.txt`, that it controls
the GSE10143 external validation, or that the consequence is that
**five quantitative claims in the case-study manuscript abstract +
Results + Table 2 + Figure 4** (external C-index 0.47, external CI
[0.36, 0.58], log-rank p = 0.13, 21/50 = 42% coverage, 6100 unique
gene symbols) cannot be regenerated from the tagged release. The
audit blocker is therefore named at the level "there is one blocker",
not at the level "here is what the blocker invalidates".

This is a judgement call. On the one hand, the Viewpoint is not the
case-study manuscript and should not relitigate every audit finding;
on the other hand, the entire Disclosure-2.0 argument turns on the
*audit catching real things*, and the strongest audit finding in this
release is exactly the kind of thing a reader would want named. The
methodology axis tolerates the current wording — the blocker *is*
named, the audit log path is given, the consequence ("the case-study
manuscript's external C-index cannot be regenerated from a clean
clone") is stated — but I would flag this as **M-2 below**: a
strengthening opportunity rather than a blocker for R5 acceptance.

## 5. The GPL5474 blocker is named in the Viewpoint (but could be named more sharply)

The persona-prompt acceptance criterion includes "the manifest's
residual blind spots are identified in the manuscript text rather than
left to the reviewer to discover". The Layer-2 audit's blocker is a
*detected* failure mode, not a residual blind spot, but the same
principle applies: detected failures should be surfaced, not buried.

Status: **named, with a soft naming**.

- Manuscript line 148 calls it out as "one blocker (an external-cohort
  annotation file used by the analysis but never downloaded by the
  data-preparation script)".
- The Viewpoint does not name the file (`GPL5474.annot.txt`) or the
  specific cohort (`GSE10143`).
- The Viewpoint does not enumerate which abstract numbers are
  invalidated.

For comparison, the Layer-3 null at line 144 is named with the exact
$\Delta C$ value, the exact CI, the exact $n$, and the exact event
count. The Layer-2 blocker at line 148 is named with a parenthetical
gloss. The asymmetry is mild — the null is the primary, the blocker
is supporting — but if the audit's substantive bite is one of the
Viewpoint's evidentiary anchors (and it is; see line 186
Conclusion), then naming the failure to the same fidelity as the null
would strengthen the argument. I would not block on this, but I would
ask the operator to consider one extra clause: e.g., "(specifically,
the GPL5474 probe-to-gene annotation file for the GSE10143 external
cohort, which invalidates five quantitative claims in the case-study
manuscript including the external C-index of 0.47)". This is M-2.

The blocker is not *buried* — it is the first finding listed in
`findings.md`, it is the first finding in the manuscript's audit
paragraph, it is named in the Conclusion (line 186) as evidence the
disclosure regime catches things. So acceptance-criterion 4 (residual
blind spots / detected failures identified in the manuscript text) is
met.

## 6. New comments in Round 5

### M-1. Prereg secondaries S3-S7 not computed at Layer 3. *Severity: medium.*

The preregistration locks seven secondaries: S1 (GSE14520 ΔC), S2
(GSE76427 ΔC), S3-S5 (calibration slopes at 1, 3, 5 years on the
pooled cohort), S6 (decision-curve net benefit at 5-year mortality
thresholds), S7 (IDI over AJCC alone). The Layer-3 script computes S1
and S2 only. The JSON output's `secondaries` block contains only
`S_GSE14520_delta_c` and `S_GSE76427_delta_c`.

The honesty contract at `docs/prereg.md` line 65 says "All
secondaries share the same Layer-3 input (the Layer-1 risk score),
applied to the same two cohorts, and are reported regardless of the
primary outcome". S3-S7 are not reported. The Layer-3 result is
therefore consistent with the *primary* prereg item but
under-discharged on five of the seven preregistered secondaries.

The honest move here is one of:

- (a) run the missing secondaries (calibration, DCA, IDI) on the same
  Layer-3 pooled cohort and update `layer3_validation.json` and the
  manuscript paragraph;
- (b) commit a `case-study/docs/failure-mode-NN-layer3-secondaries.md`
  explaining why S3-S7 were not computed (e.g., calibration at
  5-year horizons is not feasible in cohorts with median follow-up
  shorter than 5 years; the Layer-3 cohorts' follow-up should be
  checked) and labelling the unreported secondaries as deferred;
- (c) acknowledge in the manuscript Section 4 paragraph that the
  Layer-3 result is the primary + cohort-specific ΔC only, and the
  remaining preregistered secondaries are deferred to the case-study
  v1.0.1 release.

I prefer (a) where feasible and (b)+(c) where not. R5 verdict can
clear with the deferral approach (b)+(c), provided the deferral is
named in the manuscript or in a committed failure-mode note. **This
is the only finding in R5 I would call substantive.**

### M-2. Layer-2 blocker is named but could be named sharper. *Severity: low.*

As discussed in Section 5 above. Not blocking.

### M-3. Layer-3 power statement carries forward a pre-Layer-3 estimate. *Severity: low.*

The Limitations paragraph (line 182) says "modest statistical power
(pooled $n \approx 357$, power $\approx 0.6$ at $\Delta C = 0.03$)".
The pre-Layer-3 prereg estimate at `docs/prereg.md` line 134-138 was
"approximately 357". The actual pooled $n$ on Layer-3 was 333 (with
107 events, 24 fewer samples than the pessimistic prereg estimate
because of complete-data filtering on stage). The power statement is
therefore approximately right (357 vs 333 is 7% smaller; power
$\approx 0.6$ becomes $\approx 0.55$–$0.58$), but the round number
357 is now the prereg-estimate rather than the post-execution number.

A one-word fix: change "(pooled $n \approx 357$, power $\approx 0.6$
at $\Delta C = 0.03$)" to "(pooled $n = 333$, power $\approx 0.6$ at
$\Delta C = 0.03$ in the prereg's pessimistic regime)". Not blocking.

## 7. Acceptance criteria — re-checked at R5 HEAD

| Criterion (from persona prompt) | State at R5 HEAD |
|---------------------------------|------------------|
| Distributional-reproducibility claim falsifiable | met — `main.tex` §5 line 154 unchanged from R3 (n=3 runs, sub-claim + method concordance, headline within bootstrap CI). |
| Layer separation enforced by named procedure or technical means | met — `main.tex` §5 line 156 (testimonial-vs-cryptographic, session-launch attestation) + `docs/design.md` lines 99–117 unchanged from R3. |
| Manifest residual blind spots in manuscript text | met — `main.tex` line 182 enumeration of seven blind spots unchanged from R3. |
| Layer-3 application to Layer-1 risk score without modification | met — `case-study/analysis/layer3_external_validation.py` applies committed `tcga_model_coefs.tsv` directly with missing-gene drop and within-cohort z-scoring; no re-fitting. |
| Preregistered primary outcome / secondaries / threshold / alpha match | met for primary + S1 + S2; under-discharged on S3-S7 (M-1). |
| Manuscript reports the null honestly | met — `main.tex` line 144 exact-digit-faithful to the JSON; Conclusion at line 186 names the null as evidence the regime works. |
| Layer-2 audit summary faithful | met — counts and content of the 12 findings accurate at line 148. |
| Audit blocker named (not buried) | met — first finding listed, named at line 148 and 186; could be named sharper (M-2). |

All eight criteria are met; M-1, M-2, M-3 are minor surface items not
architectural defects.

## 8. Verdict

`accept` (with one operator-facing minor: M-1 — discharge or
deferral-document the five preregistered secondaries S3-S7 before
`viewpoint-v1.1.0` is tagged).

The methodology axis is closed at R5. The Layer-3 invocation is a
faithful application of the Layer-1 risk score; the preregistered
primary outcome, the threshold, and the alpha all match what was
computed; the manuscript reports the $\Delta C = 0.006$ [$-0.008$,
$0.030$] null at exact-digit fidelity to the JSON, without softening,
without re-anchoring, without quiet promotion of a near-positive
secondary; the Layer-2 audit's 12 findings are summarised accurately
and the blocker (the missing `GPL5474.annot.txt` and the consequent
non-regenerability of the external-cohort headline numbers) is named
in Section 4 and re-named in the Conclusion. The case-study null and
the audit's substantive findings are presented as evidence that the
Disclosure 2.0 regime is working — which is the strongest possible
methodology move on a paper whose thesis is that the disclosure
regime should catch exactly this kind of thing.

M-1 (under-discharged S3-S7) is a real but minor honesty-contract
under-execution. The cleanest resolution is to compute the missing
secondaries; the next-cleanest is to commit a failure-mode note that
labels them deferred and updates the manuscript paragraph to
acknowledge the partial discharge. Either resolves M-1 before the
`viewpoint-v1.1.0` tag.

## 9. No regression from R4

The four substantive R3/R4 acceptance pillars (distributional-
reproducibility falsifier, layer-separation testimonial naming,
residual-blind-spot enumeration in the manuscript, deterministic
ledger regeneration) are all unchanged in substance at the R5 HEAD.
The intervening commits (`5ffd6df` manuscript v0.5; `ecf8475` Layer-3
result; `109a432` consolidated findings; `59a48dc` per-axis audit
transcripts; `99d9cfe` RELEASE_NOTES update) add the post-Layer-3
content the R4 confirmation was waiting on; none of them touches the
R3/R4 acceptance pillars.
