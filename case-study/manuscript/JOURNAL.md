# Target Journal — JCO Clinical Cancer Informatics

Layer-1 selected **JCO Clinical Cancer Informatics (JCO CCI)** as the
case-study target journal. This file distils the submission spec into
a one-page checklist the case-study manuscript draft and the editor
reviewer subagent both use.

The selection was made by Layer 1 after WebSearch on (1) JCO CCI's
remit for clinical-prediction submissions, (2) its tolerance for
TRIPOD-aligned methods detail, (3) its generative-AI policy (compatible
with the disclosure in `../../docs/ai-usage-disclosure.md`), and (4) its
practical acceptance rate for single-cohort case studies with one
external validation. Alternative venues that were considered but not
chosen: *Briefings in Bioinformatics* (more methods-leaning, would
require a sharper methodological contribution than HCC-TRS provides),
*npj Precision Oncology* (more biology-leaning, would benefit from a
mechanistic story), *JHEP Reports* (good fit but smaller informatics
audience).

## Identifier and contact

- Journal: JCO Clinical Cancer Informatics
- Publisher: American Society of Clinical Oncology
- Author Information page: <https://ascopubs.org/journal/cci>
- Information for Contributors (PDF): <https://ascopubs.org/pb-assets/pdfs/JCO-CCI-IFC.pdf>
- AI policy: ASCO journals policy (JCO CCI follows JCO's policy), see
  <https://ascopubs.org/authors/journal-policies>

## Article type

**Original Reports**.

## Word and structural limits

| Element                          | Limit / requirement                                                 |
|----------------------------------|----------------------------------------------------------------------|
| Body text (Intro - Discussion)   | <= 3,000 words                                                       |
| Abstract                         | <= 250 words, structured: Purpose / Methods / Results / Conclusion   |
| References                       | ~40 (soft cap); >60 risks technical-check trim                       |
| Display items (figures + tables) | <= 5 in main paper (extras to Data Supplement)                       |
| Plain-language summary           | Encouraged but not strictly required for Original Reports            |

Word count excludes abstract, references, figure legends, table content.

## Required reporting

- **TRIPOD 2015** (or TRIPOD+AI 2024) checklist required for clinical-
  prediction-model submissions. The manuscript includes a TRIPOD
  compliance table in the supplement and notes the items not
  applicable.
- **AMA Manual of Style** numbered superscript citations.
- **ORCID** for the corresponding author at submission.
- **Data Availability Statement**: TCGA accessions and GEO accession(s);
  link to the public repository tag.
- **Code Availability**: link to the public repository tag.
- **Pre-registration**: statement disclosing the case-study Layer-1
  prereg (`case-study/docs/prereg.md`) and the operator's Layer-3
  prereg (`docs/prereg.md`).

## Generative-AI disclosure

JCO CCI follows the ASCO journals' generative-AI policy. Permitted uses
require disclosure in the **Methods** section, stating tool name,
version, and exact purpose. Prohibited uses (must not occur) include
AI authorship, AI-generated images/figures, AI clinical interpretation,
AI treatment recommendations. The case-study manuscript:

- Uses Anthropic Claude (Opus 4.7, 1M context) via Claude Code for
  Layer-1 orchestration including methodology drafting, manuscript
  drafting, and reviewer-subagent dispatch.
- Does **not** use AI for figure generation; all figures are produced
  by deterministic Python from analysis scripts.
- Does **not** use AI for clinical-outcome interpretation; survival
  models are statistical, not AI-summarised, and the discussion frames
  results without AI-generated clinical recommendations.
- Discloses the full envelope in `../../docs/ai-usage-disclosure.md`
  (linked from the manuscript's AI-statement).

JCO CCI's policy does not prohibit AI from drafting the methodology
section as long as it is disclosed. The case-study manuscript discloses
this honestly. The Viewpoint manuscript discusses this disclosure
asymmetry between current journal policy and operating reality; that
discussion is bounded to the Viewpoint, not the case-study manuscript.

## Data and code availability statement (template)

> **Data**. TCGA-LIHC RNA-seq STAR counts and clinical attributes were
> downloaded from the GDC public API on <DATE>. The non-reserved GEO
> validation cohort (GSE<XXXXX>) was downloaded from NCBI GEO via the
> Series Matrix file on <DATE>. GSE14520 and GSE76427 are reserved for
> the operator's Layer-3 external validation per a preregistration
> dated 2026-05-21 and were not accessed during model development.
>
> **Code**. Analysis scripts, manuscript source, reviewer-loop logs,
> and the LaTeX source for this manuscript are publicly available at
> the public release tag <case-study-vX.Y.Z> of the repository at
> <https://github.com/htlin/end-to-end> (URL fixed at the time of
> tagging; the repository is private until the Viewpoint is accepted,
> at which point it becomes public).

## Pre-registration statement (template)

> **Pre-registration**. The Layer-1 analytic design (sub-claim,
> primary outcome, statistical method, feature-selection rule, multiple-
> testing family) is preregistered in `case-study/docs/prereg.md`,
> committed before any model was fitted. The Layer-3 external-validation
> design (cohorts, metrics, null hypothesis, threshold) is preregistered
> separately in `docs/prereg.md`.

## Format compliance plan

- LaTeX class: `article`, 12pt, 1.5-spaced for submission.
- References: AMA-style numbered, generated from `references.bib`
  using `apacite`-replacement `unsrtnat` configured for AMA-like
  superscripts, or natbib with `numbers,super,sort&compress`.
- Figures: PDF, embedded as `\includegraphics`. Source PDFs in
  `../figures/`.
- Submission package will include: `main.pdf`, supplementary PDF,
  TRIPOD checklist, ORCID, ICMJE conflict-of-interest forms,
  data-availability statement, AI-usage statement, response-to-
  reviewers letter for each revision.

## Editor reviewer triggers (informational)

The editor reviewer subagent (`prompts/03-reviewer-editor.md`) checks
the manuscript against this file every round. Triggers it raises:

- Body > 3,000 words.
- Abstract not Purpose/Methods/Results/Conclusion.
- > 5 display items in main text without justification.
- No TRIPOD compliance reference.
- No Data Availability or Code Availability section.
- No generative-AI disclosure in Methods or Acknowledgements.
- No ORCID for corresponding author.
- Reference style not numbered superscript.

## Notes on selection rationale

A reviewer challenging the venue choice would receive this answer:

- The HCC-TRS contribution is *methodologically modest*; it is a
  bootstrap-validated additive Cox model with one external cohort,
  not a novel learning architecture. *Briefings in Bioinformatics*
  would expect a stronger methodological contribution.
- The clinical-translation story is *deliberately bounded* (the
  manuscript states the score is illustrative and not clinical-grade)
  to honour the Viewpoint's integrity contract. *Genome Medicine* and
  *JHEP Reports* expect a clinical hook the case study does not over-
  promise.
- JCO CCI's remit is precisely "clinical informatics applied to cancer
  data" with an audience that is comfortable with TRIPOD-aligned
  prediction-model reporting and one external cohort.

If the editor reviewer rejects the venue fit at round 1, the alternative
venue is *Briefings in Bioinformatics*, and a venue pivot is recorded
as a Layer-1 failure mode under `reviewer-logs/round-NN/failure-mode-
venue-pivot.md`. The pivot is *not* permitted to scope the analysis;
only the manuscript framing changes.
