# Viewpoint Round 2 — Clinician-Investigator Reviewer

- **Round**: 2
- **Reviewer**: clinician (clinician-investigator persona)
- **Date**: 2026-05-21
- **Manuscript commit**: 5fde2234b24b5c4e483bf5ba1ff72310f03e8694 (head;
  v0.4 + response-to-reviewers).
- **Files inspected**: `manuscript/main.tex`, `manuscript/cover-letter.md`,
  `docs/ai-usage-disclosure.md`, `docs/prereg.md`,
  `reviewer-logs/viewpoint-round-01/clinician.md`,
  `reviewer-logs/viewpoint-round-01/response-to-reviewers.md`,
  `reviewer-logs/viewpoint-round-01/decisions.json`.
- **External check**: `https://lin.hsiehting.com/cv/` re-fetched via
  WebFetch, 2026-05-21. CV confirms: Hematology & Medical Oncology Fellow
  at Koo Foundation Sun Yat-Sen Cancer Center since August 2023; board-
  certified in Internal Medicine (TSIM) and Medical Oncology (Taiwan
  Oncology Society); four-paper record (HFNO in cancer patients,
  G-CSF timing in CIN, HSCT in T-cell lymphoma, theory-of-mind in LLM
  poker agents).

## Overall impression

The revision is meaningfully closer to what a clinician-investigator
reading Lancet DH would accept. The two structurally important moves
in v0.4 are (i) the rewrite of Section 4 paragraph 1 — the cross-
specialty case-study choice is now owned as deliberate, with the
practical mechanism (MIT-redistributability of TCGA-LIHC, cross-domain
mismatch as the sharper test) named — and (ii) the pre-written
conditional Layer-3 sentence that commits both branches of the
headline in advance of execution. These are the two moves a hostile
reader would have demanded; both have been made.

The tone calibration in Sections 1, 5 and 8 has been performed cleanly.
The set-notation in Section 1 has been replaced with prose; "operator-
sovereign autonomy" is gone from Section 5; the Section 8 closer is
now "the repository remains in the public record regardless of the
editorial decision; the substantive question for the field is whether
the disclosure unit it embodies should generalise", which reads as
argument rather than posture.

The Disclosure 2.0 burden objection has been addressed via the
"minimum viable manifest" (items 1, 2, 3 and 6), and an equity counter-
argument has been added to Section 5. The minimum viable manifest is
a real concession, not cosmetic; it would in fact be usable by a
clinician-investigator with only GitHub fluency.

Three caveats keep me from a clean accept. (a) The Section 4 first
paragraph now correctly identifies the operator as a fellow but
slightly loses the rhetorical sharpening I argued for in Round 1: a
fellow successfully operating a cross-domain workflow is a *more*
surprising existence proof than an attending, and the revision does
not exploit that. This is a minor opportunity cost, not a blocker.
(b) The conditional Layer-3 prose is well-constructed, but the
manuscript explicitly states "Layer~3 executes once, without re-
tuning" — meaning the version of the manuscript currently in the
repository still has not been written against a real result. This
honours the spirit of my Round 1 C3 (the commitment is no longer
rhetorical; both branches are pre-committed before execution) but it
remains operator-dependent: the manuscript must not be submitted
until the actual run has occurred and the conditional has collapsed
to one branch. (c) New issue surfaced below (N1).

I am recommending **minor revision**. None of the remaining items
require structural rework; all are addressable within the next pass
prior to submission.

## Verification of Round 1 comments

### C1 [closed] HCC framing reads opportunistic, not deliberate

Resolved. `manuscript/main.tex` line 131 rewrites the Section 4
opening as: "The case study runs outside the operator's sub-specialty
so that domain expertise cannot quietly carry the workflow. The
operator is a haematology and medical oncology fellow at the Koo
Foundation Sun Yat-Sen Cancer Center whose published clinical work is
in hematologic malignancies and supportive care...". The "board-
certified medical oncologist whose published work is in hematologic
malignancies" phrasing has been dropped. The cross-specialty choice
is owned with both reasons (MIT-redistributability + cross-domain
mismatch as the sharper test). Section 1 paragraph 2 likewise
distinguishes domain vs orchestration prompts. The CV check at
`https://lin.hsiehting.com/cv/` confirms the "haematology and medical
oncology fellow" wording is accurate; the operator is indeed board-
certified in Medical Oncology by the Taiwan Oncology Society, but is
in a fellow position rather than an attending one, which the
manuscript now reflects accurately.

Minor opportunity cost: the rhetorical lever I named in Round 1 (a
fellow is a *more* surprising existence proof than an attending) is
not picked up. The current text is honest and adequate; it could be
sharper. Not a blocker.

### C2 [closed] Disclosure 2.0 burden is unrealistic for the median target reader

Resolved. Section 3 now defines a "minimum viable manifest" (items
1, 2, 3 and 6: prompts, model identifier, commit history, tagged
release). Items 4 (reviewer transcripts) and 5 (audit log) become
required only "when audit-subagent compute is available". Section 5
adds the equity counter-argument explicitly: "The full manifest
assumes git fluency, a Zenodo account and a public tagged release.
The minimum viable manifest in Section~\ref{sec:unit} (prompts,
model identifier, commit hash, tagged release) preserves the most
consequential audit surfaces at near-zero infrastructure cost..."
This is the tiered minimum I asked for in Round 1, and the four-item
floor is plausibly executable by an evening-and-weekend clinician-
investigator with one GitHub repo to her name.

### C3 [closed-with-condition] Negative-result commitment is unverifiable

The "<<HEADLINE:layer3_primary>>" placeholder is gone. In its place
(lines 144) the manuscript carries: "At release tag the Layer-3
sentence will read either 'The Layer-1 risk score improved OS
discrimination over AJCC pathologic stage by $\Delta C$ = $\hat{\delta}$
(95\,\% CI $L$--$U$); primary hypothesis rejected' or, in the null
case, '$\Delta C = \hat{\delta}$ (95\,\% CI includes zero); primary
hypothesis not rejected, and Sections~7--8 rewritten conditional on
the null.' Both branches are pre-written; Layer~3 executes once,
without re-tuning."

This is the right structural answer. A clinician-reader who pulls up
the prereg at `docs/prereg.md` can verify that the primary outcome
(ΔC-index $\geq$ 0.03 with bootstrap 95% CI excluding zero), the
secondary outcomes (S1-S7, all reported regardless of primary), the
multiple-testing family (Bonferroni 0.05/7 = 0.0071), and the stop
rule (single-shot, no iteration) are locked. Section 7 already names
the power constraint (pooled $n \approx 357$, power $\approx 0.6$).

The conditional close is genuine, not rhetorical. The Round 1
objection is satisfied at the manuscript-design level.

Operator condition (not a manuscript fix): the version in the
repository at the moment of submission must have the placeholders
($\hat{\delta}$, $L$, $U$) substituted with the actual numbers from
the executed Layer 3, and the conditional sentence collapsed to
whichever branch the result picked. The current text is the right
template; submitting it as-is, with $\hat{\delta}$ still a hat, would
re-open this comment. I treat this as the responsibility of the
operator-step submission gate, not as an unresolved manuscript
defect.

### C4 [closed] Risk-stratification case study without a stated clinical decision

Resolved. Section 4 paragraph 5 now reads: "The case study is
illustrative of the \emph{workflow}, not of clinical utility. No
decision threshold is proposed and no clinical action in HCC is
supported." Section 7 (Limitations) reinforces: "null results in
Layer~3 do not refute the methodology and positive results do not
establish a clinical biomarker." This is the right pair of sentences.

### C5 [closed] Tone calibration

Resolved across the three flagged locations:

- Section 1: the set-notation `\{prompt, model identifier, tool
  envelope, ...\}` is gone. The Key Messages bullet and the Section 1
  body both render the list as prose ("the prompts, the model
  identifier, the tool envelope, the commit history, the reviewer-
  subagent transcripts and the audit log").
- Section 5: "operator-sovereign autonomy" → "fully autonomous
  workflows" / "copilot-supervised workflows". The phrasing now reads
  as policy vocabulary rather than design-doc vocabulary.
- Section 8 closer: rewritten to "The repository remains in the
  public record regardless of the editorial decision; the substantive
  question for the field is whether the disclosure unit it embodies
  should generalise." This is the soft-but-firm register Lancet DH
  publishes editorials in.

One small residual: Section 1 paragraph 1 cites the Sakana paper as
"produced a manuscript that passed first-round workshop peer review
under blind review". This is accurate per the published Sakana
record but it is the same breathless framing I flagged in Round 1.
It is a minor stylistic point; left as-is, it is acceptable.

### C6 [closed] Workflow description does not match real practice in two places

Resolved. Section 1 paragraph 2 now reads: "It takes one \emph{domain}
prompt plus a small set of \emph{orchestration} prompts (Layer~1,
Layer~2 audit, four reviewer personas, all committed verbatim in
\texttt{prompts/})..." and the same paragraph adds: "Realistic
practice includes restarts; the present case study documents one in
\texttt{case-study/docs/failure-mode-01-cohort-selection.md}." Section
4 paragraph 2 mirrors the same distinction: "The pipeline received
one \emph{domain} prompt ... and the orchestration prompts in
\texttt{prompts/}... One operator-initiated restart is committed
(\texttt{failure-mode-01-cohort-selection.md}); the manifest preserves
the failure." This is exactly the disambiguation I asked for, and the
explicit pointer to the failure-mode-01 file is the right move.

### C7 [closed] Cover-letter sentence on prior LLM work

Resolved. The cover letter at `manuscript/cover-letter.md` lines
65--72 now carries a new section, "Generative-AI background of the
author": "My prior LLM-adjacent work (theory-of-mind-like behaviour
in LLM poker agents, arXiv 2026, sole author) informs this Viewpoint's
framing of agentic-LLM disclosure. My day job is as a haematology and
medical oncology fellow; I am not an LLM researcher, and the present
manuscript reflects a clinician-investigator's practical encounter
with agentic tooling rather than a methods-paper contribution."

This is the factual, non-embellished framing I asked for and it
correctly underplays rather than overplays the prior LLM record. The
"salaried haematology and medical oncology fellow at the Koo
Foundation Sun Yat-Sen Cancer Center" wording later in the Conflicts
of Interest paragraph (line 104) is also calibrated and accurate per
the CV.

### C8 [closed] Name figure-generation script paths

Resolved. The Acknowledgements paragraph now explicitly names
"\texttt{manuscript/figures/build\_fig1.py} (artefact ledger,
regenerated from \texttt{git log})" and
"\texttt{manuscript/figures/build\_fig2.py} (policy gap matrix)".
A reader who wants to audit the no-AI-figures commitment can `git
blame` both files directly. Done.

## New issues identified in Round 2

### N1 [low] Acknowledgements paragraph hyphenation in "AI-vs-operator" / "Layer-2"

Stylistic micro-issue at copy-edit level: the Acknowledgements
paragraph and Section 4 paragraph 5 use "AI-vs-operator" and
"Layer-2 audited it" / "Layer~2 audit"; the manuscript is mostly
consistent on "Layer~1/2/3" with the tilde, but the cover letter and
some prose run "Layer 1" / "Layer 2" without the tilde. Editorial
copy-editors will harmonise this; flagging for the operator's pre-
submission pass.

Action: in a final pass, harmonise to "Layer~1", "Layer~2", "Layer~3"
throughout the manuscript, cover letter, and disclosure documents.
Non-blocking.

### N2 [low] Section 4 mentions "clinical-genomics journal of its own choice" without naming it

Section 4 paragraph 2 says the pipeline "drafts a manuscript targeting
a clinical-genomics journal of its own choice". A clinician-reader
will want to know which journal the autonomous pipeline selected (it
is a non-trivial output of the workflow and the basis for the journal-
fit subagent's behaviour). The case-study manuscript itself almost
certainly names it, and Lancet DH editors will want this in the
Viewpoint for narrative completeness.

Action: in the next pass, replace "a clinical-genomics journal of its
own choice" with the actual journal name plus a citation to the
case-study manuscript (or its preprint). Non-blocking.

### N3 [low] Operator's actual workflow includes one human gate the manuscript should name

The `docs/ai-usage-disclosure.md` itemises the operator's
interventions and lists, among them, "Approving the final cover
letter and clicking submit in Editorial Manager on the day of
submission" and "Reading and accepting (or rejecting and re-running)
each commit and each reviewer round before the corresponding tag is
pushed". This is an honest description of a meaningful operator-in-
the-loop gate that the manuscript itself does not advertise. Section
4 implies the only human step is Layer 3; the disclosure doc
correctly says the operator also gates commits and tag pushes. The
two should be reconciled.

Action: in Section 4 or Section 5, add one clause noting that the
operator gates the release tag (the disclosure doc records this and
the manuscript should not under-claim it). Non-blocking; it
strengthens the realism of the workflow description.

## Verdict

`minor-revision`.

Acceptance criteria for Round 3 (all addressable without structural
change):

1. At the moment of release tag, the Layer-3 conditional sentence is
   collapsed to the actual branch (positive or null), with the real
   $\Delta C$ value and CI substituted for $\hat{\delta}$, $L$, $U$.
   This is the C3 close-out gate and is the single non-negotiable item.
2. N1, N2, N3 addressed in a final copy-edit pass.

The workflow description now reads real, the operator-expertise
representation is calibrated to the CV, the negative-result
commitment is genuinely held (subject to the release-tag gate above),
and the tone is appropriate for the Lancet DH editorial register. I
will recommend accept in Round 3 upon (1).
