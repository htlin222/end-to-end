# Round 1 — Clinical Reviewer

**Round**: 01
**Reviewer**: Clinical (per `prompts/03-reviewer-clinical.md`)
**Date**: 2026-05-21
**Reviewed artefacts**: `case-study/manuscript/main.tex`.

## Overall impression

The clinical framing is bounded and honest in places, but the abstract
and the Results frame the discrimination delta in language that an
attending hepatologist will misread as clinically meaningful. The
Discussion's Limitations section correctly addresses several of these
issues but the abstract / Introduction need tighter language. The
GSE10143 null result is acknowledged but the implications for clinical
generalisability deserve more weight.

## Comments

### Comment 1 [HIGH] — Baseline-staging substitution AJCC vs BCLC needs to be stated up-front, not buried in Methods

The Viewpoint repository's domain prompt described "OS stratification
beyond BCLC stage", and `docs/prereg.md` flags AJCC-vs-BCLC substitution
as a known limitation. The case-study manuscript discusses this in
the Discussion's "Population" limitation but the abstract and the
Introduction speak of "improving OS discrimination over AJCC pathologic
stage" as if that were the canonical clinical comparator for HCC. **It
is not**: clinical HCC management uses BCLC. Either:

(a) Lead the Introduction with a one-paragraph statement of why this
manuscript compares against AJCC (TCGA-LIHC records AJCC, BCLC is the
clinical standard, this is a public-data substitution), OR
(b) Re-title the manuscript "beyond AJCC pathologic stage in resected
HCC" to make the audience clear from the first sentence.

The current title does include "beyond AJCC pathologic stage" which
helps, but the rest of the paper does not return to BCLC and a
hepatologist reader will treat the absence as an implicit claim that
AJCC is the comparator. Add an explicit one-line statement.

Severity: high.

### Comment 2 [HIGH] — Population framing: TCGA-LIHC is heavily enriched for resected, BCLC A/B disease

This is acknowledged in the Discussion but should be stated **also**
in the abstract and the Introduction. "Resected primary HCC" appears
twice in the Discussion but never in the abstract. The score's
performance in BCLC C/D patients is **not assessed** and a hepatologist
reader will need to be told that within the abstract, before the
methods. One sentence: "Findings apply to the resected, surgical-
candidate population represented in TCGA-LIHC; the score is not
evaluated in BCLC C/D disease."

Severity: high.

### Comment 3 [HIGH] — Aetiology heterogeneity is acknowledged but not handled

The Discussion notes HBV/HCV/MASH/alcohol heterogeneity but the model
does not stratify or adjust. This is a real prognostic confounder in
HCC (the survival of HBV-related HCC after curative resection differs
materially from MASH-HCC) and a Layer-1 internal subgroup analysis
should be reportable from the TCGA-LIHC clinical fields. Either:

(a) Add an exploratory subgroup analysis with aetiology where data
permit, or
(b) State explicitly in the manuscript that aetiology data was not
reliably available in the TCGA-LIHC clinical export used.

Currently the manuscript reads as if aetiology were available but
ignored.

Severity: high.

### Comment 4 [HIGH] — Decision-curve analysis is absent

For a transcriptomic score positioned as "refining OS stratification",
a Vickers-Elkin DCA at clinically relevant thresholds (5-year
mortality 0.1/0.2/0.3 is the convention in HCC) is the minimum
clinical-translation artefact. None is reported in this manuscript.
The reserved Layer-3 prereg (`docs/prereg.md` S6) includes DCA at
those thresholds. The Layer-1 manuscript should at least show DCA on
the TCGA-LIHC development set so the reader can see the net-benefit
envelope.

Severity: high.

### Comment 5 [MEDIUM] — Treatment-era confounding statement is correct but weak

The Discussion's "Treatment era" paragraph is one sentence. For an
HCC paper, this is the single most important external-validity
caveat: TCGA-LIHC enrolled patients before the immune-checkpoint era
(atezolizumab + bevacizumab approval 2020). The score may correctly
identify high-OS-risk patients in the pre-immunotherapy era but the
risk strata may NOT correspond to the same clinical course under
modern systemic therapy. Expand to a full paragraph.

Severity: medium.

### Comment 6 [MEDIUM] — "Clinically meaningful margin" in the Discussion is unjustified

The Discussion says "the case study refines OS stratification beyond
AJCC stage by a clinically meaningful margin". For HCC, a 0.06
optimism-corrected ΔC in a TCGA development cohort with no external
replication is **not** clinically meaningful in any operational sense:
no decision threshold changes, no surveillance interval would be
modified, no adjuvant therapy is indicated by a 0.06 ΔC. Either:

(a) Strike "clinically meaningful" and replace with "statistically
detectable and prespecified as the Layer-1 internal threshold", OR
(b) Define what clinical decision is changed by a 0.06 ΔC and cite
the source.

I would accept (a).

Severity: medium.

### Comment 7 [MEDIUM] — Competing-risks treatment: liver transplant, non-cancer death

In HCC, liver transplant within the follow-up window and non-cancer
deaths from chronic liver disease are common competing events. The
Methods uses OS (any-cause), which is appropriate for the headline
endpoint but a sensitivity analysis with cancer-specific mortality
(or Fine-Gray for cancer-mortality with transplant as competing
event) would strengthen the clinical interpretation.

Severity: medium. Required: at least a sentence acknowledging this
in Discussion (which is present — keep it and consider expanding).

### Comment 8 [LOW] — Plain-language summary

JCO CCI's submission form does not strictly require a plain-language
summary for Original Reports, but for the Viewpoint manuscript's
disclosure-standard argument to land, the case-study manuscript
should include a 100-word plain-language summary. Optional.

Severity: low.

### Comment 9 [LOW] — Median follow-up and event accrual table

A small "Cohort characteristics" table with median follow-up time,
event count by stage, and follow-up by stage would help the reader
calibrate the C-index in clinical units. Optional but conventional.

Severity: low.

## Verdict

**`major-revision`**.

The combination of (1) up-front AJCC-vs-BCLC framing, (2) explicit
"resected surgical-candidate" population statement in abstract, (3)
aetiology subgroup, and (4) decision-curve analysis would bring this
manuscript to a level a hepatologist reader can endorse. Comments 1-4
are blockers; 5-7 are tighten-the-language items; 8-9 are optional.
