# `01-layer1-pipeline.md` — Layer 1 Autonomous Pipeline Kickoff

**Protocol artefact.** Verbatim kickoff prompt for the autonomous Claude
Code session that produces the case study. Issued once, at session start.
No further operator interaction during this session is permitted by the
honesty contract in `docs/design.md`.

## Preamble

- **Model**: Anthropic Claude `claude-opus-4-7` (1M-context variant) via
  the Claude Code CLI.
- **Snapshot date**: planned for the day Layer 1 is dispatched; recorded
  in the actual session at execution time.
- **Tool envelope**: Read, Edit, Write, Bash, WebSearch, WebFetch, Agent
  (general-purpose subagent), MCP `claude_ai_PubMed`, MCP
  `claude_ai_bioRxiv`, TaskCreate / TaskUpdate / TaskList.
- **Session boundary**: kickoff prompt opens the session; operator
  reads but does not type into the session. The session ends at the
  push of the `case-study-v1.0.0` tag.

## Prompt (verbatim)

> You are running Layer 1 of the architecture described in
> `docs/design.md`. You are a single autonomous Claude Code session. Your
> mandate is to produce a complete reproducible study and a draft
> manuscript matching a clinical-genomics journal's submission
> specifications, in this repository's `case-study/` subdirectory, on the
> following domain:
>
> **Domain prompt.** Use TCGA-LIHC plus public GEO cohorts (GSE14520 and
> GSE76427 are reserved by the operator for held-out external validation
> and are **off-limits to you during Layer 1**) to refine overall-survival
> stratification of hepatocellular carcinoma beyond AJCC pathologic stage.
> Select your own sub-claim, your own statistical method, your own
> feature set, and your own target journal from among clinical-genomics
> venues with author instructions you can retrieve via WebFetch. Produce
> a fully reproducible analytic pipeline, a draft manuscript matched to
> the target journal's submission specifications (write a
> `case-study/manuscript/JOURNAL.md` distilling those specifications), and
> four reviewer-subagent rounds (methods, clinical, biostatistics,
> target-journal editor) until unanimous ACCEPT.
>
> **Hard constraints.**
>
> 1. You do not touch GSE14520 or GSE76427 except to record that they are
>    reserved external-validation cohorts in the manuscript's data-
>    availability statement. No download, no read, no peek at metadata.
> 2. You commit to git after every substantive change with a semantic
>    message. You do not force-push, amend, or rebase any commit you have
>    already created.
> 3. You write to `case-study/`, `prompts/`, and `reviewer-logs/` only.
>    You do not edit `manuscript/`, `docs/`, or any file outside
>    `case-study/`. The Viewpoint manuscript and the integrity anchors
>    are out of scope.
> 4. You do not edit the prompts in `prompts/`. If you want to fork a
>    prompt for an experimental subagent, you add `prompts/NN-name-v2.md`.
> 5. You commit `case-study/manuscript/JOURNAL.md`, `case-study/docs/
>    prereg.md` (a case-study-internal preregistration of *your* primary
>    outcome, distinct from the Layer-3 preregistration in
>    `docs/prereg.md`), and the analysis stub `01_prepare_data.py` before
>    you run any code that touches the outcome.
> 6. You produce reviewer-loop artefacts in `reviewer-logs/round-NN/` per
>    the spec in `reviewer-logs/README.md`. Each round's `summary.md` and
>    `decisions.json` are committed; reviewer transcripts are verbatim.
> 7. You tag `case-study-v1.0.0` only when all four reviewer subagents
>    in the closing round return `verdict: "accept"` in
>    `decisions.json`.
> 8. You report Bash exit codes truthfully. If a download fails, the
>    failure is recorded; you do not pretend it succeeded.
> 9. If you discover a methodological flaw mid-run, you commit the flaw
>    as a `failure-mode.md` under the relevant round and re-design;
>    you do not edit the history of the flaw away.
> 10. Honesty contract from `docs/design.md` is binding: no claim
>     screening, no history rewriting, no post-hoc instrumentation.
>
> **Deliverables.**
>
> - `case-study/analysis/01_prepare_data.py` through
>   `case-study/analysis/04_figures.py`, each idempotent and producing
>   committed intermediate artefacts in `case-study/data/results/`.
> - `case-study/manuscript/main.tex`, `case-study/manuscript/references.
>   bib`, `case-study/manuscript/JOURNAL.md`, `case-study/manuscript/
>   Makefile`, `case-study/manuscript/latexmkrc`. Manuscript compiles
>   to `case-study/manuscript/main.pdf` (gitignored).
> - `case-study/docs/prereg.md` (Layer-1-internal preregistration).
> - `reviewer-logs/round-01/` through `reviewer-logs/round-NN/` with the
>   four reviewer transcripts, `summary.md`, and `decisions.json` per
>   round.
> - A `case-study-v1.0.0` tag, pushed only after unanimous ACCEPT.
>
> **You do not deliver.**
>
> - The Layer-2 audit (`reviewer-logs/audit/`). That is a separate
>   session.
> - The Layer-3 external validation
>   (`case-study/data/results/layer3_validation.json`). That is the
>   operator's single step, performed against the two reserved GEO
>   cohorts after you finish.
> - Any change to `manuscript/`, `prompts/00-original-spec.md`, or
>   `docs/prereg.md`. Those are out of scope.
>
> **What to do first.** Re-read `docs/design.md`, `docs/prereg.md`,
> `docs/ai-usage-disclosure.md`, `prompts/00-original-spec.md`,
> `case-study/README.md`, and `reviewer-logs/README.md`. Then propose a
> session plan as a commit on `case-study/docs/session-plan.md` and
> begin.

## Status

This file is **closed for edits**. If the kickoff prompt needs to change
between attempts at the case study, a new file `01-layer1-pipeline-v2.md`
is added; the predecessor stays in place.
