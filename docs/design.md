# Design — `end-to-end`

A single-operator agentic-research demonstration packaged as a submission to
*The Lancet Digital Health* (Viewpoint).

## What this repository is

This repository is two things at once.

1. **A Viewpoint manuscript** (`manuscript/`) that argues current journal AI
   policies have not caught up with the operating reality of clinician-
   investigators. The Viewpoint proposes a new disclosure standard whose
   minimum unit is **prompt + commit hash + tagged release**, not the
   classical methods-section narrative.

2. **The empirical artefact that the Viewpoint advocates for** (`case-study/`,
   `reviewer-logs/`, `prompts/`, `docs/`). Everything that the proposed
   disclosure standard would require is materialised in this repository, with
   nothing redacted and no post-hoc curation. The Viewpoint is published *by
   virtue of* demonstrating compliance with the standard it proposes.

The medium is the message. A reader cannot evaluate the Viewpoint without
inspecting the repository it is bundled with. A reviewer who accepts the
Viewpoint endorses the methodology; a reviewer who rejects it must do so on
grounds that the repository itself disproves or the disclosure standard fails
to address.

## The three-layer architecture

The case study (`case-study/`) was produced through three deliberately
separated layers. Mixing layers breaks the integrity claim; this design
document records the separation rules so they can be audited.

### Layer 1 — Pipeline (the subject)

A single Claude Code session, kicked off with the operator-supplied
orchestration prompt in `prompts/00-original-spec.md`. The session received
exactly one domain input ("use TCGA-LIHC + public GEO cohorts to refine HCC
overall-survival stratification beyond BCLC stage"). It selected its own
sub-claim, designed its own analysis, drafted its own LaTeX manuscript, and
ran its own reviewer-subagent loop. **Zero human intervention** between
kickoff and the `case-study/v0.x` release tag.

Failures, deadends, hallucinated citations, and revisions are all preserved
in the git history of `case-study/`. The integrity rule is asymmetric: Layer
1 may fail, but its trail may not be edited after the fact.

### Layer 2 — Audit (the observer)

A separate, sealed Claude Code session with no exposure to Layer 1 except
through the final committed repository state. The audit transcript lives in
`reviewer-logs/audit/`. It performs:

- **Re-execution**: clean clone, `uv sync`, run every `analysis/*.py` from
  scratch. Verify that committed result files match regenerated ones.
- **Citation veracity**: every BibTeX entry in `case-study/.../references.bib`
  resolved against Crossref / PubMed. Any non-resolvable citation is recorded
  as a Layer-1 failure mode, not silently fixed.
- **Statistical reproducibility**: Cox model coefficients, C-index, log-rank
  p-values reproduce within tolerance from the same seed.
- **Claim-vs-data alignment**: claims in the case-study manuscript text are
  cross-checked against what the code actually computes.

The audit cannot modify Layer 1 artefacts. It can only file findings, which
land in `reviewer-logs/audit/findings.md` and become part of the artefact
ledger.

### Layer 3 — External validation (the judge)

The single human (operator) step. Layer 1's final risk-score formula is
applied to two GEO cohorts (`GSE14520`, `GSE76427`) that Layer 1 never saw.
Reported metrics: Harrell's C-index, log-rank p, calibration slope, decision-
curve net benefit at clinically relevant thresholds.

The validation step is purely measurement. It does not select cohorts based
on the result. The two GEO cohorts and the metric set are preregistered in
`docs/prereg.md` **before** any of them is touched. If both cohorts produce
a null result, the null is reported and the Viewpoint discusses it.

## Honesty contract

These rules are binding for all contributors (human and AI).

1. **No claim screening.** Whatever Layer 1 produces is published in the
   case study, including a boring or wrong claim. The Viewpoint argument is
   that the *process* is auditable; cherry-picking the result would defeat
   the entire argument.
2. **No history rewriting.** No force-push, no `git rebase -i`, no
   `git commit --amend` after the first push of any commit. Mistakes are
   fixed with new commits whose messages name the prior mistake.
3. **Failure preservation.** Every reviewer-subagent round leaves a verbatim
   transcript in `reviewer-logs/round-XX/`, including rounds where the
   reviewers were wrong and the pipeline argued back. Negative reviewer
   findings are not deleted when later resolved.
4. **No post-hoc instrumentation.** Metrics not preregistered in
   `docs/prereg.md` are reported as exploratory and cannot be promoted to
   the headline finding.

### Procedural vs technical enforcement (Round 1 methodology comment 3)

A reviewer rightly observed that the four rules above are mostly
behavioural rather than mechanically enforceable. The honest map is:

| Rule | Enforcement |
|------|-------------|
| 1. No claim screening | Procedural; operator-trust dependent. The published artefact ledger lets a third party check whether late commits add or remove claims, but a single-operator pipeline cannot self-prove it never screened. |
| 2. No history rewriting | Mechanically enforceable via GitHub branch protection on `main` (forbid force-push, forbid history rewrites, require linear history). This is the one rule for which a technical guarantee is feasible; the operator commits to enabling branch protection at the `viewpoint-v1.0.0` tag and to documenting the configuration in `docs/branch-protection.md`. |
| 3. Failure preservation | Procedural. The repository preserves what is committed; nothing prevents an operator from not committing a particular failed run. The mitigation is that the operator-supplied orchestration prompts forbid uncommitted state at session end (Layer 1 kickoff prompt explicitly requires "commit after every substantive change"). |
| 4. No post-hoc instrumentation | Procedural; the preregistration commit's SHA is the immutable anchor. Adding outcomes after Layer 3 runs is detectable by diffing the prereg's commit content; promoting exploratory results to primary is detectable by comparing the manuscript's reported outcomes to the preregistration. |

The Viewpoint Section~5 ``A single operator cannot audit himself''
counter-argument names the seal as testimonial, not cryptographic, and
proposes a session-launch attestation
(`reviewer-logs/audit/session-launch.json`) as the minimum operational
evidence. Both the design doc and the Viewpoint acknowledge this is
short of cryptographic enforcement and would benefit from third-party
re-audit through the public release.

### Intentionally-overwritable artefacts (Round 1 methodology comment 11)

A small number of pipeline-side artefacts are designed to be
overwritten on the next pipeline run rather than preserved:

- `case-study/data/results/cohort-selection.json` — recomputed
  deterministically from the analysis scripts.
- `case-study/data/results/*.tsv` and `*.json` cache files produced
  by `case-study/analysis/01_prepare_data.py` and downstream scripts.

These are listed in `case-study/data/results/MANIFEST.md` (when Layer 1
ships it). The carve-out is operationally necessary because the
analysis scripts are idempotent and re-running them recomputes
intermediate state; preserving every intermediate would inflate the
release bundle without adding audit value. The honesty contract's
``failure preservation'' rule applies to reviewer transcripts, audit
findings, and operator-vs-AI commit boundaries, not to deterministic
intermediates that the audit re-execution layer recomputes on a clean
clone.

## Repository as artefact ledger

`docs/ledger.md` is the chronological narrative that backs Figure 1 of the
Viewpoint. It is generated from `git log --follow --all` plus
`reviewer-logs/*/summary.md`, regenerated on each release tag, and committed
back to the repository. The ledger is the single source of truth for the
"what happened, in what order, by whom (human or which agent)" claim that
the Viewpoint makes.

## Versioning convention

Tags follow `v<MAJOR>.<MINOR>.<PATCH>`.

- `MAJOR` bumps mark scientific pivots (e.g., the claim changed materially,
  or a Layer-1 failure invalidated an earlier finding).
- `MINOR` bumps mark reviewer-round revisions of the case-study manuscript.
- `PATCH` bumps mark typo and terminology fixes only.

Two parallel tag prefixes are used:

- `viewpoint-v<x>.<y>.<z>` — Viewpoint manuscript releases.
- `case-study-v<x>.<y>.<z>` — case-study manuscript releases.

The submission-ready Viewpoint tag bundles a frozen pointer to the
case-study tag it relies on; this pointer is recorded in
`manuscript/JOURNAL.md` under "Data and Code Availability".

## What this repository is *not*

- Not a system paper. The pipeline is not a software product. It is a
  workflow assembled from commodity tools (Claude Code, public datasets, R /
  Python, LaTeX).
- Not a benchmark. We do not compare against Co-Scientist or Sakana AI
  Scientist on accuracy. The argument is normative (disclosure), not
  competitive (performance).
- Not wet-lab validated. External validation is restricted to the two
  preregistered held-out GEO cohorts.
- Not a clinical decision-support tool. The HCC risk score in the case study
  is illustrative and is not intended for clinical use; the case-study
  manuscript states this explicitly.

## Reading order for reviewers

1. `manuscript/main.pdf` — the Viewpoint, 2500 words.
2. `docs/ai-usage-disclosure.md` — every AI tool, prompt and intervention.
3. `prompts/00-original-spec.md` — the operator-supplied orchestration prompt.
4. `case-study/manuscript/main.pdf` — Layer 1's autonomous output.
5. `reviewer-logs/round-01..04/` — the reviewer-loop transcripts.
6. `reviewer-logs/audit/findings.md` — Layer 2's audit findings.
7. `docs/ledger.md` — chronological artefact ledger (Figure 1 source).
