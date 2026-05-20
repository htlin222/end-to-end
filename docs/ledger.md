# Artefact Ledger

Regenerated from `git log` by `scripts/regenerate_ledger.py`. Re-run after every commit or at release time. This file is the source of truth behind Figure 1 in the Viewpoint and is referenced from `docs/design.md` Section ``Repository as artefact ledger''.

## Summary

- Total commits: **52**
- AI-co-authored commits: **52**
- Operator-only commits: **0**
- Tags: case-study-v1.0.0, viewpoint-v1.0.0
- First commit: 2026-05-20T16:17:31+00:00
- Latest commit: 2026-05-20T19:52:20+00:00

## Chronological narrative

| # | Time (UTC) | SHA | Layer | Author | Subject |
|---:|---|---|---|---|---|
| 1 | 2026-05-20 16:17 | `0a4c904` | Viewpoint | AI-co-authored | chore: scaffold reproducible-study skeleton from end-to-end-study skill |
| 2 | 2026-05-20 16:18 | `59e7faf` | Layer 1 | AI-co-authored | refactor: restructure into single-repo layout for Lancet DH Viewpoint submission |
| 3 | 2026-05-20 16:19 | `851c61b` | Docs | AI-co-authored | docs: add design document specifying three-layer architecture |
| 4 | 2026-05-20 16:20 | `a639cc7` | Viewpoint | AI-co-authored | manuscript: distil Lancet Digital Health Viewpoint specs into JOURNAL.md |
| 5 | 2026-05-20 16:21 | `3bb07d0` | Docs | AI-co-authored | docs: publish AI usage disclosure before any AI-assisted content |
| 6 | 2026-05-20 16:23 | `252c1e1` | Prompts | AI-co-authored | prompts: commit operator-supplied orchestration spec verbatim |
| 7 | 2026-05-20 16:24 | `88d6d15` | Docs | AI-co-authored | docs: preregister case-study Layer-3 external validation design |
| 8 | 2026-05-20 16:26 | `35c1869` | Layer 1 | AI-co-authored | docs: rewrite top-level README and add case-study + reviewer-logs READMEs |
| 9 | 2026-05-20 16:32 | `6861743` | Viewpoint | AI-co-authored | manuscript: draft Lancet DH Viewpoint v0.1 (compiles, 6 pages, ~2476 words) |
| 10 | 2026-05-20 16:35 | `84869b9` | Prompts | AI-co-authored | prompts: add Layer 1 / Layer 2 / four reviewer-persona kickoff prompts |
| 11 | 2026-05-20 16:36 | `663101d` | Operator | AI-co-authored | chore: lock Python dependencies via uv |
| 12 | 2026-05-20 16:40 | `ef234c7` | Viewpoint | AI-co-authored | manuscript: draft cover letter and medRxiv preprint metadata |
| 13 | 2026-05-20 16:43 | `22f2250` | Viewpoint | AI-co-authored | manuscript: add Figure 2 (policy-gap matrix) and supporting build script |
| 14 | 2026-05-20 16:43 | `207e9ef` | Operator | AI-co-authored | chore: add CITATION.cff for Zenodo deposit and downstream citations |
| 15 | 2026-05-20 16:46 | `a99cd3f` | Layer 1 | AI-co-authored | case-study: layer-1 prereg, session plan, JOURNAL.md, data-prep stub |
| 16 | 2026-05-20 17:03 | `a609f69` | Layer 1 | AI-co-authored | case-study: extend GEO candidate pool after failure-mode-01 |
| 17 | 2026-05-20 17:28 | `f5a0e9b` | Viewpoint | AI-co-authored | manuscript: replace Sakana arXiv cite with Lu et al. Nature 2026, add ARS counter-argument, add Nature editorial response |
| 18 | 2026-05-20 17:30 | `c694f07` | Prompts | AI-co-authored | prompts: add four Viewpoint-specific reviewer personas |
| 19 | 2026-05-20 17:33 | `a573625` | Viewpoint | AI-co-authored | manuscript: correct author lists for roessler2010 and grinchuk2018 |
| 20 | 2026-05-20 17:34 | `e008175` | Viewpoint | AI-co-authored | manuscript: substitute <<USER>> placeholders with the operator's verified GitHub handle |
| 21 | 2026-05-20 17:37 | `209e75d` | Layer 1 | AI-co-authored | manuscript: replace Figure 1 placeholder with deterministic git-log-derived artefact ledger |
| 22 | 2026-05-20 17:39 | `3c43693` | Reviewer | AI-co-authored | docs+scripts: ship Disclosure 2.0 schema and ledger generator (resolves reviewer-flagged hallucinated artefacts) |
| 23 | 2026-05-20 17:51 | `da4ddce` | Viewpoint | AI-co-authored | manuscript: v0.4 — full revision addressing 44 Round 1 reviewer comments |
| 24 | 2026-05-20 17:51 | `0810331` | Viewpoint | AI-co-authored | chore: regenerate Figure 1 ledger and docs/ledger.md after v0.4 revision |
| 25 | 2026-05-20 17:52 | `5fde223` | Reviewer | AI-co-authored | reviewer-logs: add Round 1 response-to-reviewers cross-reference table |
| 26 | 2026-05-20 17:54 | `79fe4ca` | Docs | AI-co-authored | docs: add procedural-vs-technical enforcement subsection and overwritable-artefact carve-out |
| 27 | 2026-05-20 17:57 | `69c479e` | Reviewer | AI-co-authored | scripts: add release_check.sh preflight for tagged-release readiness |
| 28 | 2026-05-20 17:59 | `c7b6586` | Viewpoint | AI-co-authored | v0.4.1: address R2 minors (word-count consistency, Layer~N hyphenation, residual failure modes in Limitations, schema toolEnvelope coupling) |
| 29 | 2026-05-20 18:00 | `49d4766` | Reviewer | AI-co-authored | reviewer-logs: Round 2 response-to-reviewers + bring all R2 reviewer outputs into repo |
| 30 | 2026-05-20 18:00 | `be58d8e` | Viewpoint | AI-co-authored | chore: regenerate ledger and Figure 1 after R2 closure (29 commits) |
| 31 | 2026-05-20 18:02 | `04c72e8` | Operator | AI-co-authored | docs: add RELEASE_NOTES.md template for viewpoint-v1.0.0 |
| 32 | 2026-05-20 18:07 | `dd7b3e4` | Viewpoint | AI-co-authored | v0.4.2: R3 minor (word count 2281->2428 in title page + cover letter) + release_check.sh fixes |
| 33 | 2026-05-20 18:07 | `4836c7a` | Reviewer | AI-co-authored | reviewer-logs: bring all four Round 3 reviewer transcripts and decisions.json into repo |
| 34 | 2026-05-20 18:07 | `98bd5eb` | Viewpoint | AI-co-authored | chore: regenerate ledger + Figure 1 after R3 closure |
| 35 | 2026-05-20 18:12 | `c805bb4` | Reviewer | AI-co-authored | reviewer-logs: bring all four Round 4 reviewer transcripts into repo + Round 4 closure |
| 36 | 2026-05-20 18:12 | `60a8c7f` | Viewpoint | AI-co-authored | release: finalise RELEASE_NOTES.md and regenerate ledger + Figure 1 at viewpoint-v1.0.0 boundary |
| 37 | 2026-05-20 18:14 | `94b65de` | Layer 1 | AI-co-authored | chore: gitignore release/ staging dir + record viewpoint-v1.0.0 tag |
| 38 | 2026-05-20 18:30 | `d7edc1f` | Layer 1 | AI-co-authored | case-study: prereg-v3 amendment caps signature at 50 genes (failure-mode-02) |
| 39 | 2026-05-20 18:41 | `816cb92` | Layer 1 | AI-co-authored | case-study: treat screen-zero permutations as null delta=0 (failure-mode-03) |
| 40 | 2026-05-20 18:42 | `ec93b6d` | Layer 1 | AI-co-authored | case-study: commit Layer-1 analytic artefacts (TCGA-LIHC + GSE10143) |
| 41 | 2026-05-20 18:42 | `ef68872` | Layer 1 | AI-co-authored | case-study: commit four manuscript figures (KM, forest, AUC, external KM) |
| 42 | 2026-05-20 18:42 | `fd825bd` | Layer 1 | AI-co-authored | case-study: add 99_reexec_check.py + manuscript references.bib + cover letter |
| 43 | 2026-05-20 18:50 | `cf5d224` | Reviewer | AI-co-authored | reviewer-logs/round-01: four reviewer transcripts + summary + decisions.json |
| 44 | 2026-05-20 19:00 | `585be81` | Layer 1 | AI-co-authored | case-study: round-02 revision (paired-optimism + DCA + IDI + calibration) |
| 45 | 2026-05-20 19:04 | `d7b9918` | Layer 1 | AI-co-authored | case-study: round-02 data artefacts (paired-optimism CI + DCA + IDI + calibration) |
| 46 | 2026-05-20 19:09 | `a87586c` | Layer 1 | AI-co-authored | reviewer-logs: Round 2 (case-study) — unanimous accept |
| 47 | 2026-05-20 19:12 | `612846a` | Layer 1 | AI-co-authored | case-study: post-tag polish from Layer 1 v2 (reproducibility tolerance + Uno IPCW caveat) |
| 48 | 2026-05-20 19:46 | `59a48dc` | Layer 2 | AI-co-authored | reviewer-logs/audit: Layer-2 four per-axis transcripts |
| 49 | 2026-05-20 19:46 | `109a432` | Layer 2 | AI-co-authored | reviewer-logs/audit: consolidated findings.md (12 findings, 1 blocker) |
| 50 | 2026-05-20 19:48 | `ecf8475` | Layer 1 | AI-co-authored | case-study: Layer 3 external validation — preregistered NULL result |
| 51 | 2026-05-20 19:50 | `5ffd6df` | Viewpoint | AI-co-authored | manuscript: v0.5 — Layer 3 NULL headline + Layer 2 audit reference |
| 52 | 2026-05-20 19:52 | `99d9cfe` | Operator | AI-co-authored | docs: update RELEASE_NOTES.md for viewpoint-v1.1.0 (post-Layer-3 + Layer-2-audit) |

## Tags

- **case-study-v1.0.0** — 2026-05-20T19:09:57+00:00
- **viewpoint-v1.0.0** — 2026-05-20T18:12:37+00:00

