# medRxiv submission metadata

[Operator: this file is the data-entry script for the medRxiv submission
form. medRxiv is the appropriate preprint server for digital-health /
clinical-policy articles; bioRxiv is not. Post the preprint **after**
the GitHub repository is publicly archived at tag `viewpoint-v1.0.0`
and **before** clicking Submit in Editorial Manager. The medRxiv DOI
goes into the cover letter and into the manuscript's Data Sharing
statement.]

## Identification

- **Article type**: Original research (medRxiv allows opinion/Viewpoint
  pieces under this category; the article-type label in the metadata
  is "research-article" and the secondary type is "Editorial").
- **Preprint server**: medRxiv (\url{https://www.medrxiv.org}).
- **Embargo**: none.

## Title

> The prompt is the protocol: a disclosure standard for clinician-
> investigators using agentic large language models.

## Running title (medRxiv accepts the same as the manuscript)

> Disclosure 2.0 for agentic clinical research.

## Author

- **Name**: Hsieh-Ting Lin
- **First and middle initials**: H-T
- **Last name**: Lin
- **ORCID**: 0009-0002-3974-4528
- **Affiliation**: Department of Hematology and Medical Oncology, Koo
  Foundation Sun Yat-Sen Cancer Center, Taipei, Taiwan.
- **Email**: mail@hsiehting.com
- **Corresponding author**: yes
- **Conflicts of interest**: none

## Abstract (medRxiv allows up to 350 words; Viewpoint has no journal abstract, so this is a preprint-only abstract for indexing)

Centralised agentic large-language-model (LLM) systems such as Co-Scientist
(\textit{Nature}, 2026) have moved autonomous scientific reasoning into the
research toolkit. In parallel, a single clinician-investigator can in 2026
assemble an end-to-end agentic workflow that performs literature scoping,
claim selection, methods drafting, manuscript writing, reviewer-subagent
critique and tagged release on commodity tooling. The Lancet group's
current generative-AI policy, calibrated for a 2023 generation of LLM use,
classifies most of what such a workflow does as prohibited and asks for a
single-sentence acknowledgement when it occurs. We argue that the current
policy fails to address the failure modes it is designed to protect
against (authorship inflation, scientific hallucination, undocumented
intervention), and propose a Disclosure 2.0 standard whose minimum unit is
the tuple \{prompt, model identifier, tool envelope, commit history,
reviewer-subagent transcripts, audit log, tagged release\}. The proposal is
operationalised: the present Viewpoint and its supporting case study
(refined HCC overall-survival stratification on TCGA-LIHC with
preregistered external validation on GSE14520 and GSE76427) are themselves
produced under Disclosure 2.0, with every artefact publicly archived. The
medium is the message: a reviewer who accepts the Viewpoint endorses the
methodology; a reviewer who rejects it must do so on grounds the
repository itself disproves.

## Keywords

generative AI; large language models; editorial policy; disclosure
standards; clinician-investigator; reproducibility; hepatocellular
carcinoma; preregistration

## Subject area

medRxiv: Health Informatics (primary); Public and Global Health (secondary).

## Funding statement

The author received no specific funding for this work.

## Declaration of interests

The author declares no competing interests.

## Data and code availability

All code, prompts, intermediate artefacts, reviewer-subagent
transcripts, audit log and the supporting case-study manuscript are
publicly archived at
\url{https://github.com/htlin222/end-to-end} under the MIT licence,
with the exact submission state tagged \texttt{viewpoint-v1.0.0}.
Public datasets used in the supporting case study (TCGA-LIHC, GSE14520,
GSE76427) are available from the original repositories cited in
\texttt{case-study/manuscript/references.bib}.

## Ethics statement

This work uses only publicly released, de-identified secondary data and
did not require additional institutional review board approval. The
Viewpoint itself does not report human-subjects data.

## Related links

- GitHub repository: \url{https://github.com/htlin222/end-to-end}
- Persistent code DOI (Zenodo): `<<INSERT after Zenodo mint>>`
- AI usage disclosure: \url{https://github.com/htlin222/end-to-end/blob/main/docs/ai-usage-disclosure.md}
- Layer-3 preregistration: \url{https://github.com/htlin222/end-to-end/blob/main/docs/prereg.md}

## Submission timing

1. Make the GitHub repository public at tag `viewpoint-v1.0.0`.
2. Trigger the GitHub-Zenodo integration to mint a persistent code DOI.
3. Post the preprint to medRxiv with the metadata above.
4. Wait for medRxiv to assign a DOI (typically 1-3 business days).
5. Update the cover letter and the manuscript's Data Sharing statement
   with the medRxiv DOI.
6. Submit to *The Lancet Digital Health* via Editorial Manager.

## medRxiv submission script (planned)

```bash
# Posting a medRxiv preprint requires manual submission via the medRxiv
# web form; no public API is available. The fields above map 1:1 to the
# form. Time required: approximately 20 minutes.
```
