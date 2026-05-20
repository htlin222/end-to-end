# Round 1 — Summary

**Round**: 01
**Date**: 2026-05-21

## Reviewer verdicts

| Reviewer    | Verdict          |
|-------------|------------------|
| Methods     | major-revision |
| Clinical    | major-revision |
| Biostat     | major-revision |
| Editor      | major-revision |

Round-01 does NOT close. Round 2 is dispatched after revision.

## Cross-reviewer convergent issues

- Calibration plot at 1/3/5 y (biostat blocker, editor low) -> Figure 3 revision.
- Bootstrap-optimism estimator (methods high, biostat high) -> re-run with paired-optimism.
- AJCC-vs-BCLC framing (clinical high) -> abstract + Introduction.
- Decision-curve analysis (clinical high) -> new artefact + Figure addition.

## Next steps before round 2

1. Open case-study/docs/failure-mode-04-bootstrap-estimator.md
2. Patch case-study/analysis/02_build_risk_score.py to track c_ajcc_b
3. Add Vickers-Elkin DCA
4. Add Hosmer-Lemeshow calibration plot
5. Add Pencina IDI
6. Add Jaccard stability check
7. Manuscript rewrites per reviewer comments (see decisions.json)

This round and its decisions are committed; round 2 follows in a separate commit.
