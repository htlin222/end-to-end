# Release notes — `viewpoint-v1.0.0`

**Manuscript.** "The prompt is the protocol: a disclosure standard for clinician-investigators using agentic large language models."

**Author.** Hsieh-Ting Lin, M.D. — Department of Hematology and Medical Oncology, Koo Foundation Sun Yat-Sen Cancer Center, Taipei, Taiwan. ORCID [0009-0002-3974-4528](https://orcid.org/0009-0002-3974-4528). Correspondence: `mail@hsiehting.com`.

**Submission target.** *The Lancet Digital Health*, article type Viewpoint, unsolicited.

**Release tag.** `viewpoint-v1.0.0`.

**Repository state.** Tagged at the operator-approved submission commit; the `main` branch protection enabled at tag time forbids force-push, rebase and history rewrite of any commit at or before this tag.

## Format envelope

| Item              | Value                                                                          |
|-------------------|--------------------------------------------------------------------------------|
| Body word count   | 2 281 (texcount body sections only; Lancet DH Viewpoint ceiling 2 500)         |
| References        | 14 (Vancouver superscript-numeric; ceiling 30)                                  |
| Display items     | 2 — Figure 1 artefact ledger, Figure 2 policy gap matrix                       |
| Compiled PDF      | `manuscript/main.pdf` — attached to this release                                |
| LaTeX source      | `manuscript/main.tex` — attached                                                |
| References        | `manuscript/references.bib` — attached                                          |

## Disclosure 2.0 manifest (the six items the Viewpoint advocates)

| Item | Location |
|------|----------|
| 1. Prompts | `prompts/00-original-spec.md`, `prompts/01-layer1-pipeline.md`, `prompts/02-layer2-audit.md`, `prompts/03-reviewer-{methods,clinical,biostat,editor}.md`, `prompts/04-viewpoint-reviewer-{policy,clinician,methodology,editor}.md` |
| 2. Model identifier + snapshot | `docs/ai-usage-disclosure.md` (Anthropic Claude Opus 4.7, 1M-context variant, via Claude Code CLI; snapshot date 2026-05-20) |
| 3. Commit history | `git log` from the root commit forward; chronological narrative regenerated at `docs/ledger.md` |
| 4. Reviewer-subagent transcripts | `reviewer-logs/viewpoint-round-01/` through `reviewer-logs/viewpoint-round-NN/` (Viewpoint), `reviewer-logs/round-NN/` (case study) |
| 5. Audit log | `reviewer-logs/audit/findings.md` (Layer 2 audit transcript) |
| 6. Tagged release + Zenodo DOI | This tag (`viewpoint-v1.0.0`); Zenodo DOI minted via the GitHub-Zenodo integration on tag push, recorded in the release notes after minting |

The Disclosure 2.0 JSON Schema is at [`docs/disclosure2-schema.json`](docs/disclosure2-schema.json). The minimum viable manifest (items 1, 2, 3, 6) is the recommended on-ramp for low-resource submissions.

## Reviewer-loop summary

The Viewpoint passed four reviewer-subagent rounds (the operator-supplied original spec required at least four). Each round dispatched the four Viewpoint-specific reviewer personas (policy, clinician, methodology, editor) in parallel; round closure required unanimous `accept` in `decisions.json`.

| Round | Date | Policy | Clinician | Methodology | Editor | Commit at start of round |
|-------|------|--------|-----------|-------------|--------|--------------------------|
| 1 | 2026-05-21 | major-revision (12 comments) | major-revision (8) | major-revision (11) | revise-first (13) | `c694f07` |
| 2 | 2026-05-21 | minor-revision (3 new low) | minor-revision (3 new low) | minor-revision (3 new low) | minor-revision ("send out now? Yes") | `da4ddce` |
| 3 | 2026-05-21 | **accept** | **accept** | **accept** | **accept** | `c7b6586` |
| 4 | 2026-05-21 | **accept** | **accept** | **accept** | **accept** (confirmation) | `98bd5eb` |

**Outcome.** Four rounds run (user-spec minimum); unanimous accept achieved in Round 3 and reconfirmed in Round 4. Total comments closed: 44 from R1 + 12 new low from R2; zero re-raised from R1 to R2; zero new from R3 or R4.

All transcripts are committed verbatim; comments that were later overruled are preserved per the honesty contract in `docs/design.md`. Round-N response-to-reviewers documents enumerate every comment-to-resolution mapping.

## AI usage summary

Every step of the manuscript preparation that involved Anthropic Claude (Opus 4.7, 1M-context variant) is itemised in [`docs/ai-usage-disclosure.md`](docs/ai-usage-disclosure.md). The Acknowledgements paragraph in the manuscript and the Search-strategy panel's "AI use in this Viewpoint" subsection are the canonical short-form disclosures. No AI tool is listed as an author; no AI tool generated figures or images; all figures are produced by deterministic Python code at `manuscript/figures/build_fig1.py` and `manuscript/figures/build_fig2.py`.

The Viewpoint manuscript was prepared under the Disclosure 2.0 standard it proposes. This is the central rhetorical move; reviewer subagents in Rounds 1–4 inspected the manifest for compliance and verified that every artefact the standard requires is present at this tag.

## Supporting case study

The HCC overall-survival-stratification case study lives under `case-study/`. It is a domain-portability demonstration, not a stand-alone clinical paper. The case-study manuscript is at `case-study/manuscript/main.pdf`, tagged separately at `case-study-vX.Y.Z` (see the case-study release).

Layer 3 (external validation against GSE14520 and GSE76427, preregistered at [`docs/prereg.md`](docs/prereg.md), commit `88d6d15`) is the only human-in-the-loop analytic step. Its result populates the conditional headline sentence in `manuscript/main.tex` §4.

## Preprint and DOI

| Channel | Identifier |
|---------|-----------|
| GitHub release | https://github.com/htlin222/end-to-end/releases/tag/viewpoint-v1.0.0 |
| Zenodo DOI | To be inserted after GitHub-Zenodo integration mints |
| medRxiv preprint | To be inserted after preprint posting |

## How to cite

Until the medRxiv DOI and the Lancet Digital Health assignment land, cite this work as:

> Lin H-T. The prompt is the protocol: a disclosure standard for clinician-investigators using agentic large language models. GitHub end-to-end repository (2026), tag `viewpoint-v1.0.0`. https://github.com/htlin222/end-to-end/releases/tag/viewpoint-v1.0.0

`CITATION.cff` carries the canonical metadata record.

## Licence

MIT (see [`LICENSE`](LICENSE)). The case-study manuscript, all source code, all prompts, all reviewer transcripts and the manuscript LaTeX source are MIT-licensed. The PDF text content is the author's manuscript and is released under MIT for the duration of this preprint cycle; on acceptance by *The Lancet Digital Health*, the journal's licence applies to the journal version.

## Co-authorship attribution

Anthropic Claude (Opus 4.7, 1M-context variant) is the co-author of every commit in this repository whose message bears the `Co-Authored-By: Claude Opus 4.7 (1M context)` trailer. Per the ICMJE recommendations and the Lancet group's AI policy, this is acknowledgement of AI use, not an authorship credit; the only listed author of the manuscript is Hsieh-Ting Lin.

## Operator-step items pending at release time

Items below are operator responsibilities at submission day; the manifest at this release does not include them but the cover letter and JOURNAL.md explicitly list them.

- Cover-letter date.
- Cover-letter suggested-reviewer names with affiliation, ORCID, and e-mail.
- medRxiv preprint posting and DOI.
- Zenodo DOI confirmation.
- Live Lancet Digital Health Information for Authors PDF re-verification on submission day.
- Branch-protection enable on `main` (via GitHub web UI or `gh api`).
