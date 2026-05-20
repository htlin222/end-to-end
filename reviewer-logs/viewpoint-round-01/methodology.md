# Viewpoint round 01 — Methodology / Reproducibility Reviewer

- **Round**: 1
- **Reviewer**: methodology
- **Date**: 2026-05-21
- **Manuscript SHA referenced**: working tree at commit `c694f07`
  (`prompts: add four Viewpoint-specific reviewer personas`),
  with two staged and seven untracked Layer-1 artefacts uncommitted.
- **Verdict**: `major-revision`

## Overall impression

The Viewpoint stakes its credibility on a six-item Disclosure 2.0
manifest plus a three-layer architecture, and it argues both are
falsifiable, auditable, and demonstrably operating in the repository it
ships with. After reading every artefact the manuscript points to, my
finding is that the architecture is **conceptually coherent and
partially implemented, but its operational guarantees are largely
aspirational**. Three independent gaps stop me at *major-revision*: the
distributional-reproducibility claim is asserted but its falsifier is
not yet written; the three-layer separation is enforced by honour
rather than by tool envelope or branch protection; and the artefact
ledger that Figure 1 advertises (`docs/ledger.md`, a re-runnable
generator) **does not yet exist in the repository**. The manuscript
also under-discloses its own residual blind spots: the
non-determinism of the LLM-as-reviewer subagent, the citation-
veracity check's silence on in-text claim-to-citation matching, and the
model-deprecation path are all argued for in `docs/design.md` and the
prompt artefacts, but the Viewpoint text itself does not surface them
as named failure modes. Disclosure that does not name its own gaps is
weaker than disclosure that names them; the manuscript currently does
the former.

The strongest defensive moves are real. The prompts are closed for
edits with supersession-by-amendment, the Layer-1 / Layer-2 / Layer-3
prompts are committed as separate, prereg-style artefacts, the
honesty-contract response to failure-mode-01 (extending the GEO pool)
is documented before the model touched the new cohort, and the
`prereg.md` Layer-3 thresholds are locked. These are not cosmetic; they
are the parts of the manifest a reviewer can verify today. They are not
yet enough to support the manuscript's stronger claim that the
manifest "actually delivers" the audit guarantees.

## Numbered comments

### 1. The distributional-reproducibility claim names a check but does not yet specify it. *Severity: blocker.*

Section 5 of `manuscript/main.tex` (lines 144–146) operationalises the
distributional claim as: "the repository includes a small re-execution
check (`case-study/analysis/99_reexec_check.py`) that runs Layer 1
three times and reports concordance on selected claim, statistical
method, and headline effect size."

`grep -r 99_reexec_check` returns no hits.
`/usr/bin/find case-study/analysis -name '99_reexec*'` returns nothing.
The file is also missing from `case-study/README.md`'s re-execution
recipe (which lists `01_prepare_data.py`, `02_layer1_risk_score.py`,
`03_layer3_external_validation.py`, `04_figures.py` — and the names do
not match the actually-committed `02_build_risk_score.py`).

The Viewpoint's central reproducibility claim therefore points at a
specification that has not been written. **What test would falsify
"distributional reproducibility"?** The manuscript needs to answer
three sub-questions before this claim is defensible:

1. *How many re-runs?* "Three times" is stated; what is the
   acceptance threshold under three independent draws? The manuscript
   needs an explicit numeric definition (e.g., majority concordance on
   selected sub-claim across n=k runs at alpha=...).
2. *Concordance on what?* The text names "selected claim, statistical
   method, headline effect size". For the effect size, what
   tolerance? Absolute? Relative? Within bootstrap CI?
3. *Who decides the runs are concordant?* If a human adjudicator
   (Layer 1 producing differently-worded but equivalent methods
   paragraphs) is needed, the falsifier is not machine-checkable; if a
   string-equality check is used, almost every run will fail and the
   claim becomes meaningless. The middle path (semantic equivalence
   via an LLM judge) introduces a new failure mode.

**Required action.** Either commit a working `99_reexec_check.py`
with a concrete falsifier definition before tag, or downgrade the
claim in Section 5 to "single-run reproducibility with
operator-described variability bounds". Pretending a check exists
when it does not is the failure mode the rest of the manifest exists
to prevent.

### 2. Three-layer separation is enforced by honour, not by tool envelope. *Severity: high.*

`docs/design.md` (lines 28–96) defines the three layers and asserts
that "the audit cannot modify Layer 1 artefacts. It can only file
findings." `prompts/02-layer2-audit.md` (lines 16–20, 65–69) puts the
same prohibition in the Layer-2 prompt: "Read, Bash (read-only mode:
no writes to repository files outside `reviewer-logs/audit/`)". This
is the entire enforcement mechanism.

Three problems:

- *The "read-only Bash" prohibition is a string in a prompt.* Bash
  itself is not running in read-only mode at the kernel level; the
  Layer-2 session has full write access to the repository. The
  honesty contract turns on the agent *choosing* not to write
  elsewhere. A future operator pointing the audit prompt at a
  different repository can silently delete the prohibition.
- *No branch protection or pre-receive hook is committed.* Layer 1's
  prompt forbids force-push, amend, rebase (`prompts/01-layer1-
  pipeline.md` lines 52–53; `docs/design.md` lines 85–86), but the
  repository has no `.github/branch-protection.yaml`, no server-side
  hook, no `core.hooksPath` configured, no `pre-receive` script.
  Honesty contract item 2 is technically a comment in a Markdown
  file.
- *Layer separation is collapsible by the operator.* The kickoff
  prompts for Layer 1 and Layer 2 are committed; the *invocations*
  (which model, which session, which working directory) are not.
  Whether Layer 2 was actually started as "a separate, fresh
  session" with no Layer-1 context is a claim the artefact ledger
  cannot verify after the fact.

**Required action.** Either (a) add a `.githooks/pre-commit` or
`.github/workflows/honesty-contract.yml` that mechanically rejects
force-push, rebase, amend, and cross-layer file edits and document
this enforcement layer in `docs/design.md`; or (b) acknowledge in the
manuscript (Section 4 or Limitations) that the three-layer separation
is procedurally — not technically — enforced, and name that as a
residual blind spot.

### 3. The four honesty-contract rules are not technically enforceable as written. *Severity: high.*

`docs/design.md` (lines 80–98) lists four rules:

1. No claim screening.
2. No history rewriting.
3. Failure preservation.
4. No post-hoc instrumentation.

Of these, only rule 2 is potentially mechanically enforceable (via
branch protection on `main` plus a forbid-force-push policy at the
git server). The repository does not currently configure either. Rules
1, 3, 4 are all behavioural and depend on the operator's continued
co-operation.

Worse, two of the rules are partially **violated by the very design
they are paired with**:

- Rule 4 ("metrics not preregistered cannot be promoted to the
  headline finding") was already amended once — `case-study/docs/
  prereg-v2.md` extends the GEO candidate pool *after* the first
  pool failed. The amendment is well-documented in `failure-mode-01-
  cohort-selection.md` and arguably honourable; but the auditor
  cannot tell the difference between "amendment forced by genuine
  data unavailability" and "amendment forced by an unfavourable
  Layer-3 number that has not yet been written down". The honesty
  contract does not differentiate these, so a strict reader has to
  trust that the amendment was authored *before* Layer 3 ran.
- Rule 3 ("failure preservation") is stated, but
  `case-study/data/results/cohort-selection.json` carries a comment
  ("will be overwritten on the next pipeline run") indicating that
  some artefacts are explicitly designed to be non-preserving. This
  is operationally sensible but contradicts the spirit of rule 3
  without a written carve-out.

**Required action.** Add a short "Procedural-vs-technical
enforcement" subsection to `docs/design.md` (and a sentence in the
Viewpoint Section 5 or Limitations) that explicitly names which
honesty rules are technically enforceable, which are operator-trust-
dependent, and which artefacts are intentionally overwritable.

### 4. Disclosure 2.0's defence against citation hallucination is single-pronged and partial. *Severity: high.*

The Zhao et al. corpus-scale audit (cited in the persona prompt; not
yet cited in `manuscript/references.bib` — see Comment 7) found that
LLM-generated literature reviews fabricate references at non-trivial
rates and that the fabrication signal is sometimes *between* a real
DOI and a real-looking citation. The Disclosure 2.0 manifest defends
against this with one mechanism: the Layer-2 audit's "citation
veracity check" (`prompts/02-layer2-audit.md` lines 42–47; mirrored
in `reviewer-logs/audit/citations.md` per the README).

This is necessary but insufficient. The audit prompt specifies
"resolve the DOI or the title via Crossref and PubMed. Record
per-entry: resolved / unresolved / wrong-target-resolved". It does
**not** specify:

- *In-text claim-to-citation alignment.* A real citation that
  is real *and* mis-applied (e.g., the cited paper does not support
  the in-text claim it is attached to) passes the audit. This is
  exactly the failure mode the Zhao audit highlights as
  under-detected by surface-level DOI checks.
- *Author-list correctness.* `wang2010` in `references.bib` carries
  a hand-note ("the formal cohort citation is the GSE14520
  description in Roessler et al. 2010, which appears under the same
  accession. Verify final author list against PubMed at submission")
  and `grinchuk2018` carries "to be re-verified by the Layer-2 audit
  subagent". The audit prompt does not currently encode an author-
  list comparison.
- *Year and journal-volume sanity.* `coscientist2026` and
  `luSakana2026` are dated 2026 and carry verification notes "PMID
  ... verified PubMed 2026-05-21"; the audit prompt would re-verify
  the DOI but not the PMID-DOI agreement.

Additionally, the bibliographic record itself contains placeholders
that subvert the manifest: `repoprereg` has
`<<PREREG_COMMIT_SHA>>` and `lintom2026`'s arXiv id is "to be
inserted at submission". If the tagged release is the immutable
disclosure unit, these placeholders need to be resolved **before**
the tag, not at submission.

**Required action.** Extend `prompts/02-layer2-audit.md`'s citation
check to include in-text alignment (per-cite passage-to-claim
mapping) and author-list cross-check; either resolve the bibliography
placeholders before tag or move them out of the immutable artefact
into a manuscript-companion file that is allowed to mutate.

### 5. The artefact ledger is described as deterministically regenerable; the generator does not yet exist. *Severity: blocker.*

`docs/design.md` lines 99–106:

> `docs/ledger.md` is the chronological narrative that backs Figure 1
> of the Viewpoint. It is generated from `git log --follow --all` plus
> `reviewer-logs/*/summary.md`, regenerated on each release tag, and
> committed back to the repository.

`/usr/bin/find docs -type f` returns three files; `ledger.md` is not
among them. Figure 1 (`manuscript/figures/fig1-artifact-ledger.pdf`)
exists, but the script that produced it is not committed (the figures
directory contains `build_fig2.py` only). The manuscript's central
"the prompt is the protocol" claim hinges on the ledger being
deterministically regenerable from a clean clone; today it is neither
present nor regenerable.

The ledger is the Viewpoint's single most important reproducibility
artefact: it is the surface a reviewer would inspect to evaluate the
"every commit, every reviewer round, every audit checkpoint, every
tag" claim. Without it, Figure 1 is a static screenshot.

**Required action.** Before `viewpoint-v1.0.0` is tagged, commit
`docs/ledger.md` and the generator script (e.g., `scripts/
build_ledger.py`), and add the generator invocation to the Makefile
chain in `manuscript/Makefile`. The Layer-2 audit should test that
the committed ledger matches a re-generated ledger byte-for-byte (or
at least content-equivalent if timestamps are normalised).

### 6. Model-deprecation is named once and immediately dropped. *Severity: medium.*

The Limitations section (lines 166–168) says: "The current model
identifier (Anthropic Claude Opus 4.7, 1M-context variant) is one of
several relevant systems; cross-vendor portability is an open
question." This is the only place the manuscript mentions that the
pinned model has a deprecation horizon.

Three concrete gaps:

- *No graceful-degradation path.* When Anthropic eventually retires
  `claude-opus-4-7`, every reproducer who tries to re-run Layer 1
  against the snapshot date will fail. The manifest needs a stated
  policy for that case: re-run on the closest available successor
  with a labelled-as-divergent badge, or freeze the artefact at the
  date of deprecation with the audit log explicitly noting the
  model is no longer reproducible from API.
- *Snapshot fidelity is API-side.* "Snapshot date 2026-05-20"
  encodes that the operator believes the model behaviour was stable
  on that date; Anthropic may apply hidden fine-tuning updates
  retroactively keyed to the same model id. The manifest cannot
  detect this from the client side. The manuscript should
  acknowledge that "snapshot date" is best-effort, not bit-stable.
- *Cross-vendor portability.* Mentioned once; not given a recipe.
  A reproducer who has only GPT-5 or Gemini-3-Pro is left with no
  guidance.

**Required action.** Add one paragraph to Section 5 (or Limitations)
naming the deprecation policy: which artefacts survive deprecation
(committed transcripts, the analysis code, the manuscripts), which
are model-dependent and degrade (re-execution against the pinned
model), and what counts as a "Disclosure 2.0 second-best"
reproduction.

### 7. Zhao et al. corpus-scale hallucination audit is the persona's anchor; the manuscript does not cite it. *Severity: medium.*

The persona prompt (`prompts/04-viewpoint-reviewer-methodology.md`
line 20) explicitly names "the recent Zhao et al. corpus-scale
citation-hallucination audit (2026)" as the empirical anchor for the
defence-against-hallucination argument. The Viewpoint's Section 2,
which discusses scientific hallucination as one of three failure
modes motivating current policy, currently cites only the
Sakana/Lu et al. Nature 2026 paper's self-reported limitations
(`luSakana2026`). The Zhao audit is the corpus-scale evidence; its
absence weakens the manuscript's empirical footing.

**Required action.** Either add the Zhao 2026 citation to the
`references.bib` and to Section 2's hallucination paragraph, or
explicitly state (in the manuscript or a methods-companion note)
that the manuscript draws only on self-reported hallucination
evidence and not the corpus-scale audit, with the reason. The 30-
reference ceiling for Lancet Viewpoints can absorb one more entry.

### 8. The reviewer-subagent transcripts are committed verbatim, but reviewer-side hallucination is acknowledged only in passing. *Severity: medium.*

Section 5 of the manuscript (lines 150–151):

> Documented and demonstrated in `reviewer-logs/round-01/methods.md`,
> where the methods reviewer fabricated a non-existent citation.
> Disclosure 2.0 handles this by preserving the fabrication and
> recording its resolution rather than silently deleting it.

`reviewer-logs/round-01/` is currently **empty** (the directory does
not yet exist in the working tree). The manuscript is citing an
artefact that has not yet been produced. This is the same failure
mode as Comment 5 (forward-reference to a non-existent file) and
should be resolved on the same review round.

More substantively, the reviewer-subagent loop is itself non-
deterministic: the same persona prompt on the same draft on
different days may emit different review comments. The Disclosure
2.0 manifest does not require reviewer-loop reproducibility, only
that the *output transcripts* are preserved verbatim. This is a
defensible choice but should be named in Section 4 or Limitations:
the reader is reading the reviewer transcripts that *did* occur, not
the ones that *would* occur on a re-run.

**Required action.** When the reviewer round 1 artefacts land,
update Section 5 to point at the actual file path; add one sentence
acknowledging that the reviewer-subagent loop is itself
non-deterministic and that distributional-reproducibility applies to
the analytic pipeline, not to the reviewer comments.

### 9. The `docs/disclosure2-schema.json` referenced in Section 6 does not exist. *Severity: medium.*

Section 6 of the manuscript (lines 161–162):

> A reference schema accompanies this Viewpoint at
> `docs/disclosure2-schema.json`.

`/usr/bin/find docs -name 'disclosure2-schema*'` returns nothing.
This is the third forward-reference to a non-existent artefact
(after `99_reexec_check.py` and `docs/ledger.md`). Each individually
is a missing file; collectively they raise a methodology-review
concern that the manuscript was drafted ahead of the repository
state and the file-citation discipline of the manifest does not
extend to internal cross-references.

The manifest's strongest claim is that **every artefact the manuscript
cites is in the tagged release**. Three forward-references break that
claim. Either the artefacts land before tag, or the manuscript's
cross-references are downgraded to "intended" rather than
"accompanies this Viewpoint".

**Required action.** Commit a draft `docs/disclosure2-schema.json`
even if minimal (one YAML or JSON schema covering the six manifest
items); or remove the reference from Section 6 and restate it as
"will be released as a companion artefact".

### 10. The "single operator cannot audit himself" counter-argument is rebutted by appeal to Layer 2; Layer 2's seal is honour-based. *Severity: medium.*

Section 5 (lines 148–149): "Layer 2 is a sealed audit subagent with
no contact with Layer 1." This is the operative rebuttal to the most
serious philosophical objection to single-operator agentic research.

The seal is enforced by (i) the Layer-2 prompt instruction "you may
not contact Layer 1's session" and (ii) the operator dispatching
Layer 2 in a fresh Claude Code session. Neither is auditable from
the committed repository. The Layer-2 transcript will record that
the session was fresh; the transcript itself is produced by the same
operator who could in principle have run a "Layer 1 leaking into
Layer 2" session and committed only the clean-looking transcript.

**Required action.** Add a session-launch attestation (a small
`reviewer-logs/audit/session-launch.json` containing the Claude Code
session id, the working-directory hash, and a checksum of the
Layer-1 commit range the audit was dispatched against) and document
in Section 5 or Limitations that the seal is testimonial and
externally re-runnable rather than cryptographically enforced.

## Failure modes the manifest does not catch (named)

The persona prompt asks for an explicit enumeration. The seven
following residual blind spots survive the six-item Disclosure 2.0
manifest as currently specified:

1. **Reviewer-AI collusion.** Nothing in the manifest prevents an
   operator from running Layer 1 and the reviewer subagents from the
   same model with subtle persona-prompt edits that bias the loop
   toward accepting the operator's preferred result. The personas are
   committed; the *invocation* against the model is not auditable.
2. **Prompt-text drift via whitespace and Unicode.** "Closed for
   edits" means semantically closed; the manifest does not require a
   committed SHA-256 of each prompt artefact. A zero-width-space
   substitution in the operator-spec prompt would not show up in a
   normal diff.
3. **Layer-3 cohort-knowledge leakage via the operator's memory.**
   The operator is a clinician who could have prior knowledge of
   GSE14520 / GSE76427 effect sizes from the literature. The
   manifest treats the operator's mind as a sealed black box; in
   reality, the operator's prior knowledge could have shaped the
   Layer-3 threshold of 0.03. The manifest cannot detect this.
4. **Selective failure preservation.** The honesty contract requires
   preserving failures, but does not require preserving *failed
   runs that produced unfavourable numbers*. An operator who ran
   Layer 1 three times and committed only the third run's transcript
   would technically violate rule 2 (no history rewriting) only if
   the unproductive runs were committed first; if they were never
   committed, the manifest cannot tell.
5. **The audit subagent's own hallucinations.** Layer 2 runs the
   same model class as Layer 1. Its citation-veracity check could
   mark a real fabrication as resolved (the Crossref/PubMed query
   returns a near-match; the agent decides it's the same paper).
   The audit is not externally re-audited.
6. **Tool-envelope drift.** "Tool envelope = Read, Edit, Write,
   Bash, ..." is committed as text. The actual tool envelope present
   in the session is set by Claude Code at launch and could include
   tools not in the committed list (e.g., MCP servers configured in
   the operator's `~/.claude/settings.json` and inherited by the
   session). The manifest does not require dumping the realised
   tool envelope.
7. **The "Disclosure 2.0 of Disclosure 2.0".** The Viewpoint itself
   was drafted with AI assistance per `docs/ai-usage-disclosure.md`,
   but the manifest the Viewpoint proposes treats the Viewpoint's
   own drafting prompts (the operator-spec plus iterative drafting)
   as covered by the same six items. There is no separate prompt
   trail for the Viewpoint manuscript's *prose revisions across
   reviewer rounds*. If a reviewer-subagent comment in round N
   suggests rephrasing, and the operator-plus-Claude rewrites
   accordingly, the *intermediate diff* is captured by git but not
   labelled as AI-assisted vs operator-edited. The acknowledgement
   paragraph in the manuscript (lines 191–192) blanket-attributes
   all of it to Claude, which is honest but coarse.

The single most consequential failure mode is **#5: the audit
subagent's own hallucinations** — because the manifest's entire
trust chain ultimately rests on Layer 2 being right, and Layer 2 is
the same kind of system as Layer 1. The manuscript should name this
explicitly in Limitations.

## Recommended path to `accept` in round 2

1. Land `99_reexec_check.py` with a concrete numeric falsifier;
   land `docs/ledger.md` and its generator; land
   `docs/disclosure2-schema.json` (Comments 1, 5, 9).
2. Decide and disclose: is the three-layer separation technical or
   procedural? Either install branch protection / git hooks or name
   the seal as testimonial in the manuscript text (Comments 2, 3, 10).
3. Strengthen the audit prompt with in-text citation-claim alignment
   and author-list verification; resolve the bibliography
   placeholders before tag (Comment 4).
4. Add the deprecation and snapshot-fidelity paragraph (Comment 6).
5. Cite the Zhao corpus-scale hallucination audit, or explicitly
   declare its absence (Comment 7).
6. Add the named-residual-failure-mode paragraph to the manuscript's
   Limitations, drawing on items 1–7 of the section above.

With those changes, the methodology axis would clear `accept`. None
of them require re-writing the architecture; all of them are
documentation, schema and one short Python script away.

## Verdict

`major-revision`. The architecture is sound, the prompts are
sound, the case-study Layer-1 honesty response (failure-mode-01) is
exemplary; but three artefacts the manuscript points to do not yet
exist (`99_reexec_check.py`, `docs/ledger.md`,
`docs/disclosure2-schema.json`), the three-layer seal is honour-
based, and the residual blind spots are present in the design
document but absent from the manuscript text. Fix the forward-
references, name the residual blind spots in the manuscript, and the
methodology axis clears.
