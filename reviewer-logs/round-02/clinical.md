# Round 2 — Clinical Reviewer

**Round**: 02
**Reviewer**: Clinical (per `prompts/03-reviewer-clinical.md`)
**Date**: 2026-05-21
**Reviewed artefact**: `case-study/manuscript/main.tex` at HEAD post-
commit `d7b9918`.

## Overall impression

Big improvement on Round 1. The AJCC-vs-BCLC substitution is now
explicit in the abstract and the Introduction. The "resected, surgical-
candidate" framing is in the conclusion of the abstract. A plain-
language summary is present. The decision-curve analysis at 5-year
mortality thresholds 0.10/0.20/0.30 is now reported (figure 5,
`dca_metrics.json`). The "clinically meaningful" overstatement is
removed. Treatment-era confounding is one full paragraph. Aetiology
unavailability is documented.

I am close to accept; one item remains.

## Per-Round-1-comment status

| R1 ID | Status | Notes |
|-------|--------|-------|
| 1 (AJCC-vs-BCLC up-front) | resolved | Abstract conclusion includes it; Introduction has a dedicated sentence. |
| 2 (resected-only framing) | resolved | Abstract conclusion: "Findings apply to the resected surgical-candidate HCC population". |
| 3 (aetiology) | resolved | Methods states aetiology fields not available in the GDC clinical export used; Limitations notes this. |
| 4 (DCA) | resolved | Figure 5 + `dca_metrics.json` report Vickers-Elkin net benefit at 0.10/0.20/0.30. DCA shows the combo model net benefit slightly above treat-all at p=0.20 (delta NB ~ 0.007). The marginal NB delta is honestly reported. |
| 5 (treatment era) | resolved | Full paragraph in Discussion. |
| 6 ("clinically meaningful") | resolved | Replaced with "statistically detectable and meeting the prespecified Layer-1 threshold". |
| 7 (competing risks) | resolved | Discussion explicitly notes competing-risks limitation. |
| 8 (plain-language summary) | resolved | Present, 100-150 words. |
| 9 (cohort characteristics) | partial | A small table is not in the manuscript text; the manuscript references Methods for the cohort numbers. Acceptable. |

## New Round-2 comments

### Comment 1 [MEDIUM] — DCA delta vs treat-all is small and should not be over-claimed

The reported DCA shows combo NB = 0.364 at p=0.20 vs treat-all NB =
0.357 (delta 0.007). At p=0.10 the combo NB equals treat-all (the
score classifies everyone above 0.10). At p=0.30 the combo NB
(0.064) exceeds treat-all (0.018). The clinically interesting band
is between p=0.20 and p=0.30, where the combo offers a small but
measurable net benefit over treat-all-or-none.

The Results section reports the numbers but the Discussion should
add one sentence noting that the DCA's clinical-utility implication
is **narrow**: a clinician using the combo model would gain over
treat-all only at decision thresholds where the implicit harm-to-
benefit ratio exceeds ~0.25 (the slope from p_t = 0.20 onward), which
in HCC corresponds to surveillance- or adjuvant-decision contexts,
not transplant eligibility.

Severity: medium. One sentence in Discussion.

### Comment 2 [LOW] — IDI at 5 years is 0.18; interpret in clinical units

The reported Pencina IDI at 5y is 0.18 (95% CI 0.13-0.23). For a
clinical reader, "IDI 0.18" is dense. Add a parenthetical: "(i.e.,
average predicted 5-year mortality of events exceeds non-events by an
additional 18 percentage points when AJCC + \HCCRTS replaces AJCC
alone)". This translates the statistic.

Severity: low.

## Verdict

**`accept`**, conditional on Comment 1 being addressed in a minor
Discussion edit.

The clinical comments from Round 1 are resolved; Round 2 comments are
both about clinical-language interpretation and do not require
analytic re-runs.
