# Cover Letter — npj Digital Medicine Perspective submission

**Date.** `<<INSERT submission date>>`
**To.** The Editors, *npj Digital Medicine*

Dear Editors,

I am pleased to submit the enclosed unsolicited **Perspective** for consideration in *npj Digital Medicine*. The Perspective extends a transparency lineage that *npj Digital Medicine* itself opened in 2020 with Sendak and colleagues' [*Presenting machine learning model information to clinical end users with model facts labels*](https://doi.org/10.1038/s41746-020-0253-3). Model Facts Labels named the disclosure unit for a deployed clinical ML model; CONSORT-AI / SPIRIT-AI (Nature Medicine 2020) named it for AI-intervention trials; TRIPOD+AI (BMJ 2024) named it for AI-enabled prediction-model reporting. The lineage assumes the disclosed unit is a model or a trial. In 2026 that assumption broke: Google DeepMind's Co-Scientist ([10.1038/s41586-026-10644-y](https://doi.org/10.1038/s41586-026-10644-y)) and Sakana AI's end-to-end pipeline ([10.1038/s41586-026-10265-5](https://doi.org/10.1038/s41586-026-10265-5)) demonstrated that agentic-LLM workflows can autonomously perform manuscript-grade scientific reasoning. No corresponding transparency standard exists for that class.

This Perspective proposes Disclosure 2.0 — a six-item manifest (prompts, model identifier and tool envelope, commit history, reviewer-subagent transcripts, audit log, tagged release with persistent DOI) — as the agentic-LLM-research extension of the Model Facts Labels / TRIPOD+AI lineage. The Perspective and its supporting hepatocellular-carcinoma case study are themselves produced under Disclosure 2.0: the case study returned a preregistered null on external validation against GSE14520 and GSE76427 ($n=333$, $\Delta C$-index = 0.006 [-0.008, 0.030]) and a sealed Layer-2 audit filed twelve substantive findings on the case-study manuscript that the within-pipeline reviewer rounds did not catch. Both outcomes are visible because the disclosure regime is designed to make them visible.

The repository [https://github.com/htlin222/end-to-end](https://github.com/htlin222/end-to-end) is publicly archived under the MIT licence at tag `viewpoint-npjdm-v1.0.0`. A medRxiv preprint will be posted before submission.

## Submission metadata

| Item                | Value                                                    |
|---------------------|----------------------------------------------------------|
| Article type        | Perspective                                              |
| Body word count     | 1,529 (texcount; npj DM has no strict ceiling)           |
| References          | 11                                                       |
| Figures             | 1 (artefact ledger)                                      |
| Abstract            | ~250 words on title page                                 |
| Repository          | https://github.com/htlin222/end-to-end (`viewpoint-npjdm-v1.0.0`) |
| medRxiv DOI         | `<<INSERT after preprint posting>>`                      |
| Zenodo DOI          | `<<INSERT after GitHub-Zenodo mint>>`                    |

## Originality

This manuscript is original, has not been published, and is not under consideration at another journal. Companion variants targeted at *The Lancet Digital Health* (tag `viewpoint-v1.1.0`) and *NEJM AI* (tag `viewpoint-nejmai-v1.0.2`) were prepared in the same repository for fallback retargeting; they are not submitted to any journal at present and will not be submitted while the *npj Digital Medicine* Perspective is under consideration.

## Generative-AI background of the author

My prior LLM-adjacent work (theory-of-mind-like behaviour in LLM poker agents, arXiv 2026; an "AI Agents in Oncology" manuscript at *Journal of Cancer Research and Practice*, 2025) informs this Perspective's framing of agentic-LLM disclosure. My day job is as a haematology and medical oncology fellow at the Koo Foundation Sun Yat-Sen Cancer Center; I am not an LLM researcher, and the Perspective reflects a clinician-investigator's practical encounter with agentic tooling rather than a methods-paper contribution.

## Suggested reviewers

1. `<<INSERT reviewer 1>>` — clinical-AI transparency standards (Model Facts Labels, TRIPOD+AI, CONSORT-AI lineage)
2. `<<INSERT reviewer 2>>` — agentic LLM scientific discovery
3. `<<INSERT reviewer 3>>` — biomedical-journal AI disclosure policy
4. `<<INSERT reviewer 4>>` — digital-health workflow reproducibility / FAIR

Suggested starting points (operator selects, conflict-screens against Koo Foundation / Anthropic / Google / OpenAI / Sakana AI paid relationships):

- **Mark P. Sendak** (Duke DIHI; Model Facts Labels lead author; published in npj DM 5+ times) — natural fit
- **Karandeep Singh** (UCSD Jacobs; TRIPOD+AI working-group member)
- **Mohammad Hosseini** (Northwestern Galter Library; AI disclosure policy specialist)
- **Andrew L. Beam** (HSPH; multiple npj DM and JAMA Network reproducibility editorials)
- **Suchi Saria** (JHU; clinical AI implementation policy)
- **James Zou** (Stanford BMI; Lancet "agentic AI teammates" Feb 2025)

## Conflicts of interest

The author declares no competing interests. The author does not hold equity, employment, or paid advisory roles with Anthropic, Google, OpenAI, Sakana AI, or any other company whose tools are discussed.

## Funding

No specific funding. The Anthropic Claude subscription used to operate the workflow is the author's personal expense.

## Generative-AI disclosure

The Perspective and its supporting case study were prepared using Anthropic Claude (Opus 4.7, 1M-context variant) via the Claude Code CLI. A full per-step disclosure log is at `docs/ai-usage-disclosure.md` in the linked repository. No AI tool is listed as an author. No AI-generated figures.

Sincerely,

Hsieh-Ting Lin, M.D.
Department of Hematology and Medical Oncology
Koo Foundation Sun Yat-Sen Cancer Center
Taipei, Taiwan
ORCID: 0009-0002-3974-4528
mail@hsiehting.com
