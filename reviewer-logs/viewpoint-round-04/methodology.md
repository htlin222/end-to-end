# Viewpoint Round 4 — Methodology / Reproducibility Reviewer (Confirmation)

- **Round**: 4 (confirmation)
- **Reviewer**: methodology
- **Date**: 2026-05-21
- **Manuscript HEAD inspected**: `98bd5eb` (chore: regenerate ledger +
  Figure 1 after R3 closure)
- **Persona spec**: `prompts/04-viewpoint-reviewer-methodology.md`
- **Round 3 verdict**: `accept` (with three `release_check.sh`
  operator-hygiene flags logged as non-blocking; my R3 note recorded
  them as check-script defects, not methodology defects).

## Confirmation mandate

The R4 brief is narrow: read the updated `main.tex`, `docs/design.md`,
`docs/disclosure2-schema.json`, `docs/ledger.md`,
`scripts/release_check.sh`; run the release check; verify ledger
determinism; confirm the three R3 false-positive flags are corrected.

## Files re-read at HEAD `98bd5eb`

- `manuscript/main.tex` — Section 5 distributional-reproducibility
  falsifier (line 150 region), layer-separation paragraph (line 152
  region), Limitations seven-blind-spot enumeration (line 178 region):
  all unchanged in substance from the R3 accept state.
- `docs/design.md` — Procedural-vs-technical enforcement table (lines
  99–117) and "Intentionally-overwritable artefacts" subsection (lines
  119–137): both unchanged from R3.
- `docs/disclosure2-schema.json` — `toolEnvelope` description with the
  MUST/SHOULD coupling to `models[].name` (lines 74–81): unchanged
  from R3.
- `docs/ledger.md` — regenerated at `98bd5eb`, captures 33 commits at
  the parent of HEAD (one-commit lag is structurally unavoidable; the
  new ledger-determinism check in `release_check.sh` no longer fails
  on it — see below).
- `scripts/release_check.sh` — three predicates rewritten since R3.

## Three R3 false positives — corrected at HEAD

I flagged three operator-hygiene defects in R3. All three are fixed
at `98bd5eb`.

### 1. `git fsck` grep predicate (R3 flag → fixed)

R3 reported the `no force-pushed or rebased history` check used
`grep -vq "broken link\|missing"`, which exits 1 on empty input
(`grep -q` returns the wrong polarity with `-v` against an empty
stream).

At HEAD line 65 the predicate is now:

```sh
! git fsck --no-progress --no-dangling 2>&1 | grep -qE "broken link|missing"
```

This is the standard "absence of matching lines" idiom: `grep -qE`
exits 0 only when a match is found, and the leading `!` inverts to 0
on empty input. Verified by running the script: the check is now
`OK`. Fix is correct.

### 2. Body word count enumerator (R3 flag → fixed)

R3 reported the shell-awk body-word-count enumerator did not deduct
the title-page metadata block (Running title, Article type, word
count line, References count, Display items, Corresponding-author
address, Conflicts, Funding, Role of funder), so it reported 2,727
against a true body of 2,281.

At HEAD line 105 the predicate is now a Python invocation against
`texcount -inc -sum manuscript/main.tex` that parses the
`-sum`-mode totals directly, treating the manuscript's own
`%TC:ignore`/`%TC:endignore` block markers as the canonical
non-body declaration. This is the right approach: it lets the
manuscript author mark non-body regions inline rather than the
release script maintaining a parallel deduction list.

Verified at HEAD: the body word count check reports `OK`. The
manuscript was retitled-and-recounted to 2,428 words at commit
`dd7b3e4` (R3 close-out word-count update); 2,428 < 2,500 so the
Lancet DH ceiling is respected and the title page (line 60), cover
letter (line 58), and this check are now in agreement. Fix is
correct.

### 3. Ledger-regen determinism check (R3 flag → fixed)

R3 reported the `docs/ledger.md regenerates deterministically (no
diff)` check compared the *committed* ledger to a fresh regen at
HEAD, which is structurally guaranteed to be off by one row (the
regen-and-commit step adds the 30th commit whose row cannot exist
in the file that commit just wrote). My recommendation in R3 was to
either accept the off-by-one as a known artefact or to switch the
check to compare two consecutive regenerations against each other.

At HEAD lines 175–181 the predicate is now:

```sh
uv run python scripts/regenerate_ledger.py >/dev/null 2>&1;
cp docs/ledger.md /tmp/ledger.run1;
uv run python scripts/regenerate_ledger.py >/dev/null 2>&1;
cp docs/ledger.md /tmp/ledger.run2;
diff -q /tmp/ledger.run1 /tmp/ledger.run2
```

This tests the property that actually matters — that the regenerator
is deterministic — and ignores the structurally-unavoidable
commit-self-reference off-by-one. This is exactly the fix I
recommended (path (a)). Verified at HEAD: the check reports `OK`.
Fix is correct.

**Caveat the operator should be aware of.** This check predicate no
longer enforces that the committed ledger is current at the release
tag. The pre-tag operator step (re-run `regenerate_ledger.py`,
commit, then push the tag on the second commit) is the gate that
ensures the committed ledger is current at the *released* SHA. This
trade-off is correct for a release-check script that runs against an
arbitrary HEAD, but the release procedure should explicitly note
"re-run regenerator and commit before tagging" so the lag-by-one is
resolved at tag time. I am not raising this as a new comment; it is
an operator note on `RELEASE_NOTES.md` (which exists at HEAD per
`04c72e8`).

## `release_check.sh` run at HEAD `98bd5eb`

```text
::: 28 passed, 1 failed, 1 warned
::: release blocked
```

Breakdown:

| Status | Check | Methodology assessment |
|--------|-------|------------------------|
| FAIL | `working tree is clean` | Working tree has uncommitted case-study Layer-1 re-execution artefacts (operator-step, will be addressed at `case-study-v1.0.0` tag). Not a methodology defect. |
| OK | `on main branch` | clean |
| OK | `no force-pushed or rebased history` | **R3 false-positive corrected** — predicate now exits 0 correctly on clean repo. |
| OK | `item 1 prompts: closed-for-edits present` | clean |
| OK | `item 2 model identifier` | clean |
| OK | `item 3 commit history integrity` | clean |
| OK | `item 4 reviewer transcripts` | clean |
| WARN | `item 5 audit log: Layer-2 audit complete` | `reviewer-logs/audit/findings.md` is the submission-day Layer-2 step; manuscript Section 3 item 5 downgrade language covers this. |
| OK | `item 6 disclosure2-schema present` | clean |
| OK | `manuscript main.tex compiles` | clean |
| OK | `manuscript main.pdf produced` | clean |
| OK | `no placeholder tokens in main.tex` | clean |
| OK | `no placeholder tokens in cover-letter.md` | clean |
| OK | `no placeholder DOIs in references.bib` | clean |
| OK | `body word count <= 2500` | **R3 false-positive corrected** — `texcount`-driven enumerator now reports correctly under the 2,500 ceiling. |
| OK | `reference count <= 30` | clean |
| OK | `display items <= 2` | clean |
| OK | `Acknowledgements names AI tool and version` | clean |
| OK | `Acknowledgements states no AI authorship` | clean |
| OK | `Search-strategy panel has AI-use disclosure` | clean |
| OK | `Acknowledgements states no AI figures` | clean |
| OK | `all cite keys in main.tex have a bib entry` | clean |
| OK | `no <<PREREG_COMMIT_SHA>> placeholder` | clean |
| OK | Figure 1 / Figure 2 / Figure 1 sidecar present (3 checks) | clean |
| OK | `docs/ledger.md present` | clean |
| OK | `docs/ledger.md regenerator is deterministic (two consecutive runs identical)` | **R3 false-positive corrected** — predicate now compares run1 vs run2 directly, eliminating the off-by-one. |
| OK | `gh is authenticated` | clean |
| OK | `origin remote is reachable` | clean |

**Summary: 28 passed, 1 failed (working tree clean — operator-step),
1 warned (Layer-2 audit log — submission-day operator-step).** The
single FAIL is the working-tree-clean check; that gate is the
release-tag's right place to refuse, and the operator will clear it
at submission. The one WARN is the submission-day Layer-2 audit. No
methodology-axis defect remains in the release check or its
predicates.

## Ledger determinism — verified

I ran `uv run python scripts/regenerate_ledger.py` three times in
succession on the working tree at HEAD `98bd5eb`:

```text
$ shasum -a 256 /tmp/ledger.r4.first /tmp/ledger.r4.second /tmp/ledger.r4.third
f8b5f7759af75ceb7ddaf4372e2795f2dde2ddcf1549dbde18f89ca75cdcab6e  /tmp/ledger.r4.first
f8b5f7759af75ceb7ddaf4372e2795f2dde2ddcf1549dbde18f89ca75cdcab6e  /tmp/ledger.r4.second
f8b5f7759af75ceb7ddaf4372e2795f2dde2ddcf1549dbde18f89ca75cdcab6e  /tmp/ledger.r4.third
```

All three runs produced byte-identical output. The regenerator is
deterministic, confirming the property the new
`release_check.sh` check encodes. (I then restored the committed
`docs/ledger.md` via `git checkout HEAD -- docs/ledger.md` so the
working tree state is unchanged.)

## Acceptance criteria — re-checked at HEAD

| Criterion (from persona prompt) | State at R4 HEAD |
|---------------------------------|------------------|
| Distributional-reproducibility claim falsifiable | met — `main.tex` §5 line 150 region unchanged from R3 (n=3 runs, sub-claim + method concordance, headline within bootstrap CI; graceful-downgrade path explicit). |
| Layer separation enforced by named procedure or technical means | met — `main.tex` §5 line 152 (testimonial-vs-cryptographic, session-launch attestation) + `docs/design.md` lines 99–117 (procedural-vs-technical table) unchanged from R3. |
| Manifest residual blind spots in manuscript text | met — `main.tex` line 178 enumeration of seven blind spots unchanged from R3, including the reviewer-AI collusion and uncommitted-run selective preservation entries that closed R2's M-3. |

All three criteria continue to be met. No regression since R3.

## New issues in Round 4

None.

## Verdict

`accept`.

The methodology axis is closed. The three `release_check.sh` defects
I flagged as non-blocking operator-hygiene items in R3 are all
corrected at HEAD `98bd5eb` and verified by running the script. The
ledger regenerator is deterministic across three consecutive runs.
The manuscript text, design doc, and Disclosure 2.0 schema are
unchanged in the substantive content the R3 verdict relied on. The
only remaining FAIL in the release check (`working tree is clean`)
is the appropriate operator-step gate that the release tag will
clear at submission. The manuscript is ready to submit on the
methodology axis.
