# Failure mode 05 — GPL5474 annotation file not downloaded

**Detected by**: Layer 2 audit on `case-study-v1.0.0`, finding F1 (blocker)
(`reviewer-logs/audit/findings.md`).

**Symptom**: `case-study/analysis/02_build_risk_score.py` requires
`case-study/data/raw/GPL5474.annot.txt` to map Illumina probe IDs to
gene symbols for the GSE10143 external scoring step.
`case-study/analysis/01_prepare_data.py` did not download this file.
On a clean clone (where raw data is gitignored), the external-cohort
branch of the pipeline failed; `04_figures.py` then crashed; the
in-tree `99_reexec_check.py` reported FAIL.

**Impact on `case-study-v1.0.0`**: The committed external-cohort
results (`external_geo_scores.tsv`, GSE10143 C-index 0.47, log-rank
p = 0.13) were valid at the time they were produced (the annotation
file was present on the operator's local disk), but were not
reproducible from a clean clone. Five claims in the case-study
manuscript depended on the external-cohort branch and inherited the
reproducibility gap.

**Resolution path (case-study-v1.0.1)**: `01_prepare_data.py` adds a
`_download_gpl_annotation(platform_id)` helper that fetches the
chosen-platform's GPL annotation file from NCBI's FTP server,
decompresses, and writes to `case-study/data/raw/<platform>.annot.txt`.
The `main()` flow calls this after `harmonise_geo` based on the
chosen platform recorded in `data-prep-manifest.json`.

**Status of the original failure**: preserved verbatim. The audit
finding remains in `reviewer-logs/audit/findings.md` as F1 (blocker).
The Viewpoint manuscript at `viewpoint-v1.1.0` cites the original
`case-study-v1.0.0` failure as evidence the Layer-2 audit catches
reproducibility gaps. `case-study-v1.0.1` is a forward-moving fix
release that does not modify `case-study-v1.0.0`.

**Verification**: on a clean clone of the repository at
`case-study-v1.0.1`, running `uv sync` followed by
`uv run python case-study/analysis/01_prepare_data.py` produces
`case-study/data/raw/GPL5474.annot.txt`. `02_build_risk_score.py`
then proceeds to score GSE10143 without intervention.
