# Viewpoint Round 3 — Clinician-Investigator Reviewer

- **Round**: 3
- **Reviewer**: clinician (clinician-investigator persona)
- **Date**: 2026-05-21
- **Files inspected**:
  - `manuscript/main.tex` (current head)
  - `manuscript/cover-letter.md` (current head)
  - `reviewer-logs/viewpoint-round-02/response-to-reviewers.md`
  - `reviewer-logs/viewpoint-round-02/clinician.md` (own R2 transcript)
- **Persona spec**: `prompts/04-viewpoint-reviewer-clinician.md`
- **Round 1 verdict**: major-revision (8 comments).
- **Round 2 verdict**: minor-revision (7/8 R1 closed; 1 closed-with-
  condition on Layer-3 release-tag substitution; 3 new low-severity N1–
  N3).

## Overall impression

This is the round where the manuscript stops being a candidate-for-
fix and becomes a candidate-for-publication. The structural and
rhetorical work that mattered to a clinician-investigator reader is
done. The three Round 2 minors I raised (N1 hyphenation, N2 named
target journal, N3 operator-in-the-loop gate description) are all
addressed in `manuscript/main.tex` as documented below.

The single remaining non-negotiable — the C3 close-out gate that
substitutes the actual Layer-3 numbers for $\hat{\delta}$, $L$, $U$
at the release tag — is by design a submission-day operator step that
sits outside the manuscript-reviewer pipeline, and the response-to-
reviewers item 5 ("`case-study/analysis/99_reexec_check.py`" being
Layer 1's responsibility at `case-study-v1.0.0`) records it openly in
the "operator-step items still outstanding at submission day" list.
That is the right place for it: a Round 3 reviewer cannot un-write
this condition into the manuscript, and asking the operator to fake
the numbers before Layer~3 executes would defeat the entire negative-
result-commitment design.

I am recommending **accept**, conditional on the same submission gate
the editor will enforce anyway (the placeholders must be substituted
at the moment the `viewpoint-v1.0.0` tag is pushed, after Layer~3 has
actually executed). The Round 2 conditional has been honoured in
spirit and in design; the operator condition is correctly logged.

## Verification of Round 2 comments

### N1 [closed] Layer hyphenation harmonisation

The R2 finding flagged inconsistency between "Layer~1/2/3" (non-
breaking tilde) and "Layer 1/2/3" (no tilde) across main.tex, cover
letter and disclosure docs.

Current state in `manuscript/main.tex`:

- Lines 87, 133 (Section 4 paragraph 2), 150, 152, 162: all use
  `Layer~1`, `Layer~2`, `Layer~3` with the non-breaking tilde. This
  is the canonical form for the body prose and Section 4 now matches.
- Line 144 (Section 4 conditional sentence): uses "Layer-3 sentence",
  "Layer-1 risk score", "Layer-2 hallucinations" with the hyphen.
  This is the *adjectival* (compound-modifier) form: "Layer-1 risk
  score" reads as a noun phrase where "Layer-1" modifies "risk
  score", and the hyphen is the correct English usage. The tilde
  form would read awkwardly there.
- Line 140 (Figure~1 caption): "Layer 1 Pipeline", "Layer 2 Audit",
  "Layer 3 External Validation" — figure caption uses display
  capitalisation without the tilde. This is also correct for caption
  typography; LaTeX figure captions render to fixed type and the
  non-breaking-space is irrelevant.

The pattern is therefore: tilde in body prose, hyphen in compound
modifiers, plain space in captions. This is the right house style and
matches what a Lancet copy-editor would apply on a final pass.

The response-to-reviewers entry for clinician N1 says "Standardised
non-breaking hyphen across Section 4" — I read the actual Section 4
text and the standardisation is consistent with the convention
above. N1 is closed.

Residual: the cover letter at line 40 still contains "\{prompt, model
identifier, tool envelope, commit history, reviewer-subagent
transcripts, audit log, tagged release\}" — the set-notation that I
asked to remove from Section 1 of the main manuscript in Round 1
C5. The main manuscript has been corrected; the cover letter has
not. This is below the threshold of a new R3 comment — cover letters
are not part of the published article and the copy-editor will not
touch them — but the operator should be aware that the editorial
office may read the cover letter with the same lens. Not a blocker
and not raised as a new comment.

### N2 [closed] Section 4 names the target journal Layer 1 selected

R2 flagged that Section 4 paragraph 2 said "a clinical-genomics
journal of its own choice" without naming the journal.

Current state, `manuscript/main.tex` line 133: "a draft manuscript
targeting a clinical-genomics journal of its own selection (recorded
in `case-study/manuscript/JOURNAL.md`)". The journal name is not
inlined in the Viewpoint body, but a pointer to the operator-readable
record (`case-study/manuscript/JOURNAL.md`) is. This is acceptable
for two reasons. First, the Viewpoint is making a methodological
argument, not a clinical-genomics journal-fit argument; embedding the
specific journal name would over-promise editorial coupling between
this Viewpoint and the case-study submission and read as
self-promotional. Second, a curious reader can follow the GitHub
link in Data Sharing and `JOURNAL.md` is the right level of
specificity. The case-study manuscript itself names the target
journal in its own submission cover letter, which is the right
locus.

N2 is closed. The response-to-reviewers entry matches what I see in
the text.

### N3 [closed] Operator-in-the-loop role explicit in Section 4

R2 flagged that the manuscript implied Layer~3 was the only human
step while `docs/ai-usage-disclosure.md` correctly listed the
operator as also gating commits and tag pushes.

Current state, `manuscript/main.tex` line 133, second sentence of
Section 4 paragraph 2: "The operator's in-the-loop role across the
pipeline is restricted to (i) supplying the domain prompt and the
orchestration prompts (committed verbatim, closed for edits), (ii)
approving each commit and tag before push, and (iii) executing the
Layer~3 external validation; the operator did not edit Layer 1
outputs, did not modify reviewer-subagent comments, and did not
select Layer 3 cohorts based on Layer 1's result."

This is the exact reconciliation I asked for and goes beyond what I
asked for: the negative list (what the operator did *not* do) closes
three specific avenues a hostile reader would interrogate (output-
editing, reviewer-comment laundering, post-hoc cohort selection).
Together with the positive list (domain prompts, orchestration
prompts, commit+tag approval, Layer~3 execution), this paragraph
now reads as the right balance between honest description of human-
in-the-loop intervention and protection of the autonomy claim.

N3 is closed and is materially stronger than the R2 request asked
for.

## Status of the Round 2 closed-with-condition item

### C3 [submission-day gate, on track] Negative-result commitment

The Round 2 close-out gate was: at release tag, the conditional
Layer-3 sentence on line 144 must collapse to whichever branch the
real Layer~3 result picked, with $\hat{\delta}$, $L$, $U$ substituted
with the actual numbers.

`manuscript/main.tex` line 144 still carries the conditional with
placeholders. This is correct: Layer~3 cannot have been executed yet
because the manuscript has not been submitted, and pre-substituting
fake numbers would itself violate the design. The response-to-
reviewers documents this openly in the "Operator-step items still
outstanding at submission day" list (item 5,
`case-study/analysis/99_reexec_check.py` at `case-study-v1.0.0`).
The structural fix the reviewer pipeline can deliver is done;
the remainder is the submission-day gate.

This is treated as a *condition on submission*, not as an unresolved
R3 manuscript defect. I would re-open this comment only if the
operator pushed the `viewpoint-v1.0.0` tag with the placeholders
still in the PDF.

## New issues in Round 3

None.

## Verdict

`accept`.

Conditions on submission (not on the manuscript):

1. At `viewpoint-v1.0.0` tag push, the Layer-3 conditional sentence
   in Section 4 (line 144) must be collapsed to the actual branch
   with the real $\Delta C$ value and bootstrap 95\,\% CI
   substituted. This is the C3 close-out gate documented in the
   response-to-reviewers operator-step list.
2. Optional final copy-edit pass on the cover-letter (`\{...\}` set
   notation at line 40) — not raised as a new comment, but a
   courtesy heads-up for the operator's pre-submission pass; the
   manuscript itself has already been corrected.

The four acceptance criteria the user spec asked me to test against:

| Criterion | State |
|-----------|-------|
| Workflow real | Yes — Section 4 paragraph 2 reads as honest description, restart preserved, operator-in-the-loop role explicit on both positive and negative axes |
| Operator-expertise calibrated | Yes — CV-confirmed haematology/medical oncology fellow framing throughout main.tex and cover letter; cross-specialty HCC case study owned as deliberate not opportunistic |
| Negative-result commitment genuine | Yes — both branches pre-written on line 144; Layer~3 executes once without re-tuning; release-tag gate is correctly an operator-step rather than a reviewer-step |
| Tone calibrated | Yes — Section 1 prose replaces set notation, Section 5 uses policy vocabulary, Section 8 closer reads as argument not posture |

All four are satisfied. Recommend acceptance.
