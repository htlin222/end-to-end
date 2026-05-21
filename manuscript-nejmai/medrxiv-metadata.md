# medRxiv submission metadata — NEJM AI Perspective preprint

Post BEFORE clicking Submit in NEJM AI Editorial Manager. medRxiv DOI
flows into the cover-letter Data-Sharing block.

## Identification

- **Article type**: Original research (medRxiv allows opinion/Perspective
  pieces under this category; secondary article type "Editorial").
- **Preprint server**: medRxiv (https://www.medrxiv.org).
- **Embargo**: none.

## Title

> The prompt is the protocol: a disclosure standard for clinician-
> investigators using agentic large language models.

## Running title

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

## Abstract (medRxiv version; longer than the NEJM AI 1-2 sentence on-page abstract)

A single clinician-investigator can in 2026 assemble an end-to-end
agentic large-language-model research workflow on commodity tooling
(Anthropic Claude via the Claude Code CLI; public TCGA-LIHC and GEO
data; Python / R / LaTeX). Current biomedical-journal artificial-
intelligence policies, calibrated for a 2023 generation of LLM use,
classify most of what such a workflow does as prohibited and ask for a
single-sentence acknowledgement. We propose a Disclosure 2.0 standard
whose published unit is the {prompts, model identifier, tool envelope,
commit history, reviewer-subagent transcripts, audit log, tagged
release} accessible at a tagged release. A minimum viable manifest
(prompts plus model identifier plus commit hash plus tag) is defined
for low-resource submissions. The present Perspective and its
supporting hepatocellular-carcinoma overall-survival case study (which
returned a preregistered null on external validation against GSE14520
and GSE76427, pooled n=333, delta-C-index 0.006 [95% bootstrap CI
-0.008 to 0.030], with twelve Layer-2 audit findings on the
case-study manuscript) are themselves produced under Disclosure 2.0;
every artefact is publicly archived at https://github.com/htlin222/
end-to-end under the MIT licence at the tagged release
viewpoint-nejmai-v1.0.0. The medium is the message: a reviewer who
accepts the Perspective endorses the methodology; a reviewer who
rejects it must do so on grounds the repository itself disproves.

## Keywords

generative AI; large language models; editorial policy; disclosure
standards; clinician-investigator; reproducibility; hepatocellular
carcinoma; preregistration; NEJM AI

## Subject area

medRxiv: Health Informatics (primary); Public and Global Health
(secondary).

## Funding statement

The author received no specific funding for this work.

## Declaration of interests

The author declares no competing interests.

## Data and code availability

All code, prompts, intermediate artefacts, reviewer-subagent
transcripts, Layer-2 audit log and the supporting case-study manuscript
are publicly archived at https://github.com/htlin222/end-to-end under
the MIT licence, with the exact preprint state tagged
`viewpoint-nejmai-v1.0.0`.

## Ethics statement

This work uses only publicly released, de-identified secondary data and
did not require additional institutional review board approval. The
Perspective itself does not report human-subjects data.

## Related links

- GitHub repository (public): https://github.com/htlin222/end-to-end
- NEJM AI Perspective tag: viewpoint-nejmai-v1.0.0
- Lancet DH Viewpoint companion (not currently submitted): viewpoint-v1.1.0
- Case-study release: case-study-v1.0.1
- AI usage disclosure: docs/ai-usage-disclosure.md
- Preregistration: docs/prereg.md (commit 88d6d15)

## Posting workflow

1. Open medRxiv submission form: https://www.medrxiv.org/submit
2. Account: create OR log in with hsieh.ting.lin@gmail.com
3. Paste title and running title (above)
4. Author block: copy from above; ORCID 0009-0002-3974-4528
5. Affiliation: Department of Hematology and Medical Oncology, Koo
   Foundation Sun Yat-Sen Cancer Center, Taipei, Taiwan
6. Abstract: paste the abstract above (medRxiv allows up to 350 words)
7. Manuscript: upload `manuscript-nejmai/main.pdf` (or compile from .tex)
8. Supporting materials: optional cover-letter.md, references.bib
9. Keywords: paste keywords above
10. Subject area: Health Informatics (primary); Public and Global Health
    (secondary)
11. Funding: none
12. Conflicts of interest: none
13. Submit; wait 1-3 business days for DOI
14. Once DOI arrives, update `manuscript-nejmai/cover-letter.md`
    `<<INSERT medRxiv DOI>>` line.
