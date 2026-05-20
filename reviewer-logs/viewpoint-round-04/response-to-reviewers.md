# Round 4 Closure — Viewpoint manuscript

Manuscript: "The prompt is the protocol: a disclosure standard for clinician-investigators using agentic large language models", Lancet Digital Health Viewpoint.

## Round 4 verdicts

**UNANIMOUS ACCEPT.**

| Reviewer | Round 1 | Round 2 | Round 3 | Round 4 |
|----------|---------|---------|---------|---------|
| policy   | major-revision (12 comments) | minor-revision (3 new low) | **accept** | **accept** |
| clinician | major-revision (8) | minor-revision (3 new low) | **accept** | **accept** |
| methodology | major-revision (11) | minor-revision (3 new low) | **accept** | **accept** |
| editor | revise-first (13) | minor-revision (3 new low; "send out now? Yes") | **accept** | **accept** |

User-spec requirements:
- "At least four rounds" ✅
- "Until all reviewers ACCEPT" ✅ (unanimous in R3, reconfirmed in R4)

## Round 4 confirmation findings

- **Policy.** R1 blocker (verbatim Lancet quotes), R1 highs (reviewer-AI symmetry; 90-day pilot; equity; forward-reference resolution) and R1 mediums (audit-log split; placeholder cleanup; literal-vs-sympathetic framing; distributional reproducibility falsifier) all intact at HEAD. R2 minors closed in v0.4.1; v0.4.2 word-count refresh did not regress any policy claim.
- **Clinician.** Workflow realism, operator-expertise calibration (haematology and medical oncology fellow), negative-result commitment (both Layer-3 branches pre-written), and tone calibration all intact. Layer-3 placeholders correctly preserved pre-Layer-3-execution.
- **Methodology.** release_check.sh: 28 passed, 1 failed (working-tree-clean — operator-step at tag), 1 warned (Layer-2 audit log — operator-step at submission). Three R3 false positives all corrected. Ledger regenerator confirmed deterministic across three consecutive runs (SHA-256 byte-identical).
- **Editor.** "Would you send this out now? Yes." Body word count 2,428 / 2,500 ceiling; references 14 / 30; displays 2 / 2; title page and cover letter internally consistent. Zero blocking issues.

## Operator-step items at submission day

These are the only items still pending; none are in-manuscript and none affect reviewer verdicts.

1. medRxiv preprint posting and DOI.
2. Zenodo concept DOI (after GitHub-Zenodo integration trigger at tag push).
3. Cover letter: submission date + four suggested-reviewer names with affiliation/ORCID/email.
4. Live Lancet Digital Health IFA re-verification (returned HTTP 403 to research IPs throughout all four rounds; operator must verify from an institutional IP on submission day).
5. April 2026 LDH "agentic AI colleague" editorial DOI confirmation (editor R3 nudge; not blocking).
6. GitHub branch-protection on `main` (operator commitment in `docs/design.md` at tag push).
7. Make repository public at the moment the medRxiv preprint is posted (the Viewpoint's central self-demonstration claim requires the repository to be inspectable at submission).
8. Submit to Editorial Manager: https://www.editorialmanager.com/landig/

## Bottom line

The Viewpoint manuscript is structurally ready for submission to *The Lancet Digital Health*. The repository at `viewpoint-v1.0.0` is the artefact the manuscript's Disclosure 2.0 self-demonstration argument depends on; every item of the six-item manifest is present and audited.
