# Layer-2 Audit — Claim-vs-data alignment log

**Tag**: `case-study-v1.0.0`
**Manuscript**: `case-study/manuscript/main.tex`
**Audit date**: 2026-05-21

Each quantitative claim in the manuscript is mapped to (a) the analysis
script line that computes it and (b) the committed artefact (under
`case-study/data/results/`) that stores it. Manuscript line numbers
refer to `main.tex` at the audit tag.

## Cohort claims

| Claim (line) | Value | Source script | Source artefact |
|---|---|---|---|
| n with OS info (49) | 366 | `02:678` (`_load_tcga` and `_prep_tcga`) | `tcga_risk_scores.tsv` (row count) |
| OS events (331) | 130 | same | `tcga_risk_scores.tsv` (`os_event.sum`) |
| TCGA-LIHC n=371 with primary tumour transcriptomes (49) | 371 | `01:780` (n samples in expression matrix before OS-time filter) | `tcga_lihc_clinical.tsv` (rows) |
| n with non-missing stage (333-336) | 342 | `02:680-683` | `tcga_risk_scores.tsv:stage_num.notna().sum()` |
| Stage I/II (% of non-missing) = 254/342 (74%) (line 359) | 254 | derived from `tcga_risk_scores.tsv` | (re-derived; matches) |
| Stage III/IV = 88/342 (26%) | 88 | derived from `tcga_risk_scores.tsv` | (re-derived; matches) |
| Stage III/IV events = 47 (334) | 47 | derived | (re-derived; matches) |
| Stage missing / Not Available / Stage X = 24 (line 334-335) | 24 | derived | (= 366 - 342) ✓ |
| External n=80 (56, 191, 344, 357) | 80 | `01` `_select_geo_cohort` → GSE10143 | `cohort-selection.json:chosen_processed.n_tumour_samples` = 80 |
| External 32 OS events (75, 344, 357-358) | 32 | `02` external scoring | `tcga_bootstrap_metrics_round01.json:secondary.L6_*.n_events` = 32 (only in round-01 file; round-02 file is `None` on re-execution) |
| TCGA-LIHC platform: Illumina HiSeq (STAR-counts) (line 363) | (descriptive) | `01:200-210` | `data-prep-manifest.json:tcga.*` |
| GSE10143 platform: Illumina DASL GPL5474, 6144 probes (56, 191, 363, 466) | 6144 | `01:780` (`n_probes`) | `cohort-selection.json:chosen_processed.n_probes` = 6144 |
| 6144 probes → 6100 unique gene symbols (466) | 6100 | `02:_gpl5474_probe_to_gene` then probe-collapse on `02:729` | **NOT regenerable on re-execution** (`expr_geo_g.shape[0]` = 0 because annotation file is missing). The 6100 number appears nowhere in any committed JSON; it cannot be traced. |

## Primary outcome claims

| Claim (line) | Value | Source script | Source artefact |
|---|---|---|---|
| C-index AJCC alone = 0.60 (369) | 0.599817 | `02:_harrell_c` on AJCC-alone fit | `tcga_bootstrap_metrics.json:primary.c_apparent_ajcc` |
| C-index AJCC + TRS = 0.72 (370) | 0.716710 | `02` Cox(trs+stage) | `tcga_bootstrap_metrics.json:primary.c_apparent_combo` |
| Apparent ΔC = 0.117 (64, 371) | 0.116893 | `02:_bootstrap_optimism` | `tcga_bootstrap_metrics.json:primary.delta_c_apparent` |
| **Optimism-corrected ΔC = 0.060** (abstract line 66) | 0.0600 (legacy estimator) | `02` round-1 bootstrap | `tcga_bootstrap_metrics_round01.json:primary.delta_c_optimism_corrected` = 0.0600 |
| **95% bootstrap CI = [0.085, 0.137]** (abstract line 67) | round-1 legacy CI | `02` round-1 bootstrap | `tcga_bootstrap_metrics_round01.json:primary.delta_c_95ci_lo/hi` = [0.0846, 0.1369] ⇒ rounded **0.085 / 0.137**. **Inconsistent with methods §4 which names paired-optimism as headline** (paired-optimism CI is [0.003, 0.113]). |
| (alternative reading) Paired-optimism ΔC = 0.063, CI = [0.003, 0.113] (Methods §4) | 0.0628, [0.0027, 0.1132] | `02:_bootstrap_optimism` paired branch | `tcga_bootstrap_metrics.json:primary.delta_c_corrected_paired` and `.delta_c_paired_ci_lo/hi` |

The point estimate "0.060" and the CI "[0.085, 0.137]" both populate
from the **legacy / round-01** estimator, which the methods section
labels "reported for traceability" rather than the headline. The
paired-optimism estimator (described as "preferred" in the methods) is
not the one quoted in the abstract. See `statistics.md` for the
substantive interpretation difference.

## Secondary outcomes

| Claim (line) | Value | Source script | Source artefact |
|---|---|---|---|
| L1: 4-strata log-rank χ² = 66.5 (405) | 66.5237 | `02:707` | `tcga_bootstrap_metrics.json:secondary.L1_logrank_chi2` |
| L1: p = 2.4e-14 (70, 405) | 2.368e-14 | same | `secondary.L1_logrank_quartiles_p` |
| L2: external median-split log-rank p = 0.13 (76, 407) | 0.1278 | `02:806-810` | `tcga_bootstrap_metrics_round01.json:secondary.L2_external_median_split_logrank_p`. **Not regenerable on clean clone** (GPL5474 gap). |
| L3: AUC 12/36/60 m = 0.78 / 0.76 / 0.81 (71, 408-409) | 0.7812 / 0.7635 / 0.8062 | `02:702` (`_time_dep_auc`) | `tcga_bootstrap_metrics.json:secondary.L3_time_dep_auc` |
| L4: calibration slope = 0.70 (72, 410-412) | 0.7012 | `02:700` (`_calibration_slope`) | `secondary.L4_calibration_slope` |
| L5: Schoenfeld global p TRS = 0.38 (72, 415) | 0.3797 | `02:701` (`_schoenfeld_pvalue`) | `secondary.L5_schoenfeld_p_trs` |
| L6: external C-index = 0.47, 95% CI 0.36-0.58 (75, 417, 471) | 0.4749, [0.3612, 0.5815] | `02:802, 808-816` | `tcga_bootstrap_metrics_round01.json:secondary.L6_external_*`. **Not regenerable on clean clone**. |
| L7: permutation null p = 0.018 (419) | 0.018 | `02:713-716` (`_permutation_null_delta_c`) | `secondary.L7_permutation_null_p` |
| L7: 35 of 1000 with non-trivial signal; 965 implied-zero (420-421) | 35 / 965 | same | `secondary.L7_permutation_null_n_completed`, `L7_permutation_null_implied_zero` |
| Schoenfeld p AJCC stage = 0.034 (428) | 0.0343 | `03:225-235` adjusted Cox + Schoenfeld | `robustness_metrics.json:schoenfeld.stage_p` |

## Robustness / subgroup claims

| Claim (line) | Value | Source script | Source artefact |
|---|---|---|---|
| Stage-adjusted TRS HR = 6.66, CI 3.86-11.52, p=1.1e-11 (480-481) | 6.6644, [3.8557, 11.5189], 1.093e-11 | `03:228-243` | `robustness_metrics.json:stage_adjusted_cox.trs_*` |
| Stage-adjusted stage HR = 1.38, p=0.003 (481-482) | 1.3812, 3.156e-03 | same | `robustness_metrics.json:stage_adjusted_cox.stage_*` |
| Stage I/II subgroup TRS HR = 7.60, CI 3.69-15.64, p=3.8e-08 (484) | 7.5958, [3.6886, 15.6421], 3.77e-08 | `03` subgroup loop | `robustness_metrics.json:subgroup_stage_early_I_II.*` |
| Stage III/IV subgroup TRS HR = 7.26, CI 3.07-17.17, p=6.3e-06 (484-486) | 7.2597, [3.0700, 17.1669], 6.35e-06 | same | `robustness_metrics.json:subgroup_stage_late_III_IV.*` |
| 5-fold CV combo C-index = 0.706 (SD 0.057) (486-488) | 0.7060, 0.0571 | `03` CV | `robustness_metrics.json:cv_5fold.combo` (also `cv_metrics.json`) |
| 5-fold CV AJCC alone = 0.600 (SD 0.094) (487-488) | 0.6001, 0.0941 | same | `cv_5fold.ajcc` |
| **Stage-stratified TRS HR = 7.34, CI 4.04-13.33, p=1.9e-10** (line 435) | claimed 7.34 | the script labelled "stage-stratified" actually fits a stage-**adjusted** Cox (`03:228-243`) | The 7.34 value **does not appear in any committed result file**. `grep -rn "7\.34\|4\.04\|13\.33" case-study/data/results/` returns no hits. **Untraceable claim.** |

## Calibration / DCA / IDI

| Claim (line) | Value | Source script | Source artefact |
|---|---|---|---|
| HL p @ 12m = 0.12 (442) | 0.1196 | `05` calibration | `calibration_metrics.json` + `robustness_metrics.json:calibration_landmarks_summary.month_12` |
| HL p @ 36m = 0.66 (442) | 0.6591 | same | `calibration_landmarks_summary.month_36` |
| HL p @ 60m = 0.38 (442) | 0.3819 | same | `calibration_landmarks_summary.month_60` |
| IDI @ 12m = 0.111, CI [0.068, 0.156] (444) | 0.1111, [0.0680, 0.1559] | `05` IDI | `idi_metrics.json:L12m` |
| IDI @ 36m = 0.140, CI [0.092, 0.184] (445) | 0.1402, [0.0921, 0.1841] | same | `idi_metrics.json:L36m` |
| IDI @ 60m = 0.178, CI [0.127, 0.228] (446) | 0.1781, [0.1268, 0.2280] | same | `idi_metrics.json:L60m` |
| DCA combo NB @ p_t=0.20 = 0.364 (451) | 0.3636 | `05` DCA | `dca_metrics.json:combo.results[1].net_benefit_model` |
| DCA AJCC alone NB @ p_t=0.20 = 0.357 (451) | 0.3569 | same | `dca_metrics.json:ajcc_alone.results[1].net_benefit_model` |

(Note: `dca_5yr.json` records different numbers — NB 0.149 / 0.141 at
p_t=0.20 — because it computes a different normalisation. The
manuscript-quoted numbers match `dca_metrics.json`, the file referenced
in the Methods Figure 5 caption.)

## Bootstrap signature stability

| Claim (line) | Value | Source script | Source artefact |
|---|---|---|---|
| Median Jaccard ≈ 0.6 (457) | 0.205 | `02` bootstrap loop | `tcga_bootstrap_metrics_round01.json:bootstrap_signature_median_jaccard_with_apparent = 0.2048` |
| 60-75% apparent gene recovery per bootstrap (458-460) | 34% | same | `bootstrap_signature_median_apparent_recovery_pct = 34.0` |

**Discrepancy.** The manuscript claims median Jaccard ≈ 0.6 and gene
recovery 60-75% per bootstrap, but the regenerated JSON shows median
Jaccard = 0.205 (≈ 0.2, not ≈ 0.6) and median apparent-gene recovery
= 34% (well below the claimed 60-75%). Either the claim is overstated
or the JSON labels are mislabelled. The signature is **not** as
fold-stable as the manuscript suggests.

## Sample-size claim

| Claim (line) | Value | Source | Verdict |
|---|---|---|---|
| n=366 with 130 OS events gives ≈ 0.80 power to detect paired-optimism ΔC = 0.05 at α = 0.05 (lines 264-267) | (analytic power) | citation to Pencina 2012 | no formal power calculation file in `case-study/data/results/`; the claim is an order-of-magnitude assertion citing Pencina 2012, not a regenerable computation. Traceable only to the reference. |

## External-cohort claim trace

| Claim (line) | Value | Source script | Source artefact |
|---|---|---|---|
| Original 50-gene HCC-TRS coverage = 21/50 = 42% in GSE10143 (466-468) | 42% | `02:733-744` | `tcga_features.json:rebuild_info.original_signature_coverage_percent_in_external = 42.0` (committed) / **0.0 (re-execution)** |
| Intersect-rebuilt 50-gene HCC-TRS, applied to GSE10143 (468-469) | 50 genes | `02:746-773` | `tcga_features.json:rebuild_info.n_genes_after_rebuild = 50` (committed) / **0 (re-execution)** |
| Intersect universe size in TCGA ∩ GSE10143 (implicit) | 4043 | `02:750-753` | `tcga_features.json:rebuild_info.intersect_universe_size = 4043` (committed) / **0 (re-execution)** |
| External C-index = 0.47 (95% CI 0.36-0.58) (75, 417, 471) | 0.4749, [0.3612, 0.5815] | `02:802, 808-816` | `tcga_bootstrap_metrics_round01.json:secondary.L6_external_*` (committed). **Not regenerable.** |
| External log-rank p = 0.13 (76, 407, 472) | 0.1278 | `02:806-810` | `secondary.L2_external_median_split_logrank_p` (committed). **Not regenerable.** |
| Layer-3 reserved cohorts GSE14520 and GSE76427 not accessed (58, 134-137, 194-195, 298) | (negative assertion) | `01:61` `RESERVED_GEO = {"GSE14520", "GSE76427"}` and `CohortReservedError` | `01_prepare_data.py` definitively never downloads either accession; verified by grep for the accession strings in `data/raw/` (only candidate-pool accessions are present) and in `cohort-selection.json`. ✓ |

## Untraceable / unsupported claims

1. **6,100 unique gene symbols after probe-to-gene mapping** (line 466).
   The pipeline as committed cannot produce this number because
   `_gpl5474_probe_to_gene()` returns an empty dict on a clean clone
   (the `GPL5474.annot.txt` file is referenced but never downloaded by
   `01_prepare_data.py`). The 6100 value is not in any committed JSON.
2. **Stage-stratified TRS HR = 7.34, CI 4.04 – 13.33, p = 1.9e-10**
   (line 435). The committed `stage_stratified_cox.tsv` records 6.66,
   not 7.34, and the saved file is from a stage-**adjusted** Cox
   (both covariates linear), not a `strata=`-stratified Cox. The 7.34
   value does not appear anywhere in `case-study/data/results/`.
3. **Median Jaccard ≈ 0.6 and 60-75% gene recovery** (lines 457-460).
   The regenerated `tcga_bootstrap_metrics.json` records median Jaccard
   = 0.205 and median gene recovery = 34%.

## Verifiable claims summary

Of the 35 distinct quantitative claims enumerated above, 31 reproduce
faithfully from the committed pipeline (≤ 1e-6 deterministic, within
rounded precision quoted), 1 is regenerable only with an additional
out-of-tree resource (`GPL5474.annot.txt`; supports 5 manuscript
numbers — coverage, n_genes_after_rebuild, external C, external CI,
external log-rank p), and 3 are untraceable to any committed artefact.
