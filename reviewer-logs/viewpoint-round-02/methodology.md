# Viewpoint round 02 — Methodology / Reproducibility Reviewer

- **Round**: 2
- **Reviewer**: methodology
- **Date**: 2026-05-21
- **Manuscript SHA referenced**: working tree at HEAD `5fde223`
  (`reviewer-logs: add Round 1 response-to-reviewers cross-reference table`);
  v0.4 manuscript content was committed in `da4ddce`.
- **Verdict**: `minor-revision`

## Overall impression

The revision is responsive and the central architectural gaps from
Round 1 have closed. The three forward-references that blocked Round 1
(`docs/disclosure2-schema.json`, `docs/ledger.md`, `99_reexec_check.py`)
have been resolved in the manner I asked for: the first two are
committed and the third is *honestly downgraded in the manuscript text
itself*, which is the more credible move than fabricating a script.
The distributional-reproducibility claim now carries a concrete
falsifier with a numeric tolerance (selected sub-claim and statistical
method concordant across three runs; headline effect size within the
original's bootstrap 95\,\% CI). The audit log is split into 5a /
5b / 5c with the in-text citation-claim alignment requirement that
Round 1 comment 4 asked for. The three-layer seal is now explicitly
named as testimonial rather than cryptographic in Section 5, with the
session-launch attestation file path called out. The Limitations
section now carries the named blind spots (procedural enforcement,
reviewer-loop non-determinism, operator's prior clinical knowledge).
Zhao et al.\ 2026 is cited in Section 2 with the specific 146\,932
number; the Sakana hallucination citation is paired with it.

`docs/ledger.md` regenerates deterministically. I ran
`uv run python scripts/regenerate_ledger.py` twice and the two outputs
are byte-identical; the file the regenerator now writes captures all
25 commits in the current `git log`. The committed
`docs/ledger.md` snapshot was taken at commit `0810331` (23 commits)
and is therefore two commits behind HEAD by design — the next
release-tag regeneration will catch it up. This is the right
behaviour, not a defect, but is documented as comment M-2 below.

The schema at `docs/disclosure2-schema.json` is rich enough for the
manuscript's claim: it requires `schemaVersion`, `manuscriptTitle`,
`submissionVenue`, `operator`, `models`, `toolEnvelope`, `repository`,
`release` (the eight-item base); and provides optional
`prompts`, `reviewerSubagents`, `audit` (with `reExecution`,
`citationVeracity`, `statisticalReproducibility`, `claimDataAlignment`,
`consolidatedFindings` — these align with the 5a/5b/5c split),
`preregistration`, and `honestyContract`. The minimum-viable subset
(prompts, model, commit hash, tagged release) is expressible by
treating `reviewerSubagents` and `audit` as absent. **One schema gap
worth naming**: the schema does not enforce that the minimum-viable
manifest is a *subset* (i.e., there is no `oneOf` discriminator
between "full" and "minimum-viable" variants). Section 6 of the
manuscript names both; the schema lets a producer omit `audit` and
still be valid, which is correct in spirit but should be documented
in the schema's `description`.

## Round 1 comments — closure status

| # | R1 severity | R1 summary | Round 2 status | Where in v0.4 |
|---|-------------|------------|-----------------|--------------|
| 1 | blocker | Distributional-reproducibility falsifier unspecified; `99_reexec_check.py` missing | **closed** | `main.tex` §5 names selected sub-claim + statistical method + headline-statistic-within-bootstrap-CI as the falsifier, across three runs; downgrade path for missing-script case is explicit |
| 2 | high | Three-layer separation enforced by honour only | **closed** | `main.tex` §5 and Limitations both name the seal as testimonial; session-launch attestation path declared as the minimum operational evidence |
| 3 | high | Honesty-contract rules behavioural | **closed** | Limitations: "only the no-history-rewriting rule is mechanically enforceable, via branch protection on `main`"; the other three are named as behavioural |
| 4 | high | Citation hallucination defence partial | **closed** | §3 item 5b: "citation veracity for every entry (DOI, author list, journal, year) and every in-text claim-to-source alignment" |
| 5 | blocker | `docs/ledger.md` does not exist | **closed** | committed at `docs/ledger.md`; generator `scripts/regenerate_ledger.py` regenerates deterministically (verified, see below) |
| 6 | medium | Model deprecation named and dropped | **closed** | §5 final paragraph + Limitations: deprecation policy (re-execute on named successor with labelled-as-divergent attestation, or freeze artefact in audit log) |
| 7 | medium | Zhao et al.\ corpus-scale audit not cited | **closed** | `references.bib` `zhaoHallucinations2026`; cited at §1 and §2 with the 146\,932 figure |
| 8 | medium | Reviewer-loop non-determinism not acknowledged | **closed** | Limitations: "the reviewer-subagent loop is itself non-deterministic --- distributional reproducibility applies to the analytic pipeline, not to the reviewer comments" |
| 9 | medium | `docs/disclosure2-schema.json` does not exist | **closed** | committed; covers all six manifest items + optional audit/reviewer-subagent blocks (one minor doc gap; see M-1 below) |
| 10 | medium | Layer-2 seal is testimonial | **closed** | §5 makes the testimonial-vs-cryptographic distinction explicit |
| 11 | medium | Failure preservation rule partially violated | **open (deferred)** | Acknowledged in response-to-reviewers as deferred to next `docs/design.md` update; the manuscript Limitations does not surface this specific carve-out (intentionally-overwritable artefacts) |

Net: ten of eleven Round 1 comments closed; one (R1-#11)
explicitly deferred to a `docs/design.md` update and not surfaced in
the manuscript text. I do not treat the deferral as a blocker
because R1-#11 was medium severity and the rest of the honesty-
contract enforcement story is now named in Limitations.

## Verification of new artefacts

### `docs/disclosure2-schema.json`

Reviewed end-to-end. The schema captures the six manifest items the
manuscript names plus the audit-output sub-artefacts. Coverage check
against Section 3:

- item 1 (prompts) — present (`prompts` array, regex on path); good.
- item 2 (model identifier and snapshot) — present (`models[].vendor`,
  `name`, `version`, `snapshotDate`, `samplingParameters`); the
  `toolEnvelope` lives in its own property (separated from `models`),
  which matches the manuscript's prose but means the schema does not
  enforce that every model in `models` has an entry in
  `toolEnvelope`. This is a minor coverage gap (M-1).
- item 3 (commit history) — present (`repository.commitSha`,
  `repository.url`); branch protection is *not* expressed in the
  schema (it cannot be — branch protection is a server-side fact),
  which is fine.
- item 4 (reviewer-subagent transcripts) — present
  (`reviewerSubagents` with per-round `personas` / `verdicts` /
  `logDirectory`). Verdict enum is consistent with the four-state
  decisions.json convention.
- item 5 (audit log, three sub-artefacts) — present (`audit` with
  `reExecution`, `citationVeracity`, `statisticalReproducibility`,
  `claimDataAlignment`, `consolidatedFindings`). The schema therefore
  encodes 5a / 5b / 5c plus a claim-data alignment field that is
  conceptually 5b's prose mirror.
- item 6 (tagged release) — present (`release.tag`, `release.url`,
  optional `zenodoDoi`).

### `docs/ledger.md` regeneration

Ran twice. Both runs produced byte-identical output. The runner
emits "wrote /Users/htlin/end-to-end/docs/ledger.md (25 commits,
0 tags)"; the committed file records 23 commits because it was
generated at commit `0810331` and the regenerator is HEAD-relative.
A reproducer cloning at any tagged commit and running
`uv run python scripts/regenerate_ledger.py` will get the same
ledger byte-for-byte; the script reads `git log --reverse` and
classifies by path-prefix only, with no time-of-day or
non-deterministic input.

### Section 5 falsifier

The distributional-reproducibility falsifier is now operational
text in the manuscript:

> re-running Layer 1 against the same model identifier, snapshot
> date and committed tool envelope must yield the same selected
> sub-claim and statistical method across three independent runs,
> with the headline effect size within the original's bootstrap
> 95\,\% interval.

This answers all three sub-questions from R1 comment 1: n = 3 runs,
concordance on sub-claim and statistical method, headline effect
within bootstrap CI. The downgrade language ("if Layer 1 ships the
release without that script, the claim is downgraded to
'single-run with operator-described variability bounds' in that
release's audit log") is the right honesty move; it does not
pretend the script exists and it gives the operator a graceful
fallback. R1 comment 1 is closed.

### Audit log split 5a / 5b / 5c

Section 3 item 5 now reads:

> A sealed subagent produces three compliance-relevant sub-artefacts:
> (5a) re-execution of the analysis from a clean clone, (5b)
> citation veracity for every entry (DOI, author list, journal,
> year) and every in-text claim-to-source alignment, and (5c)
> headline-statistic rederivation from the committed code.
> Partial discharge of (5a) alone does not satisfy item 5.

The trailing sentence — "Partial discharge of (5a) alone does not
satisfy item 5" — is a stronger commitment than I asked for in
Round 1. It closes the audit-as-checkbox failure mode named in
R1-#4. Closed.

### Limitations — named blind spots

Procedural-vs-technical enforcement, reviewer-loop non-determinism,
and the operator's-prior-knowledge leakage all appear in the
Limitations paragraph. The seven failure modes I enumerated in
Round 1 ("Failure modes the manifest does not catch") are not
copied verbatim, but four of the seven (procedural enforcement,
audit-subagent hallucination, model deprecation, reviewer-loop
non-determinism) are now in the manuscript text. The remaining
three (reviewer-AI collusion, prompt-text Unicode drift, selective
failure preservation across uncommitted runs) are not surfaced.
This is a minor revision item (M-3 below); the manuscript would
benefit from one additional sentence naming them, but their
absence is not blocking.

## Comments still open

### M-1. Schema does not cross-reference `toolEnvelope` to `models`. *Severity: low.*

`docs/disclosure2-schema.json` defines `toolEnvelope` as an open
`additionalProperties` map with array values. The manuscript
(Section 3 item 2) couples the tool envelope to "the model identifier
[…] was authorised to invoke", implying a per-model envelope. A
producer of a Disclosure 2.0 manifest could populate `models` with
two entries and `toolEnvelope` with one key that matches neither
model's `name`, and the schema would accept it. A minor schema
tightening (e.g., add a `description` requiring `toolEnvelope` keys
to match a `models[].name` value, or use a `$ref` that enumerates
permitted keys at validation time) would close this. Not a Round 2
blocker.

### M-2. `docs/ledger.md` lags HEAD by two commits. *Severity: low.*

The committed `docs/ledger.md` was regenerated at commit `0810331`
and has not been updated for the two commits added since
(`5fde223`, the response-to-reviewers cross-reference). The
release-tag policy stated in the file's preamble ("Re-run after every
commit or at release time") is correct; the operator should add
the ledger regeneration to the release-tag step in `manuscript/
Makefile` or document it in `JOURNAL.md`'s submission checklist so
the tagged release ships with a current ledger. This is operator-
hygiene, not a methodology defect.

### M-3. Manuscript Limitations does not name two-of-seven Round 1 failure modes. *Severity: low.*

R1 enumerated seven residual failure modes; v0.4 surfaces four of
them in Limitations. Reviewer-AI collusion (same-model author and
reviewer subagents biased by shared persona-prompt edits) and
selective failure preservation across runs that were never
committed are absent. The cross-model-audit recommendation
(Section 6 recommendation 4) implicitly addresses the first, but
the Limitations text would be strengthened by one sentence naming
both as residual.

### R1-#11. Failure-preservation carve-out for intentionally-overwritable artefacts. *Severity: medium, deferred.*

`case-study/data/results/cohort-selection.json`'s "will be
overwritten on the next pipeline run" comment remains the canonical
example of an intentionally non-preserving artefact. The response-
to-reviewers document marks this as deferred to a future
`docs/design.md` update. I accept the deferral but the operator
should land the carve-out before `viewpoint-v1.0.0` is tagged so
that the honesty-contract enumeration in `docs/design.md` is
self-consistent at submission time.

## New issues identified in Round 2

None that block. The only new substantive observation is that the
manuscript now relies on `viewpoint-round-01` artefacts being
present in the repository (Section 5 cites them by directory and
the Acknowledgements names `reviewer-logs/viewpoint-round-01/`).
The directory does exist (it carries the five Round 1 artefacts I
am verifying against in this review). This is a defensible
self-reference and not a new forward-reference of the Round 1
type.

## Verdict

`minor-revision`. The methodology axis is materially closed: the
distributional-reproducibility falsifier is operational, the
three-layer seal is honestly named as testimonial, the audit log
is split into 5a / 5b / 5c with in-text claim-citation alignment
required, the schema and the ledger generator are committed, and
the ledger regenerates deterministically (verified). The four
remaining items (M-1, M-2, M-3, R1-#11 deferred) are all low- or
medium-severity hygiene rather than architectural gaps. With
these landed before `viewpoint-v1.0.0`, the methodology axis
clears `accept`.

## Recommended path to `accept` in round 3

1. Tighten the schema so `toolEnvelope` keys are required to be a
   subset of `models[].name` (M-1).
2. Add ledger regeneration to the release-tag Makefile target so
   the committed `docs/ledger.md` is current at submission (M-2).
3. Add one sentence to Limitations naming reviewer-AI collusion
   and uncommitted-run selective preservation as residual blind
   spots (M-3).
4. Land the `docs/design.md` carve-out for intentionally
   overwritable artefacts (R1-#11).

None of these require architectural change; all are documentation
and one Makefile target away.
