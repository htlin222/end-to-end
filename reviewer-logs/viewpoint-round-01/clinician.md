# Viewpoint Round 1 — Clinician-Investigator Reviewer

- **Round**: 1
- **Reviewer**: clinician (clinician-investigator persona)
- **Date**: 2026-05-21
- **Manuscript commit**: c694f073ba1d802541718b8449cad02698d9b4cd
- **Files inspected**: `manuscript/main.tex`, `manuscript/JOURNAL.md`,
  `manuscript/cover-letter.md`, `docs/design.md`,
  `docs/ai-usage-disclosure.md`, `docs/prereg.md`,
  `prompts/00-original-spec.md`, `prompts/04-viewpoint-reviewer-clinician.md`.
- **External check**: `https://lin.hsiehting.com/cv/` (operator CV) via
  WebFetch, retrieved 2026-05-21.

## Overall impression

I read this Viewpoint as a clinician-investigator who keeps a Claude Code
window open beside the EMR and who has shipped an LLM preprint. The
proposal — replace the methods-section paragraph with a six-item manifest
plus a tagged release — is the right argument and it is the argument I
would want my journal to engage with. The manuscript is also unusually
honest about being its own working example, which is the most powerful
move available to a single-author Viewpoint without an RCT behind it.

That said, the draft has three problems that will hurt it at desk
triage and at clinician-reader plausibility:

1. The HCC case study is presented as a "domain-portability" feature
   when, on the operator's actual CV, it is closer to a *necessity*
   (the operator's own haematology dataset access is more constrained,
   and TCGA-LIHC is the canonical public-data on-ramp). The current
   framing reads as opportunistic post-hoc rationalisation. It is
   fixable, but only by owning the framing rather than dressing it up.
2. Disclosure 2.0's manifest is calibrated for a clinician-investigator
   who is already on git; that population is small. The Viewpoint does
   not engage seriously with what the proposal asks of an
   evening-and-weekend researcher who has never used `git tag` or
   Zenodo. This is the equity objection the Lancet DH board will raise
   first.
3. The treatment of negative results is rhetorically owned ("the null
   is the headline") but operationally hedged. The body refers to
   `<<HEADLINE:layer3_primary>>` as a placeholder, which signals the
   manuscript has not yet been written against an actual Layer 3
   outcome. Until that placeholder is filled with the real number and
   the prose adjusts to whatever the number is, the "we own negatives"
   commitment is unverified rhetoric. The clinical-reader test of
   honesty on negative results is whether the *headline sentence*
   changes when the result changes; the current draft cannot
   demonstrate that.

The tone is mostly calibrated for Lancet DH. There are local
swings — "operator-sovereign autonomy", "the medium is the message" in
the design doc, "the published unit becomes \{...\}" set-notation in
the abstract bullet — that read more techno-manifesto than digital-
health editorial. Specific lines are flagged below.

I am recommending **major revision**. The revision is achievable
within one cycle and does not require new data.

## Comments

### C1 [high] HCC framing reads opportunistic, not deliberate

The Viewpoint argues (Section 4, paragraph 1) that HCC was chosen to
establish "domain portability" away from the operator's clinical
specialty. On the operator's CV the operator is a Hematology & Medical
Oncology *Fellow* (per `lin.hsiehting.com/cv/`, retrieved 2026-05-21),
not yet an attending; published work is in HSCT outcomes in T-cell
lymphoma, G-CSF timing in CIN, and a high-flow nasal oxygen study;
the one LLM-adjacent paper is on theory-of-mind behaviour in poker
agents, not on clinical genomics. The Viewpoint, by contrast,
introduces the author (Section 4) as "a board-certified medical
oncologist whose published work is in hematologic malignancies",
which slightly overstates the publication record (one of four papers
is in hematology proper; the others are supportive-care or AI). A
sophisticated clinician-reader who pulls up the operator's CV — and
Lancet DH editors do — will read the current framing as opportunistic.

The fix is honesty about the actual mechanism: the operator
deliberately ran the case study outside his sub-specialty because
(i) hematology raw data behind firewalls is harder to release under
MIT than TCGA, and (ii) the cross-domain mismatch is genuinely the
sharper test of whether the workflow generalises. Both reasons are
defensible. State them in the manuscript. Drop the "board-certified
medical oncologist whose published work is in hematologic
malignancies" phrasing and replace with something like "a
haematology-oncology fellow whose published clinical work is in
hematologic malignancies and supportive care". This is more
calibrated to the actual record and stronger as a rhetorical move,
because a fellow successfully operating a cross-domain workflow is a
*more* surprising existence proof than an attending doing the same.

Action: rewrite the first paragraph of Section 4 ("Domain-portability
case study") and the third paragraph of Section 1 ("Why disclosure
needs a new minimum unit") accordingly.

### C2 [high] Disclosure 2.0 burden is unrealistic for the median target reader

The Viewpoint's six-item manifest demands: a git repository with
non-rewritten history, a tagged release, a Zenodo DOI, a sealed
audit-subagent transcript, reviewer-subagent transcripts per round,
a machine-readable manifest (Section 6, second recommendation), and
deterministic re-execution. The operator demonstrably can do this —
the repository is sitting under my cursor. But the population the
Viewpoint claims to serve ("clinician-investigators who do not work
in big-tech labs") is overwhelmingly composed of doctors who have
used GitHub once and who would not know how to push a tag. The
manuscript does not engage with this gap. Section 6's
"machine-readable manifest" recommendation actually deepens it.

In real 2026 clinician-investigator practice (mine and that of
colleagues running evening / weekend research), the friction stack
that kills these projects is not the LLM tooling, which is now
mature; it is exactly the artefact-management discipline Disclosure
2.0 mandates. The Viewpoint should either (a) name the equity cost
honestly and propose a tiered minimum (a "Disclosure 2.0 Lite"
acceptable to journals for a transition period), or (b) propose a
journal-supplied tooling pathway that the operator does not have to
self-build. Without one of these moves, the Lancet DH editorial
board will read the proposal as a standard built around the
operator's circumstances rather than for the population it names.

Action: add one paragraph to Section 5 ("Failure modes and
counter-arguments") on the equity-of-implementation objection, and
in Section 6 ("Recommendations"), explicitly distinguish a minimum
viable manifest (prompts + model id + commit hash + tagged release)
from the full six-item manifest.

### C3 [high] Negative-result commitment is unverifiable in this draft

Line 140 of `manuscript/main.tex` contains the template token
`\texttt{<<HEADLINE:layer3\_primary>>}`. This is the load-bearing
sentence of the entire Viewpoint: the place where the manuscript
reports what the Layer 3 external validation actually found. The
prereg (`docs/prereg.md`) commits the operator to reporting the
primary ΔC-index point estimate and CI here regardless of sign, and
the design doc commits to the null being the headline if the null
emerges. None of that is verifiable while the placeholder remains.
Worse, the surrounding prose is currently written in a register
("the case-study result, with its preregistered primary outcome
point estimate, CI, and the secondary-outcome table, is reported in
\dots") that reads as if the result is already known and is mildly
positive. A reviewer cannot tell whether the placeholder will be
swapped for "ΔC-index = 0.04 (95\% CI 0.01--0.07)" or "ΔC-index = 0.01
(95\% CI -0.02--0.04), null". The two cases require materially
different surrounding prose and a materially different position in
Section 7 (Limitations).

This is the single most important clinician-reader test of the
manuscript. Until the headline is filled and the prose around it is
rewritten *as if it had to be re-defended in front of a tumour
board*, the negative-result commitment is rhetorical, not held.

Action: do not submit until Layer 3 has executed, the headline
sentence carries the real number, and the prose of Section 4
paragraphs 3-4 and Section 7 has been rewritten conditional on what
the number is. If the null comes through, the Conclusion (Section 8)
should be rewritten to lead with the null. If the positive comes
through, Section 7 should explicitly warn that 357 pooled samples at
~0.6 power do not establish a clinical biomarker.

### C4 [medium] "Risk-stratification case study" without a stated clinical decision

The case study in its present form computes a C-index improvement
over AJCC pathologic stage on TCGA-LIHC + GEO. The Viewpoint frames
this as "OS stratification of hepatocellular carcinoma". A
clinician-reader will ask: stratification *for what decision*?
Surveillance interval? Adjuvant TACE? Transplant eligibility? The
Viewpoint should be explicit that the case study is illustrative of
the *workflow*, not of *clinical utility*, and that no decision
threshold has been chosen and no decision-curve net-benefit threshold
has been justified against a real clinical context. The current draft
gestures at this in Section 7 (Limitations) but not strongly enough.
The Section 4 paragraph 5 reading-instruction ("not to evaluate
whether the case study's risk score is the best HCC risk score") is
the right move; reinforce it by also stating "the case study does
not propose, and is not intended to support, any HCC clinical
decision".

Action: amend Section 4 paragraph 5 to explicitly state the case
study is not decision-supporting, and add a one-clause reminder to
the relevant Limitations sentence in Section 7.

### C5 [medium] Tone calibration — too techno-manifesto in places

Lancet DH publishes editorials read by clinicians, methodologists
and policy people. The current draft has local swings in register
that will read as too crypto-philosophical / techno-utopian for
that audience. Specific instances:

- Section 1, "the published unit becomes \{prompt, model identifier,
  tool envelope, commit history, reviewer-subagent transcripts,
  audit log\}". Set-notation in a Viewpoint prose paragraph is
  jarring. Render as a sentence: "the published unit becomes the
  prompts that produced the work, the model used to execute them,
  the tools the model was permitted to invoke, the commit history,
  the reviewer-subagent transcripts and the audit log, accessible at
  a tagged release."
- Section 5, "operator-sovereign autonomy" vs "copilot-supervised".
  "Operator-sovereign autonomy" is a phrase from the design-doc
  vocabulary; in a Lancet DH Viewpoint it reads as an in-group term.
  Replace with "fully autonomous workflows" or "operator-led
  autonomous workflows".
- Section 1 closing, "The 2026 question is no longer whether
  autonomous agentic research is feasible; it is what the published
  unit should look like when one occurs." Good sentence, but the
  preceding paragraph reads slightly breathless ("the first AI-
  authored paper to do so under blind review"). Trim the breathless
  framing; clinicians read these editorials with prior on hype-
  resistance.
- Section 8 (Conclusion), "Whatever the editorial decision, the
  artefact stands." This is the most techno-defiant sentence in the
  manuscript. Reasonable people read this as posture rather than
  argument. Soften to "The artefact remains in the public record
  regardless of the editorial decision; the substantive question for
  the field is whether the disclosure unit it embodies should
  generalise."

Action: line-edit Sections 1, 5 and 8 against the Lancet DH editorial
register.

### C6 [medium] Workflow description does not match real clinician-investigator practice in two places

I run this kind of workflow myself and the description in Sections 1
and 2 does not quite match what 2026 looks like at the desk:

- Section 1 paragraph 2: "The workflow takes a single domain prompt,
  scans the public literature, picks an under-mined dataset, drafts
  an analysis pipeline, executes it, drafts a manuscript matched to
  a target journal, iterates against four reviewer-subagent personas
  until unanimous acceptance, and stages a tagged release." In
  practice no clinician-investigator I know runs a session this
  linearly. There is at least one "the agent picked the wrong
  dataset, I killed the session, re-prompted" moment per project.
  The current sentence describes the ideal-case run, and a
  clinician-reader will pattern-match that as too clean. The
  manuscript should briefly acknowledge that the workflow includes
  operator-initiated restarts (the failure-mode-01 commit in this
  repo's case-study history is exactly such an instance — extend
  pool of GEO candidates after a first failure).
- Section 4 paragraph 2: "The pipeline received exactly one domain
  prompt \dots and produced \dots a tagged \texttt{case-study-v1.0.0}
  release." Same issue. The reader who clicks through to the repo
  history will find more than one prompt was involved (there are
  prompts `01..03` in `prompts/`). The "one prompt" sentence is
  defensible if it means "one domain prompt" as distinct from
  pipeline-orchestration prompts, but the current phrasing elides
  the distinction. Clarify.

Action: in Section 1 paragraph 2 and Section 4 paragraph 2, distinguish
"domain prompt" (one) from "orchestration prompts" (several, all
committed to `prompts/`), and add a single sentence acknowledging
operator-initiated restarts as part of the realistic workflow.

### C7 [low] Single LLM-related prior publication is thin grounding for the Viewpoint

The operator's prior LLM-related work is the arXiv preprint on
theory-of-mind-like behaviour in poker agents. That is a real
preprint and a defensible piece of grounding, but it is one preprint,
on a non-medical domain, with no Lancet-group track record. The
manuscript does not overclaim this — it cites the prior arXiv only
once, in the Search-Strategy panel — and I am not asking for an
overclaim. I am flagging it as a structural weakness an editor will
note. A single sentence in the cover letter naming the prior LLM
preprint as the operator's bona fide for opining on agentic LLM
practice would help; the current cover letter mentions Anthropic
subscription and lack of equity but does not mention prior LLM work.

Action: add one sentence to the cover letter under "Generative-AI
use" or under a new paragraph: "My prior LLM-adjacent work
(theory-of-mind-like behaviour in LLM poker agents, arXiv 2026)
informs this Viewpoint's framing of agentic-LLM disclosure." Keep
it factual; do not embellish.

### C8 [low] "All figures are produced by deterministic Python and R code" is checkable and should be made trivially checkable

The Acknowledgements (and the Methods-equivalent disclosure) commits
to deterministic, code-only figure generation. This is the correct
commitment. To make it trivially auditable, name the two figure-
generation scripts in the repository and reference them by path in
the Acknowledgements paragraph (e.g., `figures/fig1_ledger.py`,
`figures/fig2_policy_gap.py`). The reader who wants to verify the
"no AI-generated figures" claim can then `git blame` the script
and inspect for AI-pasting; current phrasing requires the reader
to go hunting.

Action: name the figure-generation script paths in the
Acknowledgements paragraph.

## Verdict

`major-revision`.

Acceptance requires resolving C1, C2 and C3, which together cover the
three things a clinician-investigator reading this Viewpoint will
test it against: is the cross-domain framing honest, is the
disclosure burden realistic for the named population, and is the
negative-result commitment real or rhetorical. C4, C5 and C6 are
necessary to clear desk triage at Lancet DH. C7 and C8 are
nice-to-haves that will tighten the manuscript.

I will accept in round 2 if (i) Layer 3 has been executed and the
real headline number sits in the manuscript, with prose calibrated
to that number; (ii) the HCC framing is rewritten as the operator's
deliberate cross-specialty choice with the actual mechanism named;
(iii) Disclosure 2.0 either acknowledges an equity tier or commits
to a minimum viable manifest; and (iv) the tonal swings flagged in
C5 are line-edited.

## Specific paragraph that needs rewriting before resubmission

Section 4, paragraph 1 (`manuscript/main.tex` lines 127--128, "To
establish that the workflow is not a methodological self-portrait ..."
through the citations to `linehs2024` / `lintom2026`). The current
text introduces the operator as "a board-certified medical
oncologist whose published work is in hematologic malignancies".
Per the CV at `lin.hsiehting.com/cv/`, the operator is a haematology
and medical oncology *fellow* whose four-paper record covers
HSCT-in-TCL, G-CSF timing, high-flow nasal oxygen, and one LLM-on-
poker preprint. The paragraph should be rewritten to (a) state the
operator's actual position accurately, (b) own the cross-specialty
case-study choice as deliberate, with the practical reasons named
(TCGA-LIHC is publicly redistributable under MIT; cross-domain
mismatch is the sharper test of workflow generalisation), and (c)
drop the "the workflow is not a methodological self-portrait"
defensive framing in favour of a positive claim ("the case study
deliberately runs outside the operator's clinical sub-specialty so
that domain expertise cannot quietly carry the workflow"). This
paragraph is load-bearing; the rest of Section 4 reads better once
this paragraph is honest.
