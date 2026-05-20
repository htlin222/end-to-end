# Layer-2 Audit — Re-execution log

**Tag**: `case-study-v1.0.0` (commit `99d01b5`)
**Worktree**: `/tmp/cs-audit` (created with `git worktree add /tmp/cs-audit case-study-v1.0.0`)
**Audit date**: 2026-05-21
**Auditor**: Layer 2 Claude Code session (claude-opus-4-7, 1M-context variant)

## Environment

- Python 3.12.11 via `uv sync` (warning about external `VIRTUAL_ENV` was ignored).
- Pinned dependency versions resolved by `uv.lock`:
  - lifelines 0.30.3
  - scikit-learn 1.8.0
  - statsmodels 0.14.6
  - pandas 2.3.3
  - numpy 2.4.6
  - scipy 1.17.1
- Working directory `/tmp/cs-audit`; data was redownloaded from public sources;
  internet access used only via the documented endpoints in
  `case-study/analysis/01_prepare_data.py` (GDC API, NCBI GEO FTP).

## Execution order

1. `git worktree add /tmp/cs-audit case-study-v1.0.0` — succeeded.
2. Snapshotted committed `case-study/data/results/` to
   `/tmp/cs-audit-committed-results/` for later diffing.
3. `uv sync` — succeeded; 30 packages resolved and installed in
   `/tmp/cs-audit/.venv`.
4. Ran scripts sequentially:
   - `01_prepare_data.py` — exit code 0, silent stdout.
   - `02_build_risk_score.py` — exit code 0, but emitted
     `FATAL: no signature genes present in external cohort.` during
     external scoring (see "Probe-to-gene annotation gap" below).
   - `03_subgroup_and_robustness.py` — exit code 0.
   - `04_figures.py` — **exit code 1**, `TypeError: unsupported format
     string passed to NoneType.__format__` in `figure4()` (downstream
     consequence of the script-02 external-scoring failure).
   - `05_dca_idi_calibration.py` — exit code 0.
   - `99_reexec_check.py` — exit code 1 (FAIL), reporting drift in
     `tcga_bootstrap_metrics.json`, `tcga_features.json`,
     `figures_inputs.json`, and `data-prep-manifest.json`.

## File-by-file diff against committed artefacts

`diff -q` (binary equality) of every committed file in
`case-study/data/results/` against the regenerated counterpart:

| File | Result |
|------|--------|
| `calibration_landmarks.json` | EQUAL |
| `calibration_metrics.json`   | EQUAL |
| `cohort-selection.json`      | EQUAL |
| `cv_metrics.json`            | EQUAL |
| `data-prep-manifest.json`    | DIFF (timestamp + `tcga.tarball_sha256` mismatch + indentation) |
| `dca_5yr.json`               | EQUAL |
| `dca_metrics.json`           | EQUAL |
| `external_geo_scores.tsv`    | EQUAL (because script 02 took the FATAL branch and never overwrote the committed file) |
| `figures_inputs.json`        | DIFF (external block populated in committed copy, absent in regen) |
| `idi_metrics.json`           | EQUAL |
| `idi.json`                   | EQUAL |
| `robustness_metrics.json`    | EQUAL |
| `stage_stratified_cox.tsv`   | EQUAL |
| `tcga_bootstrap_metrics_round01.json` | EQUAL |
| `tcga_bootstrap_metrics.json` | DIFF (`secondary.L2_external_*` and `secondary.L6_external_*` populated in committed, `None` in regen; `external.*` block populated in committed) |
| `tcga_cox_summary.txt`       | EQUAL |
| `tcga_features.json`         | DIFF (`rebuild_info.intersect_universe_size`: committed 4043 vs regen 0; `n_genes_after_rebuild`: 50 vs 0; `original_signature_coverage_percent_in_external`: 42.0 vs 0.0) |
| `tcga_model_coefs.tsv`       | EQUAL |
| `tcga_risk_scores.tsv`       | EQUAL |
| `uno_c_sensitivity.json`     | EQUAL |

## TCGA tarball SHA mismatch

`data-prep-manifest.json` records `tcga.tarball_sha256` for the
GDC-bundle that `01_prepare_data.py` downloaded. The committed manifest
records `8f563232a61cb5e047db81972b04c99554a90a33ecf2107f34d2a0f2e5b90f3b`;
the audit re-download recorded
`229acad7a4f3c44ea2b0a742862472e2dae43c8515226414a70ddafb17b6184f`. This
indicates that the GDC-side bundle returned by the same documented API
call is not byte-stable across days. The downstream effect on the
analytic TSVs is nil — all TCGA-derived deterministic artefacts
(`tcga_risk_scores.tsv`, `tcga_model_coefs.tsv`, `tcga_cox_summary.txt`,
`robustness_metrics.json`, `cv_metrics.json`, `dca_*.json`,
`calibration_*.json`, `idi*.json`, `tcga_bootstrap_metrics.json` primary
block) reproduce bit-exactly because the script normalises after the
download. The SHA drift is therefore a manifest-only artefact, not a
results discrepancy. The pipeline does not pin or verify a GDC-side
SHA, so any change in GDC packaging would alter the manifest while
leaving results identical.

## Probe-to-gene annotation gap (script 02)

`02_build_risk_score.py` line 721 calls `_gpl5474_probe_to_gene()`,
defined at line 639 to parse `case-study/data/raw/GPL5474.annot.txt`.
That file is **never downloaded by `01_prepare_data.py`**, never
committed to the repository, and the helper silently returns an empty
dict when the file is absent. On a clean clone, the empty dict yields
zero genes after probe-collapse, which triggers
`FATAL: no signature genes present in external cohort` and the entire
external block of `tcga_bootstrap_metrics.json` /
`figures_inputs.json` is left `None` / "error".

The committed result files (`external_geo_scores.tsv`,
`tcga_bootstrap_metrics_round01.json`,
`tcga_bootstrap_metrics.json:secondary.L6_*`, `figures_inputs.json:external.*`)
contain real numbers, which means the file was present on the original
Layer-1 machine when those artefacts were generated, but the means by
which it got there is **not in the pipeline**. The honest reading is
that the external-cohort C-index of 0.475 (95% CI [0.36, 0.58]) and
median-split log-rank p = 0.128 reported in the manuscript abstract,
Results §External, and Table 2 cannot be regenerated from the tag on a
fresh machine.

`99_reexec_check.py` (in-tree distributional reproducibility check)
detected this drift on re-execution and reported FAIL — i.e., the
pipeline's own internal check confirms the gap.

## Verbatim stdout (selected)

### 01_prepare_data.py
```
(no stdout)
```

### 02_build_risk_score.py (tail)
```
Refitting final model on full TCGA cohort ...
Running 1000-iter permutation null for ΔC ...
  permutation iter 100/1000
  ...
  permutation iter 1000/1000
Scoring external GEO cohort ...
Loaded GSE10143: 80 samples, 6144 probes; probe-to-gene mapping size = 0
After probe->gene collapse: 0 genes in external cohort
HCC-TRS signature coverage in GSE10143: 0.0% (0 of 50 signature genes present)
FATAL: no signature genes present in external cohort.

=== HEADLINE ===
Apparent ΔC (AJCC+TRS vs AJCC)  = 0.1169
Optimism-corrected ΔC           = 0.0628
Bootstrap 95% CI                = [0.0027, 0.1132]
External GSE10143 C-index         = None
External median-split log-rank p = None
```

### 04_figures.py
```
Generating figure 1 (KM by TCGA quartile) ...
Generating figure 2 (forest) ...
Generating figure 3 (AUC / calibration) ...
Generating figure 4 (external KM) ...
Traceback (most recent call last):
  File "/private/tmp/cs-audit/case-study/analysis/04_figures.py", line 173, in <module>
    sys.exit(main())
             ^^^^^^
  File "/private/tmp/cs-audit/case-study/analysis/04_figures.py", line 167, in main
    figure4()
  File "/private/tmp/cs-audit/case-study/analysis/04_figures.py", line 151, in figure4
    f"C-index = {c:.2f} ({ci_lo:.2f}-{ci_hi:.2f}); "
                ^^^^^^^
TypeError: unsupported format string passed to NoneType.__format__
```

### 99_reexec_check.py (verdict)
```
FAIL — re-execution drift exceeded tolerance:
  - tcga_bootstrap_metrics.json:external.* fields: present in committed, None in regen
  - tcga_features.json:rebuild_info.intersect_universe_size: 4043 vs 0
  - tcga_features.json:rebuild_info.n_genes_after_rebuild: 50 vs 0
  - tcga_features.json:rebuild_info.original_signature_coverage_percent_in_external: 42 vs 0
  - figures_inputs.json:external.* fields: present in committed, None in regen
  - data-prep-manifest.json:tcga.tarball_sha256: str mismatch (committed vs regen)
```

## Concordance summary

- **TCGA-LIHC internal analyses reproduce bit-exactly** for all
  deterministic outputs (model coefficients, risk scores, bootstrap
  primary, secondary L1/L3/L4/L5/L7, robustness, subgroups, CV, DCA,
  IDI, calibration).
- **External GSE10143 analyses do not reproduce**: secondary L2 and
  L6 cannot be computed from the pipeline as committed because the
  GPL5474 probe-to-gene annotation file is referenced but never
  downloaded. Figure 4 fails. The committed external numbers are
  therefore not independently regenerable from the tag.
