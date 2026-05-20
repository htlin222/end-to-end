# `prompts/` — Protocol Artefacts

This directory is the new minimum disclosure unit that the Viewpoint
manuscript argues should accompany every agentic-LLM-assisted study. It
contains the prompts used to orchestrate the three layers and the four
reviewer subagents.

Files in this directory follow a hard integrity rule: **once a prompt is
committed and used, it is not edited after the fact**. If a prompt needs
to change between rounds, a new file (`NN-name-v2.md`) is added; the
predecessor stays in place. This makes the prompt history immutable in the
same way the LaTeX history is.

## Inventory

| File                          | Role                                                     |
|-------------------------------|----------------------------------------------------------|
| `00-original-spec.md`         | The operator-supplied orchestration spec (verbatim).     |
| `01-layer1-pipeline.md`       | Layer 1 autonomous pipeline kickoff prompt.              |
| `02-layer2-audit.md`          | Layer 2 audit subagent prompt.                           |
| `03-reviewer-methods.md`      | Methods reviewer persona prompt.                         |
| `03-reviewer-clinical.md`     | Clinical (oncology / hepatology) reviewer persona.       |
| `03-reviewer-biostat.md`      | Biostatistics reviewer persona.                          |
| `03-reviewer-editor.md`       | Target-journal editor persona (Lancet Digital Health).   |

## Model-pinning and snapshot

Each prompt's preamble records:

- **Model identifier**: Anthropic Claude `claude-opus-4-7` (1M-context
  variant), accessed via the Claude Code CLI.
- **Snapshot date**: the YYYY-MM-DD when the prompt was first executed.
- **Temperature / sampling parameters**: default Claude Code values
  (temperature governed by the runtime; no explicit override unless noted).
- **Tool-use envelope**: which tools Claude was permitted to invoke
  (WebFetch, WebSearch, Bash, Read/Edit/Write, MCP servers, Agent
  dispatch).

The Viewpoint argues that the {prompt + model id + snapshot date + tool
envelope} tuple is the new disclosure minimum unit, replacing the
prose-only methods-section narrative. This directory is the operational
implementation of that argument.

## Re-execution caveats

LLMs are not bit-deterministic across runs even at identical parameters.
The Viewpoint manuscript discusses this explicitly and does not claim bit-
identical reproducibility. The reproducibility claim is **distributional
reproducibility**: re-running the same prompt against the same model id on
the same snapshot date with the same tool envelope produces an outcome
whose substantive findings are statistically indistinguishable.

The case study includes a small re-execution check in
`case-study/analysis/99_reexec_check.py` (planned), which re-runs Layer 1
three times and reports concordance on (a) selected claim, (b) chosen
statistical method, (c) headline effect size.
