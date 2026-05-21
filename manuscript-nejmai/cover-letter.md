# Cover Letter — NEJM AI Perspective submission

**Date.** `<<INSERT submission date>>`
**To.** The Editors, *NEJM AI*

Dear Editors,

I am pleased to submit the enclosed unsolicited **Perspective** for consideration in *NEJM AI*. The Perspective addresses a question that the launch of NEJM AI explicitly placed at the centre of the journal's remit: what disclosure standard should accompany biomedical manuscripts whose preparation involved generative-AI tooling at depth.

In 2026, Google DeepMind's Co-Scientist (*Nature* 2026, DOI [10.1038/s41586-026-10644-y](https://doi.org/10.1038/s41586-026-10644-y)) and Sakana AI's end-to-end pipeline (*Nature* 2026 651:914-919, DOI [10.1038/s41586-026-10265-5](https://doi.org/10.1038/s41586-026-10265-5)) demonstrated that autonomous agentic-LLM research has crossed peer review. In parallel, a single clinician-investigator can in 2026 assemble an equivalent workflow on commodity tooling. Current biomedical-journal AI policies — calibrated for a 2023 generation of LLM use — classify most of what such a workflow does as prohibited and ask for a single-sentence acknowledgement. The Perspective proposes a Disclosure 2.0 standard whose minimum unit is the {prompts, model identifier, tool envelope, commit history, reviewer-subagent transcripts, audit log, tagged release} — and the Perspective itself, together with its supporting hepatocellular-carcinoma case study (which returned a preregistered null on external validation), is produced under exactly that standard. The medium is the message.

The repository [https://github.com/htlin222/end-to-end](https://github.com/htlin222/end-to-end) is publicly archived under the MIT licence at tag `viewpoint-nejmai-v1.0.0`. A medRxiv preprint will be posted before submission; the DOI will be inserted into this letter and the manuscript's Data Sharing statement before clicking Submit.

## Submission metadata

| Item                | Value                                                    |
|---------------------|----------------------------------------------------------|
| Article type        | Perspective                                              |
| Body word count     | 620 (under 1,200 ceiling)                                |
| References          | 5/5                                                      |
| Figures             | 1/1 (artefact ledger)                                    |
| Abstract            | 1 sentence, present on title page                        |
| Repository          | https://github.com/htlin222/end-to-end (tag `viewpoint-nejmai-v1.0.0`) |
| medRxiv DOI         | `<<INSERT after preprint posting>>`                      |
| Zenodo DOI          | `<<INSERT after GitHub-Zenodo mint>>`                    |

## Originality

This manuscript is original, has not been published, and is not under consideration at another journal. A longer Viewpoint-format companion that targets *The Lancet Digital Health* was prepared in the same repository (tag `viewpoint-v1.1.0`) but is not submitted to any journal at present and will not be submitted while the NEJM AI Perspective is under consideration.

## Generative-AI background

My prior LLM-adjacent work (theory-of-mind-like behaviour in LLM poker agents, arXiv 2026; an "AI Agents in Oncology" manuscript at *Journal of Cancer Research and Practice*, 2025) informs this Perspective's framing of agentic-LLM disclosure. My day job is as a haematology and medical oncology fellow at the Koo Foundation Sun Yat-Sen Cancer Center; I am not an LLM researcher, and the Perspective reflects a clinician-investigator's practical encounter with agentic tooling rather than a methods-paper contribution.

## Suggested reviewers

1. `<<INSERT reviewer 1>>` — editorial AI policy / biomedical publishing
2. `<<INSERT reviewer 2>>` — agentic LLM scientific discovery
3. `<<INSERT reviewer 3>>` — clinical-prediction-model reporting (TRIPOD)
4. `<<INSERT reviewer 4>>` — digital-health workflow reproducibility / FAIR

## Conflicts of interest

The author declares no competing interests. The author does not hold equity, employment, or paid advisory roles with Anthropic, Google, OpenAI, Sakana AI, or any other company whose tools are discussed.

## Funding

No specific funding for this work. The Anthropic Claude subscription used to operate the workflow is the author's personal expense.

## Generative-AI disclosure

The Perspective and its supporting case study were prepared using Anthropic Claude (Opus 4.7, 1M-context variant) via the Claude Code CLI. A full per-step disclosure log is at `docs/ai-usage-disclosure.md` in the linked repository. No AI tool is listed as an author. No AI-generated figures.

Sincerely,

Hsieh-Ting Lin, M.D.
Department of Hematology and Medical Oncology
Koo Foundation Sun Yat-Sen Cancer Center
Taipei, Taiwan
ORCID: 0009-0002-3974-4528
mail@hsiehting.com
