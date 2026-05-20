# `02-layer2-audit.md` — Layer 2 Audit Subagent Kickoff

**Protocol artefact.** Verbatim kickoff prompt for the sealed Claude Code
session that audits Layer 1's committed output. Issued once. No
contact between Layer 1's session and Layer 2's session is permitted by
the honesty contract.

## Preamble

- **Model**: Anthropic Claude `claude-opus-4-7` (1M-context variant) via
  the Claude Code CLI; **a separate, fresh session** from Layer 1.
- **Snapshot date**: planned for the day Layer 2 is dispatched.
- **Tool envelope**: Read, Bash (read-only mode: no writes to repository
  files outside `reviewer-logs/audit/`), WebFetch (Crossref / PubMed
  resolution), MCP `claude_ai_PubMed`.
- **Session boundary**: starts at kickoff; ends when
  `reviewer-logs/audit/findings.md` is committed with the closure tag
  per `reviewer-logs/README.md`.

## Prompt (verbatim)

> You are running Layer 2 of the architecture described in
> `docs/design.md`. You are a sealed Claude Code session with **no
> exposure** to Layer 1's reasoning. You see only the committed final
> state of the repository at tag `case-study-v1.0.0` and the chronological
> commits behind it. You may not modify any file outside
> `reviewer-logs/audit/`.
>
> Your mandate is to perform four audit checks and write findings.
>
> 1. **Re-execution check.** From a clean clone of the repository at the
>    target tag, run `uv sync` and execute the case-study analysis
>    scripts in order (`case-study/analysis/01_prepare_data.py` through
>    `04_figures.py`). Capture the full stdout/stderr in
>    `reviewer-logs/audit/reexec.md`. Diff the regenerated artefacts in
>    `case-study/data/results/` against the committed versions where
>    feasible. Record concordance, discrepancies, and any environment
>    sensitivities. If a script fails, the failure is the finding; do
>    not patch the code.
>
> 2. **Citation veracity check.** For every BibTeX entry in
>    `case-study/manuscript/references.bib`, resolve the DOI or the
>    title via Crossref and PubMed. Record per-entry: resolved /
>    unresolved / wrong-target-resolved. Cross-link unresolved or
>    wrong-target entries to the manuscript passage that cites them.
>    Output to `reviewer-logs/audit/citations.md`.
>
> 3. **Statistical reproducibility check.** Re-derive the headline
>    statistics in the case-study manuscript (Cox model HR, C-index,
>    log-rank p, calibration slope, IDI where applicable) from the
>    regenerated intermediate artefacts. Tolerance: relative difference
>    <= 1e-3 for deterministic quantities, bootstrap-CI overlap for
>    random quantities. Output to `reviewer-logs/audit/statistics.md`.
>
> 4. **Claim-vs-data alignment check.** For each quantitative claim in
>    the case-study manuscript text, locate the analysis script line
>    and the result file that produced it. Record any claim that
>    cannot be traced. Output to `reviewer-logs/audit/claim_alignment.md`.
>
> Consolidate all four into `reviewer-logs/audit/findings.md`. The file
> contains, per finding, the location, the severity (low / medium /
> high / blocker), and a one-paragraph statement of fact. You do not
> recommend fixes; you state findings.
>
> **Hard constraints.**
>
> - You may not edit `case-study/`, `manuscript/`, `prompts/`, `docs/`,
>   or any file outside `reviewer-logs/audit/`.
> - You may not contact Layer 1's session or read Layer 1's
>   chain-of-thought (it is not in the repository).
> - You may not silently fix issues. Findings are findings.
> - You may not run external data downloads except through Crossref and
>   PubMed APIs for citation verification, and through the documented
>   download recipes in `case-study/analysis/01_prepare_data.py` for the
>   re-execution check.
> - Honesty contract from `docs/design.md` is binding.
>
> **Closure.** Audit closure is when `reviewer-logs/audit/findings.md`
> reports on all four checks. Commit the consolidated `findings.md` and
> exit the session.

## Status

Closed for edits. Successor versions live in `02-layer2-audit-v2.md` and
keep the predecessor in place.
