# Target Journal — *The Lancet Digital Health*

Article type: **Viewpoint** (opinion piece reflecting an individual perception,
involvement, or contribution to digital health; unsolicited contributions are
welcome).

Sources (consulted 2026-05-20):

- Lancet Digital Health "Information for Authors" PDF (mirrored references
  on the Lancet website; PDF Cloudflare-gated as of 2026-05-20).
- Elsevier Guide for Authors landing page (`elsevier.com/journals/the-lancet-
  digital-health/2589-7500/guide-for-authors`; redirects to ScienceDirect,
  also gated).
- *The Lancet* "Editorial Policies" page on AI usage, applied across the
  Lancet family of journals.
- "Lancet AI Policy" 2026 synthesis (Manusights).
- *The Lancet Digital Health* "About" page (`thelancet.com/landig/about`).

The figures below are the operative ceilings for this submission. Any
discrepancy with the live Information-for-Authors PDF, retrieved on the day
of submission, **must** be resolved in favour of the live PDF; this file is
the operator's working interpretation, not the authoritative source.

## Format ceilings

| Item              | Ceiling for Viewpoint                                  |
|-------------------|---------------------------------------------------------|
| Body word count   | **2 500 words**                                         |
| References        | **30** maximum                                          |
| Display items     | **2** (any combination of figures and tables)           |
| Summary / abstract| None required for Viewpoint                             |
| Title             | <= 150 characters incl. spaces                          |
| Running title     | <= 50 characters                                        |
| Key messages box  | Optional but improves desk acceptance; <= 5 bullets     |

## Structure (Review-like)

Lancet Viewpoints are "prepared in a similar way to a Review". Recommended
sections:

1. **Opening framing** — the question, the stake, the actor.
2. **2-4 substantive sections** — argument with evidence and counter-argument.
3. **Recommendations / call to action** — concrete proposals.
4. **Search strategy and selection criteria** panel — required when prior
   literature is cited (placement: end of Viewpoint, before References).
5. **Declarations** — contributors, declaration of interests, data sharing,
   acknowledgements, role of the funding source.

## Reference style

- **Vancouver superscript-numeric.** In-text: `study A1,2 and study B3-5`.
- Reference list: sequential by first appearance; full author list up to six,
  then `et al.`; journal abbreviations follow Index Medicus.
- DOIs required where available.
- LaTeX: `\bibliographystyle{vancouver-superscript}` if available, else
  `vancouver` + `\usepackage[numbers,super,sort&compress]{natbib}`.

## File formats

- **LaTeX accepted** by The Lancet group. Submit `.tex`, `.bib`, all figure
  files, and the compiled `.pdf`.
- Microsoft Word is also accepted; the operator may convert via
  `pandoc main.tex -o main.docx --bibliography references.bib --csl=vancouver-superscript.csl`
  if the submission portal rejects LaTeX uploads.
- Figures: vector PDF or EPS preferred. PNG accepted at >= 300 dpi for the
  long axis. No AI-generated figures.

## Title page contents

- Full title.
- Running title (<= 50 characters).
- Each author's full name, highest academic degree, ORCID, affiliation.
- Corresponding author's full postal address, e-mail.
- Word count (body, excluding references and display items).
- Reference count.
- Number of display items.
- Conflict of interest statement.
- Funding statement.
- Search strategy and selection criteria reference (panel id).

## Generative-AI disclosure policy (verbatim spirit)

The Lancet group's current public policy as of 2026:

1. **AI tools cannot be listed as authors.** AI cannot meet the ICMJE
   accountability requirement and must not be credited as such.
2. **Disclosure is mandatory** when a generative-AI tool is used in the
   preparation of a manuscript. The disclosure must appear in two places:
   - **Methods section** (or equivalent for non-research articles): which
     tool, version, vendor; what task it was used for; what human review or
     editing was applied; any limitations encountered.
   - **Acknowledgements**: a formatted statement, e.g., "The author
     acknowledges the use of Anthropic Claude (Opus 4.7) via Claude Code for
     manuscript drafting and revision. All scientific arguments, claim
     selection, and final interpretation are the author's responsibility."
3. **Permitted uses (current policy):** language editing, grammar repair,
   prose polishing.
4. **Prohibited uses (current policy):** generating scientific arguments,
   drafting methodology descriptions, producing literature reviews, creating
   new scientific content, generating images or figures.

### Friction with this submission

The Viewpoint argues that the Lancet group's "prohibited uses" list is
structurally inconsistent with the operating reality of clinician-
investigators using agentic LLM tooling in 2026. The submission therefore
**does** invoke uses currently classified as prohibited, and **does** disclose
them in full. The point of contact between submission and policy is the
explicit subject matter of the Viewpoint, not an oversight. See
`docs/ai-usage-disclosure.md` for the complete log.

## Data and code availability

The Lancet Digital Health requires a Data Sharing Statement on submission.
Acceptable language for this submission:

> All code, prompts, intermediate artefacts, reviewer-subagent transcripts,
> and the case-study manuscript are publicly archived at
> `https://github.com/<user>/end-to-end` under the MIT licence, with the
> exact submission state tagged `viewpoint-v1.0.0`. Public datasets used in
> the supporting case study (TCGA-LIHC, GSE14520, GSE76427) are available
> from the original repositories cited in `case-study/manuscript/references.bib`.

## Competing interests

The author declares no competing interests. (Confirm at submission and update
if any commercial relationship arises in the meantime.)

## Reporting guidelines

Viewpoints are opinion pieces and are not bound to a specific reporting
checklist. However, where the Viewpoint cites the supporting case study, the
case-study manuscript itself follows **TRIPOD 2015** for the prognostic-
model component (the HCC risk-score evaluation) and **STROBE** for the
cohort description.

## Cover letter requirements

Cover letter should:

- State the article type (Viewpoint), word count, reference count, and
  display-item count.
- State that the manuscript has not been published and is not under
  consideration elsewhere.
- State preprint posting status (medRxiv DOI and date, if applicable).
- Briefly summarise the contribution (why this Viewpoint, why now).
- Suggest 3-5 independent reviewers (Lancet group accepts and uses
  suggestions selectively).
- Identify any individuals the author would prefer not to review (max two).
- State conflicts of interest.

## Submission portal

The Lancet Digital Health uses the Lancet group's Editorial Manager at
`https://www.editorialmanager.com/landig/`. ScholarOne is not used for this
journal. ORCID is required for the corresponding author at submission.

## Preprint policy

The Lancet group permits posting of preprints on bioRxiv / medRxiv prior to
submission. For this submission the operator will post the manuscript to
medRxiv after the case-study repository is publicly archived (tag
`viewpoint-v1.0.0`) and before clicking "Submit" in Editorial Manager. The
medRxiv DOI is reported in the cover letter.

## Author block (verbatim for this submission)

```
Hsieh-Ting Lin, M.D.
Department of Hematology and Medical Oncology
Koo Foundation Sun Yat-Sen Cancer Center
125 Lide Road, Beitou District, Taipei 112, Taiwan
ORCID: 0009-0002-3974-4528
Correspondence: mail@hsiehting.com
```

(Postal address line above is a placeholder for the institution's official
postal address; replace with the verified address from the institution's
website prior to final submission.)

## Operator's submission checklist

- [ ] Title and running title within character limits
- [ ] Body word count <= 2 500
- [ ] References <= 30, Vancouver superscript-numeric, all DOIs resolved
- [ ] Display items <= 2 (Figure 1 = artefact ledger; Figure 2 = policy gap)
- [ ] Search strategy and selection criteria panel present
- [ ] Generative-AI disclosure present in Methods-equivalent paragraph AND
      Acknowledgements
- [ ] `docs/ai-usage-disclosure.md` cross-linked from manuscript
- [ ] Data sharing statement points to the GitHub repository and tag
- [ ] Cover letter includes article type, word/ref/display counts, preprint
      DOI, reviewer suggestions
- [ ] ORCID linked in Editorial Manager
- [ ] No AI-generated figures
- [ ] medRxiv preprint posted, DOI recorded
- [ ] Live Information-for-Authors PDF re-verified on day of submission;
      diffs against this file resolved.
