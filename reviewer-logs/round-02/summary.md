# Round 2 — Summary

**Round**: 02
**Date**: 2026-05-21
**Manuscript reviewed**: case-study/manuscript/main.tex at git HEAD post-commit d7b9918.

## Reviewer verdicts

| Reviewer    | Verdict   |
|-------------|-----------|
| Methods     | accept    |
| Clinical    | accept    |
| Biostat     | accept    |
| Editor      | accept    |

**Round-2 closes with unanimous accept.**

## Per-reviewer Round-1 resolution summary

- Methods: 8 of 9 R1 comments resolved; #9 (uv.lock) deferred to tag time.
- Clinical: all 9 R1 comments resolved.
- Biostat: all 10 R1 blockers / high / medium / low comments resolved.
- Editor: 9 of 10 R1 comments resolved; #5 (tag placeholder) deferred to tag time.

## Remaining Round-2 comments (all low or medium, none blocking)

- Methods #1: add Limitations note on signature instability (Jaccard 0.20).
- Methods #2: state landmark-AUC vs Uno-IPCW heuristic.
- Clinical #1: DCA's clinical-utility band is narrow (treat-all > combo at p_t=0.10).
- Clinical #2: plain-language IDI interpretation.
- Biostat #1, #2: optional IBS and tau-sensitivity for Uno C.
- Editor #1, #2, #3: cover letter polish; TRIPOD checklist; reference-format spot-check.

These are minor; they would all be picked up in a Round 3, but the closure rule of "all four reviewers return verdict: accept" is satisfied.

## Disposition

Round 2 closes. The next tag is case-study-v1.0.0 unless the operator (or a Round 3 reviewer-loop run) opts to fold the Round-2 low/medium comments before tagging.

To honour the "minor bumps per round" versioning rule in docs/design.md, this closing round tags as case-study-v1.0.0 (first MAJOR.MINOR.PATCH release; subsequent rounds would bump MINOR).
