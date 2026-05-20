# `reviewer-logs/` — Reviewer-Subagent and Audit Transcripts

This directory holds the verbatim outputs of the four reviewer subagents
(per round) and the Layer-2 audit subagent. Each transcript is committed
as it was received, with no editorial smoothing, and is not edited after
the corresponding tag is pushed.

## Layout

```
round-01/            first reviewer round (after case-study draft v0.1)
  methods.md           methods reviewer (rigor, leakage, stability)
  clinical.md          clinical reviewer (HCC oncology context, translation)
  biostat.md           biostatistics reviewer (Cox assumptions, power, MTP)
  editor.md            target-journal editor persona (scope, novelty, fit)
  summary.md           one-page summary; revision decisions per comment
round-02/            second round (after revision)
  methods.md, clinical.md, biostat.md, editor.md, summary.md
round-03/, round-04/, ...
audit/               Layer-2 audit subagent transcripts
  reexec.md            re-execution log
  citations.md         BibTeX-vs-Crossref/PubMed verification log
  statistics.md        stat-reproduction log
  findings.md          consolidated audit findings (cross-linked from
                       docs/ledger.md)
```

## Filename convention

- `methods.md`, `clinical.md`, `biostat.md`, `editor.md` — one file per
  reviewer, per round.
- `summary.md` — per-round summary written by the pipeline (Layer 1)
  collating the four reviewers' comments and recording the revision
  decision for each comment with a one-letter code:
    `A` accepted into next revision
    `R` rejected with a one-paragraph rationale
    `D` deferred to the next round
- `decisions.json` — machine-readable mirror of `summary.md`, used by the
  ledger generator.

## Closure rule

A round is closed when the four reviewers' `decisions.json` files all
contain `verdict: "accept"` at the top level. The closing commit is
tagged `case-study-vX.Y.Z` per the versioning convention in
`docs/design.md`.

## Audit closure

`audit/findings.md` is closed when Layer 2 has reported on all four
audit checks (re-execution, citations, statistics, claim alignment). The
closing commit is referenced from the Viewpoint manuscript's "Data and
Code Availability" statement.

## What this directory is *not*

- Not the place where Layer 1 thinks. Layer 1's chain-of-thought is not
  captured here; what is captured is the *output artefacts* (reviewer
  comments and audit findings), with the prompts that produced them in
  `../prompts/`.
- Not redacted. If a reviewer subagent hallucinated a citation or made an
  incorrect statistical claim, the comment is preserved and the
  resolution is recorded in `summary.md`.
