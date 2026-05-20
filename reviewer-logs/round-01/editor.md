# Round 1 — Editor Reviewer (JCO CCI)

**Round**: 01
**Reviewer**: Target-journal Editor (per `prompts/03-reviewer-editor.md`)
**Date**: 2026-05-21
**Target journal**: JCO Clinical Cancer Informatics
**Reviewed artefacts**: `case-study/manuscript/main.tex`,
`case-study/manuscript/JOURNAL.md`, `case-study/manuscript/cover-letter.md`,
`case-study/manuscript/references.bib`,
`docs/ai-usage-disclosure.md`.

## Overall impression

Triage-relevant items are mostly in order: TRIPOD reporting is
referenced, an AI-usage disclosure is present in the Acknowledgements
and Methods, ORCID is provided, data and code availability are stated,
preregistration is referenced. The scope fit is borderline. The
manuscript reads as a TCGA-LIHC + one external cohort prognostic-
model paper, which is a recognisable JCO CCI submission shape, but
the methodological novelty bar is not screamingly clear — the
contribution is "the same Cox-on-TCGA pipeline that has been done
many times, but with a fully reproducible Layer-1-internal preregistered
optimism-correction". That contribution may not pass JCO CCI triage
on novelty alone.

## Comments

### Comment 1 [BLOCKER] — Scope-fit framing in the Introduction is weak for JCO CCI

JCO CCI's remit (from `ascopubs.org/journal/cci`) is "biomedical
informatics methods and processes applied to cancer-related data".
The contribution here, as currently framed, is a 50-gene Cox prognostic
score with one external null. JCO CCI has published several HCC and
liver-cancer prognostic papers in 2023-2024; the manuscript needs to
clearly state **what is methodologically novel** within JCO CCI's
prior 3 years of publications. Options:

(a) The fully-reproducible optimism-correction-plus-platform-intersect
rebuilding contract is the informatics contribution — make this
explicit in the Introduction and re-emphasise in the Discussion.
(b) The prereg-v1 / prereg-v2 / prereg-v3 transparent amendment
trail is the informatics contribution — but if you make this claim,
you're effectively writing a methods paper and the empirical results
become illustration; the manuscript would need a methods-paper framing.
(c) The Viewpoint manuscript pointing to this case study makes the
methodological argument; if so, the case-study manuscript should
position itself as supplementary illustration and not claim novelty
on its own. **Then JCO CCI is the wrong venue**; the case-study
manuscript shouldn't be submitted as a stand-alone paper.

I lean toward (a) and ask for a clear novelty statement in the
Introduction. If you cannot articulate one in two sentences, consider
withdrawing this as a stand-alone submission.

Severity: blocker.

### Comment 2 [HIGH] — Body-word count is within limit but very margin-tight

`texcount` reports 2,344 words of body text. JCO CCI's cap is 3,000.
Comfortable margin. **However**, addressing the methods reviewer's
high-severity comments (standardisation contract, paired-optimism
formula) and the biostatistics reviewer's blockers (Uno C, calibration
plot, IDI, Schoenfeld for stage covariate) will add 200-400 words.
You will end up at ~2,700-2,800. Acceptable but borderline. Watch this.

Severity: high (planning item).

### Comment 3 [HIGH] — Reference count: 22 references, all resolvable

I spot-checked the references against PubMed: Hoshida 2008 NEJM
(PMID 18923165), Boyault 2007 Hepatology (PMID 17187432), Roessler
2010 Cancer Res (PMID 21159642), Calderaro 2019 J Hepatol (PMID
31195064), Singal 2023 AASLD HCC guidance (PMID 37199193), Llovet
2021 Nat Rev Dis Primers (PMID 33479224), Forner 2018 Lancet (PMID
29307467) — all resolvable. The TRIPOD-AI 2024 BMJ reference cites
"BMJ 385:e078378"; verify the exact volume / e-locator number
matches the BMJ-published version (the BMJ catalog uses the e-locator
form for online-first papers; the citation is correct as best I can
tell).

Severity: high (verification, not change). Required: one final PubMed
sweep before submission.

### Comment 4 [HIGH] — AI disclosure language: confirm it satisfies the ASCO journals policy

The Acknowledgements paragraph + the AI Usage Statement in Methods
together disclose: tool name and version (Anthropic Claude Opus 4.7,
1M-context), use cases (drafting, code, reviewer orchestration),
exclusions (no AI for figures, no AI for clinical interpretation), and
author validation. This matches the ASCO journals' policy
(manusights.com/blog/journal-of-clinical-oncology-ai-policy). The
statement also points to `docs/ai-usage-disclosure.md` for the long-
form log.

**One additional item**: the ASCO policy requires the author to
confirm they reviewed all AI-generated content. Add one sentence:
"The author reviewed and validated all AI-generated text, code, and
interpretations before submission."

Severity: high.

### Comment 5 [HIGH] — Data and Code Availability: tagged release identifier is a placeholder

The Data and Code Availability section says "tagged release
\texttt{case-study-vX.Y.Z}". For submission this needs to be a
concrete tag (case-study-v1.0.0 once reviewer rounds close). Track this.

Severity: high (planning item, not a current revision).

### Comment 6 [MEDIUM] — Reference style: AMA superscript numeric

The natbib preamble uses `[numbers,super,sort&compress]`. The
manuscript's first reference is `villanueva2015hepatocellular` (the
year mismatch in the bib entry is intentional? — title says 2015 but
the citation in the bib is to 2019; **double-check**). The unsrtnat
.bst is used; the rendered citations should be Vancouver-superscript-
numeric. Spot-check one or two in the final PDF.

Severity: medium.

### Comment 7 [MEDIUM] — Cover letter language: positioning vs claim

The cover letter (`case-study/manuscript/cover-letter.md`) needs to
be aligned with the Discussion's "illustrative, not for clinical use"
caveat. A cover letter that overclaims will trigger a desk-reject. I
do not see the cover letter framing the manuscript as illustrative;
add a sentence in the cover letter that aligns with the manuscript's
limitations.

Severity: medium.

### Comment 8 [LOW] — Figure count: 4 figures, within JCO CCI's 5-display-item limit

Within budget. The proposed calibration plot from the biostat reviewer
would bring this to 5; still within budget.

Severity: low.

### Comment 9 [LOW] — Plain-language summary

JCO CCI does not strictly require a plain-language summary for
Original Reports but it is encouraged. The Discussion's first
paragraph is close to one; consider moving 70 words to a labeled
"Plain-language summary" subsection at the top of the manuscript.

Severity: low.

### Comment 10 [LOW] — Title length and discoverability

Current title is 24 words. JCO CCI accepts long titles, but PubMed
display truncates at ~120 characters. The current title is 184
characters. Consider shortening to ~14-16 words: "Optimism-Corrected
50-Gene Transcriptomic Score Refines OS Beyond AJCC Stage in HCC
(TCGA-LIHC)". Optional.

Severity: low.

## Verdict

**`major-revision`**.

The novelty-positioning question (Comment 1) is the editorial blocker:
without a clear statement of methodological contribution, JCO CCI
triage will return this. The AI-disclosure language tweak (Comment 4)
is required for the journal's policy. The other items are tractable
within one revision cycle.
