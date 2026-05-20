# `case-study/` — Layer 1 Pipeline Output

This directory is the empirical artefact the Viewpoint manuscript refers
to as "the case study". It is produced by Layer 1 of the architecture in
`../docs/design.md` — a single Claude Code session that received exactly
one domain prompt and operated autonomously from that point onward.

The case study is not a stand-alone publication. It is illustrative
material for Figure 1 and Section 3 of the Viewpoint and is positioned
as such in the manuscript text. The case-study manuscript here is itself
a Layer-1 product and is included as supplementary evidence.

## Domain prompt (recap)

> "Use TCGA-LIHC plus public GEO cohorts (GSE14520, GSE76427 reserved for
> external validation) to refine overall-survival stratification of
> hepatocellular carcinoma beyond AJCC pathologic stage. Produce a
> reproducible analytic pipeline, a draft manuscript matched to a clearly
> identified clinical-genomics journal's submission specifications, and
> four reviewer-subagent rounds until unanimous ACCEPT."

The full Layer 1 kickoff prompt is in `../prompts/01-layer1-pipeline.md`.

## Subdirectories

```
analysis/        numbered scripts (planned: 01_prepare_data.py ..
                 05_figures.py, 99_reexec_check.py)
data/raw/        TCGA-LIHC + GEO downloads, gitignored
data/processed/  harmonised inputs, gitignored
data/results/    small analytic artefacts kept in-repo
figures/         figure PDFs for the case-study manuscript
manuscript/      Layer-1-produced LaTeX manuscript with its own
                 references.bib, Makefile, and JOURNAL.md targeting the
                 case-study's chosen clinical-genomics journal
```

## Honesty rules specific to the case study

- `analysis/` scripts are committed as Layer 1 produced them. Any
  operator-side fix is a separate commit with a message naming the
  Layer-1 failure mode it patches.
- The case-study manuscript is committed as Layer 1 produced it across
  reviewer rounds. The Layer-3 external-validation result is appended in
  a clearly delimited section by the operator; that section's commit
  message identifies it as operator-authored.
- No data file in `data/raw/` is redistributed; only the documented
  download recipe is kept. Licensing of TCGA / GEO permits free
  re-download.

## Re-execution

```bash
uv sync
cd case-study
uv run python analysis/01_prepare_data.py
uv run python analysis/02_layer1_risk_score.py
uv run python analysis/03_layer3_external_validation.py
uv run python analysis/04_figures.py
cd manuscript && make
```

Re-execution is part of Layer 2 (audit). The audit transcript is in
`../reviewer-logs/audit/`.
