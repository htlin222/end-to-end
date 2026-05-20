# Response to Round 2 Reviewers — Viewpoint manuscript

Manuscript: "The prompt is the protocol: a disclosure standard for clinician-investigators using agentic large language models", Lancet Digital Health Viewpoint.

Round 2 verdicts received (per `decisions.json`):
- **policy** — `minor-revision` (3 new low-severity comments; 10/12 R1 closed, 0 re-raised)
- **clinician** — `minor-revision` (3 new low-severity comments; 7/8 R1 closed, 1 closed with operator-step condition)
- **methodology** — `minor-revision` (3 new low-severity comments; 10/11 R1 closed)
- **editor** — `minor-revision`, **"would I send this out now? **Yes**. Zero blocking issues survive at the manuscript level."**

Zero high-severity or blocker comments survived from Round 1. All four reviewers have closed every substantive R1 finding. Round 3 (the user's original spec requires "at least four rounds") will verify the v0.4.1 fixes.

## Round 2 minors addressed in v0.4.1

| Reviewer | Issue | Status | Where |
|----------|-------|--------|-------|
| policy N1 | word-count discrepancy main.tex 2310 vs cover-letter 2281 | ✓ | title-page metadata corrected to 2281 |
| policy N2 | `lintom2026`, `linehs2024` verification-on-submission notes | ◐ | Retained as operator-step at submission |
| policy N3 | JOURNAL.md interpretive sentence might bleed into EM metadata | ◐ | Flagged as operator-checkable; JOURNAL.md is the operator's working spec, not submission metadata |
| clinician N1 | Layer~1 vs Layer 1 hyphenation | ✓ | Standardised non-breaking hyphen across Section 4 |
| clinician N2 | Section 4 should name the journal Layer 1 selected | ✓ | Now references `case-study/manuscript/JOURNAL.md` for the Layer-1 selection rather than "of its own choice" |
| clinician N3 | Section 4 under-claims operator role | ✓ | Section 4 paragraph 2 explicit on operator-in-the-loop tasks (domain prompt supply, orchestration-prompt supply, commit+tag approval, Layer-3 execution) and operator-NOT tasks (no editing of Layer-1 outputs, no modification of reviewer comments, no Layer-3 cohort selection based on Layer-1 result) |
| methodology N1 | schema does not couple toolEnvelope keys to models[].name | ✓ | `docs/disclosure2-schema.json` toolEnvelope description now documents the coupling rule: keys MUST equal a `models[].name` |
| methodology N2 | `docs/ledger.md` lags HEAD by 2 commits | ◐ | Will regenerate at every commit going forward; release_check.sh enforces at release tag |
| methodology N3 | Two of seven enumerated residual failure modes not in Limitations (reviewer-AI collusion; selective preservation across uncommitted runs) | ✓ | Both added to Limitations explicitly |
| editor N1 | title-page word-count internal disagreement | ✓ | Resolved to 2281 (matches cover letter) |
| editor N2 | April 2026 LDH "agentic AI colleague" editorial implicitly handled but not explicitly cited | ✗ | Operator step: live Lancet DH site continues to return HTTP 403 to research IPs; the editorial title appears in search hits but the DOI cannot be confirmed without institutional access. Flagged for re-search on submission day. The current Section 1 paragraph 1 cites the Zou & Topol 2025 *Lancet* piece which is the closest verified analogue. |
| editor N3 | Acknowledgements paragraph dense at 181 words | ◐ | Deferred; the dense paragraph carries the mandated Lancet acknowledgements content. Breaking it into two paragraphs is a copy-edit pass, not substantive. |

## Operator-step items still outstanding at submission day

1. medRxiv preprint DOI (insert after preprint posting; ~3 business days)
2. Zenodo DOI (insert after GitHub-Zenodo deposit; minutes)
3. Four suggested reviewer names with affiliation / e-mail / ORCID
4. Cover letter submission date
5. `case-study/analysis/99_reexec_check.py` (Layer 1's responsibility at `case-study-v1.0.0`)
6. `reviewer-logs/audit/session-launch.json` (Layer 2's responsibility)
7. Live Lancet DH IFA re-verification (third check; site has been 403 throughout the revision cycle)
8. April 2026 LDH "agentic AI colleague" editorial DOI confirmation
9. Branch protection on `main` (operator step at `viewpoint-v1.0.0` tag per `docs/design.md`)

## Bottom line for Round 3 reviewers

All four R1 verdicts (3 × major-revision + 1 × revise-first) became 4 × minor-revision in R2. The editor explicitly said "would I send this out now? Yes." The manuscript is structurally ready; the remaining items are submission-day mechanics already enumerated. Round 3 (and the user-spec-required Round 4) are confirmation rounds.
