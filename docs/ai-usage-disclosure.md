# Generative-AI Usage Disclosure

This document discloses, in full, every use of generative-AI tooling in the
preparation of the Viewpoint manuscript and the supporting case study. It is
published in advance of any AI-assisted content so that subsequent commits
inherit a pre-declared usage envelope.

The Viewpoint manuscript and the case-study manuscript each carry a shorter
"AI Usage Statement" in their Acknowledgements and Methods sections; this
document is the long-form reference both statements link to.

## Scope of disclosure

The disclosure covers:

1. **Drafting and revising the Viewpoint manuscript itself.**
2. **The autonomous Layer-1 pipeline** that produced the case-study analysis
   and the case-study draft manuscript.
3. **The reviewer-subagent loop** that critiqued and revised both manuscripts.
4. **The audit-layer subagent** that re-executed the case-study code and
   checked citation veracity.

It does not cover: the operator's clinical practice; any tooling outside this
repository.

## Tools and versions

| Tool                 | Version                              | Vendor               | Role                                                               |
|----------------------|--------------------------------------|----------------------|--------------------------------------------------------------------|
| Anthropic Claude     | Opus 4.7 (1M-context variant)        | Anthropic            | Layer-1 orchestration, Layer-2 audit, reviewer subagents, drafting |
| Claude Code (CLI)    | Latest as of 2026-05                 | Anthropic            | Session runtime, tool use, file edits, shell execution             |
| Web search backend   | As used by Claude Code               | Anthropic-mediated   | Literature scoping, journal-spec retrieval                         |
| PubMed E-utilities   | Via Claude.ai MCP                    | NCBI                 | Reference verification                                             |
| bioRxiv / medRxiv API| Via Claude.ai MCP                    | CSHL / BMJ           | Preprint scoping                                                   |

No image-generation, figure-generation or chart-rendering model is used at
any stage. All figures are produced by deterministic Python / R code from
the case-study analysis scripts.

## Permitted-uses log (under current Lancet group policy)

The following uses fall within The Lancet group's currently published
permitted-uses list (language editing, grammar repair, prose polishing).

- Polishing the prose of the Viewpoint manuscript across reviewer rounds.
- Fixing grammar, voice and tense consistency.
- Producing concise versions of long sentences without changing meaning.
- Reformatting reference entries to Vancouver superscript-numeric style.

## Uses currently classified as prohibited

The following uses **are** invoked in this repository and **are** the subject
matter of the Viewpoint. They are itemised here in advance of any
camouflaging language.

1. **Generating scientific arguments.** The Viewpoint manuscript's argument
   structure was developed in dialogue with Claude. The operator supplied
   the thesis, the constraints (Lancet DH Viewpoint, single author, post-
   Co-Scientist landscape) and the dataset choices; Claude generated section
   plans, counter-argument enumerations and recommendation phrasing. Final
   acceptance of each argument is the operator's responsibility.
2. **Drafting methodology descriptions.** The case-study manuscript's
   Methods section was drafted by the Layer-1 pipeline (Claude) and revised
   across reviewer rounds. The operator's role is final acceptance.
3. **Producing literature reviews.** The "prior work" framing in both
   manuscripts was scoped by Claude using PubMed and bioRxiv search; the
   operator verified every retained citation against the live record.
4. **Selecting the case-study claim.** The Layer-1 pipeline was given the
   domain prompt ("HCC OS stratification beyond BCLC") and selected the
   specific sub-claim and statistical approach autonomously.
5. **Selecting reviewers.** The four reviewer subagents (methods, clinical,
   biostatistics, target-journal-editor) were instantiated by Claude from
   structured persona prompts; the operator did not pre-screen comments.

## Operator interventions, itemised

Every operator-vs-AI boundary is recorded. The operator's interventions are
restricted to:

- Supplying the operator-supplied orchestration prompt (`prompts/00-original-
  spec.md`) and three downstream domain prompts (`prompts/01-layer1-
  pipeline.md`, `prompts/02-layer2-audit.md`, `prompts/03-reviewer-*.md`).
- Confirming the case-study domain choice (HCC vs hematologic) and the
  autonomy mode (full autonomy with transparent ledger).
- Running the Layer-3 external validation on two preregistered GEO cohorts.
- Approving the final cover letter and clicking submit in Editorial Manager
  on the day of submission.
- Reading and accepting (or rejecting and re-running) each commit and each
  reviewer round before the corresponding tag is pushed.

The operator did **not**:

- Re-draft any sentence of either manuscript himself.
- Add, remove or modify reviewer-subagent comments.
- Modify a Layer-1 pipeline output after Layer-2 audited it.
- Select Layer-3 cohorts based on Layer-1's result.

## Prompt-as-protocol

The operator-supplied orchestration prompt is in `prompts/00-original-
spec.md` and is the protocol artefact this Viewpoint argues should replace
the methods-section narrative as the new minimum disclosure unit. The prompt
is committed verbatim, with no editorial smoothing, including any phrasing
the operator would now revise. The integrity rule is that the artefact is
preserved as it was used, not as the operator wishes it had been.

Model-pinning, API-snapshot and prompt-versioning details are recorded in
the same file's preamble; this is the file the Viewpoint's reproducibility
argument depends on.

## Formatted statement for the manuscripts' Acknowledgements

> The author acknowledges the use of Anthropic Claude (Opus 4.7, 1M-context
> variant) via the Claude Code CLI for argument development, methodology
> drafting, literature scoping, claim selection and reviewer-subagent
> orchestration in the preparation of this Viewpoint and its supporting
> case study. All scientific arguments, claim selections, final
> interpretations and submission decisions are the author's sole
> responsibility. A full per-tool, per-task disclosure log is published in
> `docs/ai-usage-disclosure.md` of the linked repository, with the exact
> orchestration prompts in `prompts/`. No generative-AI tool was used to
> create figures or images.

## Update policy

Any AI-tool change (new vendor, new model, new role) requires updating this
file in a commit that **precedes** the first use of the change. Backdating
disclosure is a violation of the honesty contract in `docs/design.md`.
