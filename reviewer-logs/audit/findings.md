# Layer-2 Audit — Consolidated findings

**Tag**: `case-study-v1.0.0` (commit `99d01b5`)
**Audit closure date**: 2026-05-21
**Auditor**: Layer 2 sealed Claude Code session.

Severity scale: `low / medium / high / blocker`. A blocker is a
finding that invalidates a headline number in the abstract or breaks
the pipeline's documented reproducibility claim on a clean clone.

Per-axis transcripts:

- `reexec.md` — re-execution log
- `citations.md` — Crossref / PubMed citation veracity log
- `statistics.md` — independent statistical reproducibility log
- `claim_alignment.md` — claim-to-data alignment log

## F1 — External-cohort scoring is not reproducible on a clean clone (BLOCKER)

- Location: `case-study/analysis/02_build_risk_score.py:639-643, 721`; `case-study/analysis/01_prepare_data.py` (the absence is the finding).
- Severity: blocker.
- Statement: The external-cohort C-index of 0.47 (95% CI [0.36, 0.58]) and the median-split log-rank p = 0.13 in GSE10143, which appear in the abstract (lines 73-76), Results External (lines 465-475), Methods Secondary outcomes (line 275), Figure 4, and Table 2 of the manuscript, cannot be regenerated from the tagged release. The probe-to-gene mapper `_gpl5474_probe_to_gene()` reads `case-study/data/raw/GPL5474.annot.txt`, which is never downloaded by `01_prepare_data.py`, never committed, and the helper silently returns an empty dict when the file is absent. On a fresh worktree + `uv sync` + sequential `01..05` execution, the external scoring loop raises `FATAL: no signature genes present in external cohort`, the entire secondary L2 / L6 block of `tcga_bootstrap_metrics.json` is `None`, the external block of `figures_inputs.json` is `None`, and `04_figures.py` exits 1 with a `TypeError` while drawing Figure 4. The pipeline's own in-tree `99_reexec_check.py` reports FAIL on the audit re-execution. The reproducibility unit advertised in the manuscript Methodological contribution (lines 156-160) and Data and Code Availability (lines 600-605) is therefore unmet for the external-validation portion of the headline.

## F2 — Abstract reports legacy estimator while methods name paired-optimism as headline (HIGH)

- Location: `case-study/manuscript/main.tex:65-67` (abstract); `:251-261` (methods); `:371-382` (results); `:384-400` (Table 2).
- Severity: high.
- Statement: The abstract states "the optimism-corrected ΔC was 0.060 (95% bootstrap CI 0.085 – 0.137)". The Methods Primary outcome explicitly names the paired-optimism estimator as the headline and labels the round-1 legacy estimator as "reported for traceability" only. The committed `tcga_bootstrap_metrics.json` records `delta_c_corrected_paired = 0.063` with 95% CI [0.003, 0.113], whereas `delta_c_corrected_legacy = 0.060` with 95% CI [0.083, 0.139]. The abstract's "0.060" and "[0.085, 0.137]" correspond to the round-01 legacy estimator (`tcga_bootstrap_metrics_round01.json`), not the headline paired-optimism estimator. Under the paired-optimism estimator the preregistered primary-hypothesis lower-bound threshold (> 0) is cleared by only 0.003 (vs ≈ 0.085 under legacy); the effective margin is order-of-magnitude smaller than the abstract conveys.

## F3 — "Stage-stratified" Cox HR (7.34) is untraceable (HIGH)

- Location: `case-study/manuscript/main.tex:433-437`; `case-study/analysis/03_subgroup_and_robustness.py:228-243`.
- Severity: high.
- Statement: The Results section claims that "a stage-stratified Cox (stratifying by stage 1-2 vs 3-4) was fit; HCC-TRS retained its independent effect with HR per 1-SD of 7.34 (95% CI 4.04–13.33, p = 1.9e-10)." The committed `stage_stratified_cox.tsv` records TRS HR = 6.66 (95% CI 3.86 – 11.52, p = 1.09e-11), and the saved model is a stage-adjusted bivariable Cox, not a true `strata=`-stratified Cox. The HR = 7.34 and its CI do not appear in any committed result file (`grep -rn "7\\.34\\|4\\.04\\|13\\.33" case-study/data/results/` returns no hits). The claim cannot be traced to a regenerable computation.

## F4 — Bootstrap signature-stability claim contradicts the artefact (MEDIUM)

- Location: `case-study/manuscript/main.tex:456-463`; `case-study/data/results/tcga_bootstrap_metrics_round01.json`.
- Severity: medium.
- Statement: The manuscript states median Jaccard ≈ 0.6 and 60-75% gene recovery per bootstrap. The regenerated bootstrap JSON records `bootstrap_signature_median_jaccard_with_apparent = 0.2048` and `bootstrap_signature_median_apparent_recovery_pct = 34.0`. The manuscript values overstate the actual values (Jaccard ≈ 0.2, recovery ≈ 34%) by roughly 2-3×. Either the claim is incorrect or the field names are mislabelled; in either case the reader is misled about signature stability.

## F5 — `rich2017quality` DOI resolves to a different work; no PubMed match exists (MEDIUM)

- Location: `case-study/manuscript/references.bib:89-98`.
- Severity: medium (the entry is uncited; would be high if cited).
- Statement: The BibTeX entry `rich2017quality` ("Quality of survivorship care in hepatocellular carcinoma", Rich/Yopp/Singal, JNCCN 2017, DOI 10.6004/jnccn.2017.0117) does not refer to a real paper. The DOI resolves to "NCCN Guidelines Insights: Antiemesis, Version 2.2017" by Berger et al. PubMed searches for the cited author-title combination return zero hits. The entry appears to be hallucinated. It is not cited in `main.tex`, so the error does not propagate to the reader, but it ships in the release as a Layer-1 failure mode.

## F6 — `nault2013novel` BibTeX title is incorrect (LOW)

- Location: `case-study/manuscript/references.bib:143-152`.
- Severity: low (entry is uncited).
- Statement: The BibTeX title is "A novel prognostic gene signature in early-stage hepatocellular carcinoma" but the DOI 10.1053/j.gastro.2013.03.051 resolves to "A Hepatocellular Carcinoma 5-Gene Score Associated With Survival of Patients After Liver Resection" (Nault et al., Gastroenterology 2013, 145:176-187, PMID 23567350). DOI is correct, title is paraphrased/fabricated. Entry is uncited.

## F7 — Nine BibTeX entries are present but uncited (LOW)

- Location: `case-study/manuscript/references.bib`.
- Severity: low.
- Statement: 30 entries shipped, 21 cited. Uncited: `cancer2017comprehensive`, `boyault2007transcriptome`, `rich2017quality` (F5), `nault2013novel` (F6), `wolbers2014concordance`, `steyerberg2010assessing`, `villa2016neoangiogenesis`, `barrett2013ncbi`, `benjamini1995controlling`. The unused entries do not affect the rendered `main.pdf` but inflate the references list relative to the citation graph.

## F8 — `llovet2018hepatocellular` BibTeX key is misleading (LOW)

- Location: `case-study/manuscript/references.bib:78-87`.
- Severity: low.
- Statement: Bib key is `llovet2018hepatocellular` but `year=2021` and the DOI resolves to Llovet et al., Nat Rev Dis Primers 2021 (PMID 33479224). The bib year is correct; only the key string is misleading.

## F9 — `tcga.tarball_sha256` drifts between committed and re-execution (LOW)

- Location: `case-study/data/results/data-prep-manifest.json:tcga.tarball_sha256`.
- Severity: low.
- Statement: On audit re-execution, the GDC-bundle tarball hashes to `229acad7a4f3...` rather than the committed `8f563232a61c...`. All downstream TCGA-derived deterministic artefacts reproduce bit-exactly, so the SHA drift is on upstream-server packaging. The pipeline does not pin or verify a SHA; the manifest records whatever it downloaded. `99_reexec_check.py` correctly flags this. The manuscript does not claim SHA stability, so this is informational only.

## F10 — `04_figures.py` exits non-zero when external scoring fails (MEDIUM)

- Location: `case-study/analysis/04_figures.py:151-167`.
- Severity: medium.
- Statement: When `figures_inputs.json:external` is `None` (the state reached on a clean clone via F1), `figure4()` calls `f"{c:.2f}"` on `None` and raises `TypeError`, causing `04_figures.py` to exit 1. Figures 1-3 are produced before the exception. Combined with F1, the documented sequential build of `01..04` does not run to completion on a fresh clone.

## F11 — `_calibration_slope` re-standardises before fitting (LOW)

- Location: `case-study/analysis/02_build_risk_score.py:507-516`; `case-study/manuscript/main.tex:410-414`.
- Severity: low.
- Statement: The committed `_calibration_slope` re-standardises the score before fitting Cox, so the reported 0.70 is the Cox coefficient on the standardised score. This is consistent with the manuscript text ("standardised HCC-TRS") but is not the conventional Royston slope-on-linear-predictor (which on raw HCC-TRS returns 2.15). A reader applying the conventional definition will not reproduce 0.70.

## F12 — Two Schoenfeld p-values for TRS exist in different result files (LOW)

- Location: `tcga_bootstrap_metrics.json:secondary.L5_schoenfeld_p_trs = 0.3797`; `robustness_metrics.json:schoenfeld.trs_p = 0.2571`.
- Severity: low.
- Statement: The pipeline computes Schoenfeld's global p for the TRS covariate twice (univariable in 02; bivariable in 03). The manuscript cites the univariable value (0.38). Both numbers are shipped in different JSON files; a careless reader might compare to the wrong file.

## Pass / fail per audit axis

- Re-execution: FAIL on the external-cohort axis (F1, F10); PASS on all TCGA-internal axes (bit-exact reproduction of every deterministic artefact).
- Citation veracity: FAIL on 1 entry (F5); META-MISMATCH on 1 uncited entry (F6); META-MISMATCH on 1 cited entry's key-vs-year (F8). Net: 28 of 30 entries correctly resolve.
- Statistical reproducibility: PASS on deterministic statistics (within 1e-6) and on the paired-optimism bootstrap CI (within 1e-9). FAIL on the abstract's quoted "0.060 (95% CI 0.085 – 0.137)" (F2); FAIL on stage-stratified HR = 7.34 (F3); FAIL on Jaccard ≈ 0.6 (F4).
- Claim-vs-data alignment: 31 of 35 enumerated quantitative claims trace to a regenerable script line and result file. 4 do not (rolled into F1, F3, F4).

## Total reviewer-detectable issues

12 findings filed. By severity: 1 blocker (F1), 2 high (F2, F3), 3 medium (F4, F5, F10), 6 low (F6, F7, F8, F9, F11, F12).
