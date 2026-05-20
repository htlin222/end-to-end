# Response to Round 1 Reviewers — Viewpoint manuscript

Manuscript: "The prompt is the protocol: a disclosure standard for clinician-investigators using agentic large language models", submitted to *The Lancet Digital Health* as a Viewpoint.

Round 1 verdicts received (per `decisions.json`):
- **policy** — `major-revision` (12 comments)
- **clinician** — `major-revision` (8 comments)
- **methodology** — `major-revision` (11 comments)
- **editor** — `revise-first-before-external-review` (13 comments)

This document maps each comment to the specific commit that addresses it. The git history is the substrate; the commit message of `da4ddce manuscript: v0.4 ...` is the long-form narrative response. Reviewer subagents in Round 2 should treat this file as the formal response and use it to triage which comments to verify.

## Cross-reference table

Severity legend: B = blocker, H = high, M = medium, L = low. Status: ✓ addressed in v0.4, ◐ partially addressed (operator-step remaining), ✗ not addressed (with reason).

### Policy reviewer

| # | Sev | Summary | Status | Where |
|---|-----|---------|--------|-------|
| 1 | B | Policy mis-quotation (3 places) | ✓ | `main.tex` §1, Lancet wording verbatim; image generation and reviewer-AI separated |
| 2 | H | Symmetry argument omits reviewer-AI prohibition | ✓ | `main.tex` §6 recommendation 3 (cites prohibition; reframes as bilateral) |
| 3 | H | Implementability — no Editorial Manager path | ✓ | `main.tex` §6 recommendation 1 (90-day pilot via PDF + Zenodo) |
| 4 | H | Equity dimension absent | ✓ | `main.tex` §3 (minimum viable manifest) + §5 (equity counter-argument) |
| 5 | H | Self-undermining: reviewer-logs/round-01/methods.md cited as empty | ✓ | `main.tex` §5 rewritten to cite the actual Viewpoint Round 1 artefact-drift finding; docs/disclosure2-schema.json and docs/ledger.md committed |
| 6 | M | Authorship-exclusion reinforcement undersold | ◐ | Acknowledgements adds explicit "No AI tool is listed as an author"; further §6 sentence deferred |
| 7 | M | Audit log conflates three operations | ✓ | `main.tex` §3 item 5 split into 5a re-execution, 5b citation veracity, 5c headline-statistic rederivation |
| 8 | M | Reference list placeholders | ✓ | `references.bib` repoprereg SHA filled (`88d6d15`); lintom2026, linehs2024 retained with verification notes |
| 9 | M | "Read literally vs sympathetically" framing | ✓ | `main.tex` §1 names the three specific harms with documented illustrations |
| 10 | L | Cite AMEE Guide and cross-journal comparator | ✗ | Reference ceiling pressure; non-blocking, deferred to Round 2 if needed |
| 11 | L | ARS citation is fragile (GitHub) | ◐ | Comparator citation retained; companion peer-reviewed reference deferred |
| 12 | L | "Distributional reproducibility" needs operational definition | ✓ | `main.tex` §5 specifies the falsifier (selected sub-claim and statistical method across three runs; effect size within bootstrap CI) |

### Clinician reviewer

| # | Sev | Summary | Status | Where |
|---|-----|---------|--------|-------|
| 1 | H | "Board-certified medical oncologist" overstates record | ✓ | `main.tex` §4 rewritten as "haematology and medical oncology fellow"; cover letter same |
| 2 | H | Disclosure 2.0 burden unrealistic | ✓ | Minimum viable manifest + equity paragraph |
| 3 | H | Negative-result commitment rhetorical | ✓ | `main.tex` §4 carries both branches (positive and null) of the Layer-3 sentence pre-written; Layer 3 executes once at release |
| 4 | M | No clinical decision stated | ✓ | `main.tex` §4 closes with explicit "case study is illustrative of the workflow, not of clinical utility; no decision threshold proposed" |
| 5 | M | Tone calibration | ✓ | Set-notation removed; "operator-sovereign autonomy" → "fully autonomous workflows"; §8 closer softened |
| 6 | M | Workflow description elides restarts | ✓ | `main.tex` §1, §4 distinguish domain vs orchestration prompts; failure-mode-01 restart cited |
| 7 | L | Cover letter LLM prior work mention | ✓ | Cover letter "Generative-AI background of the author" paragraph |
| 8 | L | Name figure scripts | ✓ | Acknowledgements names `manuscript/figures/build_fig1.py` and `build_fig2.py` |

### Methodology reviewer

| # | Sev | Summary | Status | Where |
|---|-----|---------|--------|-------|
| 1 | B | Distributional-reproducibility falsifier unspecified; `99_reexec_check.py` missing | ◐ | `main.tex` §5 specifies the falsifier and the downgrade behaviour if Layer 1 does not ship the script. Script itself is Layer 1's responsibility and is expected at `case-study-v1.0.0` |
| 2 | H | Three-layer separation enforced by honour only | ✓ | `main.tex` §5 acknowledges the seal is testimonial; session-launch attestation named |
| 3 | H | Honesty contract rules behavioural | ✓ | `main.tex` Limitations names which rules are mechanically vs procedurally enforced |
| 4 | H | Citation hallucination defence partial | ✓ | `main.tex` §3 audit log split (5b citation veracity explicitly requires DOI + author list + journal + year + in-text claim-to-source alignment) |
| 5 | B | `docs/ledger.md` does not exist | ✓ | Committed in separate commit; `scripts/regenerate_ledger.py` ships the generator |
| 6 | M | Model deprecation named and dropped | ✓ | `main.tex` §5 last paragraph + Limitations name the deprecation policy |
| 7 | M | Zhao et al. corpus-scale audit not cited | ✓ | `references.bib` `zhaoHallucinations2026` added; `main.tex` §2 cites it |
| 8 | M | Reviewer-loop non-determinism not acknowledged | ✓ | `main.tex` Limitations names it |
| 9 | M | `docs/disclosure2-schema.json` does not exist | ✓ | Committed in separate commit |
| 10 | M | Layer-2 seal is testimonial | ✓ | `main.tex` §5 names this and the attestation file |
| 11 | M | Failure preservation rule partially violated | ◐ | Acknowledged in v0.4 narrative; explicit design.md carve-out for intentionally-overwritable artefacts deferred to next docs/design.md update |

### Editor reviewer

| # | Sev | Summary | Status | Where |
|---|-----|---------|--------|-------|
| 1 | B | Unresolved `<<WORDCOUNT>>`, `<<REFCOUNT>>`, `<<HEADLINE>>` placeholders | ✓ | Title page now carries 2 281 / 14 / 2; headline is the conditional pre-written prose |
| 2 | B | Cover letter `<<INSERT...>>` placeholders | ◐ | Word/ref/display counts filled; medRxiv and Zenodo DOIs remain operator-step at submission |
| 3 | H | Positioning against April 2026 Lancet DH agentic-AI editorial missing | ✓ | `main.tex` §1 opening cites Zou & Topol 2025 Lancet editorial; deployment-vs-manuscript-preparation distinction explicit |
| 4 | M | Key Messages reorder | ✓ | New ordering: clinician-assembly + Disclosure 2.0 + self-demonstration + Co-Scientist comparator |
| 5 | H | Methods-equivalent AI disclosure missing | ✓ | Added to Search-strategy panel as a "AI use in this Viewpoint" subsection |
| 6 | M | Explicit "Role of the funding source" missing | ✓ | Added to title-page metadata |
| 7 | M | Reporting-guideline declaration missing | ✓ | `main.tex` §4 (TRIPOD 2015 + STROBE) |
| 8 | — | Verify live IFA on submission day | ◐ | Operator step; flagged in JOURNAL.md submission checklist |
| 9 | — | vancouver.bst superscript visual check | ✓ | Compile produces superscript numerics (confirmed; PDF p.\,3 and onwards) |
| 10 | M | Section 5 trim ARS | ✓ | Trimmed to <80 words; star count and feature enumeration removed |
| 11 | M | Bullet 4 tighten | ✓ | New ordering renders bullet 3 (former bullet 4) at 35 words |
| 12 | — | Zenodo concept-DOI | ◐ | Operator step at release-tag |
| 13 | — | "No AI tool is listed as an author" | ✓ | Acknowledgements explicit |

## Outstanding operator-step items (not addressable in this revision pass)

These are intentionally left for the submission release moment:

1. medRxiv DOI (post preprint posting; ~3 business days after release tag).
2. Zenodo concept DOI (post GitHub-Zenodo integration trigger).
3. Cover-letter suggested-reviewer names with affiliation / e-mail / ORCID.
4. `case-study/analysis/99_reexec_check.py` (Layer 1's responsibility at `case-study-v1.0.0`).
5. `reviewer-logs/audit/session-launch.json` (Layer 2's responsibility when Layer 2 is dispatched).
6. Live Lancet DH IFA re-verification (operator step on submission day).

## Outstanding low-priority items deferred

These are non-blocking; the operator commits to revisiting them if Round 2 verdicts raise them again:

- AMEE Guide No.192 citation and cross-journal comparator (policy C10).
- Peer-reviewed companion citation to ARS (policy C11).
- Explicit `docs/design.md` carve-out for intentionally-overwritable artefacts (methodology C11).
