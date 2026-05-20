"""Layer 3 external validation — preregistered.

Applies the Layer-1-locked HCC-TRS (50 genes + Cox coefficients from
case-study/data/results/tcga_model_coefs.tsv) to the two preregistered
external cohorts (GSE14520, GSE76427) per docs/prereg.md.

Primary outcome: ΔC-index = C(AJCC stage + HCC-TRS) - C(AJCC stage),
in the pooled external cohort. 1000-iteration bootstrap percentile CI.
Reject H0 if 95% CI lower bound > 0.

The Layer-1 risk score is NOT modified. Genes absent from an external
platform are dropped from the score; coverage is reported.

Outputs:
  case-study/data/results/layer3_validation.json — primary + secondaries
  case-study/data/raw/layer3/ — downloaded GEO series matrices
  case-study/data/processed/layer3_*.tsv — harmonised inputs
"""
from __future__ import annotations

import gzip
import io
import json
import os
import sys
import time
import urllib.request
import warnings
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from lifelines import CoxPHFitter
from lifelines.utils import concordance_index

warnings.simplefilter("ignore")

REPO_ROOT = Path(__file__).resolve().parents[2]
CASE = REPO_ROOT / "case-study"
RES = CASE / "data" / "results"
RAW = CASE / "data" / "raw" / "layer3"
PROC = CASE / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROC.mkdir(parents=True, exist_ok=True)

SEED = 20260521
N_BOOTSTRAP = 1000
DELTA_C_THRESHOLD = 0.03  # preregistered
ALPHA = 0.05

# Preregistered external cohorts
COHORTS = {
    "GSE14520": {
        "platform": "GPL3921",  # Affymetrix HT-HG-U133A
        "matrix_url": (
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE14nnn/GSE14520/"
            "matrix/GSE14520-GPL3921_series_matrix.txt.gz"
        ),
        "gpl_url": (
            "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL3nnn/GPL3921/"
            "annot/GPL3921.annot.gz"
        ),
        # Roessler 2010 deposited series matrix without survival; the
        # clinical fields live in this supplementary file.
        "supplement_url": (
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE14nnn/GSE14520/"
            "suppl/GSE14520_Extra_Supplement.txt.gz"
        ),
    },
    "GSE76427": {
        "platform": "GPL10558",  # Illumina HumanHT-12 V4.0
        "matrix_url": (
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE76nnn/GSE76427/"
            "matrix/GSE76427_series_matrix.txt.gz"
        ),
        "gpl_url": (
            "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL10nnn/GPL10558/"
            "annot/GPL10558.annot.gz"
        ),
        "supplement_url": None,
    },
}


# ----------------------------------------------------------------------
# I/O
# ----------------------------------------------------------------------

def _download(url: str, dest: Path) -> Path:
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    print(f"downloading {url} -> {dest}")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (end-to-end Layer-3 fetcher)"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        dest.write_bytes(r.read())
    print(f"  {dest.stat().st_size/1e6:.1f} MB")
    return dest


def _parse_series_matrix(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (expression DataFrame [probes x samples], sample-metadata DataFrame).

    The series-matrix format repeats `!Sample_characteristics_ch1` once per
    characteristic; each row's values are the per-sample value for that
    characteristic. We keep each row separately and name them
    `Sample_characteristics_ch1__N` so downstream parsing can see all of them.
    """
    sample_meta_rows: list[tuple[str, list[str]]] = []
    sample_ids: list[str] = []
    expr_lines: list[str] = []
    opener = gzip.open if str(path).endswith(".gz") else open
    in_data = False
    char_counter = 0
    with opener(path, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("!series_matrix_table_begin"):
                in_data = True
                continue
            if line.startswith("!series_matrix_table_end"):
                in_data = False
                continue
            if in_data:
                expr_lines.append(line)
                continue
            if line.startswith("!Sample_geo_accession"):
                sample_ids = line.split("\t")[1:]
                sample_ids = [s.strip('"') for s in sample_ids]
            elif line.startswith("!Sample_characteristics_ch1"):
                vals = line.split("\t")[1:]
                vals = [v.strip('"') for v in vals]
                key = f"Sample_characteristics_ch1__{char_counter:02d}"
                char_counter += 1
                sample_meta_rows.append((key, vals))
            elif line.startswith("!Sample_"):
                key = line.split("\t", 1)[0][1:]
                vals = line.split("\t")[1:]
                vals = [v.strip('"') for v in vals]
                sample_meta_rows.append((key, vals))
    # Expression: first line is the header. NCBI series-matrix files
    # double-quote both the header tokens and the probe IDs in each row.
    # Strip those quotes so the probe key matches the GPL annot table.
    def _unquote(s: str) -> str:
        return s.strip().strip('"').strip()
    header = [_unquote(h) for h in expr_lines[0].split("\t")]
    rows = []
    for ln in expr_lines[1:]:
        parts = ln.split("\t")
        if not parts or parts[0].startswith("!"):
            continue
        parts = [_unquote(p) for p in parts]
        rows.append(parts)
    expr = pd.DataFrame(rows, columns=header)
    expr = expr.set_index(expr.columns[0])
    # numeric
    for c in expr.columns:
        expr[c] = pd.to_numeric(expr[c], errors="coerce")
    expr = expr.dropna(how="all")
    # Sample metadata: keep one column per metadata row. Length mismatches
    # (e.g. a metadata row that lists only the channel-1 cells) are padded
    # with empty strings.
    meta_dict: dict[str, list[str]] = {}
    for key, vals in sample_meta_rows:
        if len(vals) < len(sample_ids):
            vals = vals + [""] * (len(sample_ids) - len(vals))
        else:
            vals = vals[: len(sample_ids)]
        meta_dict[key] = vals
    meta = pd.DataFrame(meta_dict, index=sample_ids)
    return expr, meta


def _parse_gpl_annot(path: Path) -> dict[str, str]:
    """Return probe_id -> gene_symbol map from a GPL annot or SOFT file.

    GPL annot files have leading ^Annotation, !Annotation_*, and # column
    descriptions. The actual table begins after !platform_table_begin and
    its first line is the column header (tab-separated). We accept either
    that convention (current) or a plain TSV file with a header line that
    contains "ID" and a "Symbol"-like column (legacy).
    """
    opener = gzip.open if str(path).endswith(".gz") else open
    probe_to_gene: dict[str, str] = {}
    header: list[str] | None = None
    in_table = False
    with opener(path, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            if line.startswith("!platform_table_begin"):
                in_table = True
                continue
            if line.startswith("!platform_table_end"):
                in_table = False
                continue
            if line.startswith(("^", "!", "#")):
                continue
            # If no explicit table marker was seen but the first non-comment
            # line looks like a header with "ID" or "Probe" at position 0,
            # accept it (legacy GPL files without the !platform_table_begin
            # tag, e.g. some Illumina files).
            if not in_table and header is None:
                first = line.split("\t")[0].strip()
                if first.lower() in ("id", "probe_id", "probe id", "illmn_id"):
                    in_table = True
                else:
                    continue
            if not in_table:
                continue
            if header is None:
                header = [h.strip() for h in line.split("\t")]
                continue
            parts = line.split("\t")
            if len(parts) < 1:
                continue
            row = dict(zip(header, parts))
            probe = (
                row.get("ID")
                or row.get("Probe_ID")
                or row.get("ILMN_ID")
                or row.get("Platform_SPOTID")
                or parts[0]
            )
            gene = (
                row.get("Gene symbol")
                or row.get("Symbol")
                or row.get("Gene Symbol")
                or row.get("ILMN_Gene")
                or row.get("Gene_Symbol")
                or ""
            )
            gene = gene.split("///")[0].strip()
            if probe and gene:
                probe_to_gene[probe.strip()] = gene
    return probe_to_gene


# ----------------------------------------------------------------------
# Clinical extraction
# ----------------------------------------------------------------------

def _extract_characteristics(meta: pd.DataFrame) -> pd.DataFrame:
    """Parse !Sample_characteristics_ch1 rows.

    Each row is one field across all samples; values are
    "key: value" strings. The same row may repeat with a different
    key on different lines (one per characteristic).
    """
    char_cols = [c for c in meta.columns if c.startswith("Sample_characteristics_ch1")]
    rows: dict[str, dict[str, str]] = {sid: {"sample_id": sid} for sid in meta.index}
    for c in char_cols:
        for sid, val in meta[c].items():
            v = str(val).strip()
            if ":" not in v:
                continue
            k, vv = v.split(":", 1)
            rows[sid][k.strip().lower()] = vv.strip()
    df = pd.DataFrame.from_dict(rows, orient="index").set_index("sample_id")
    df.columns = [c.lower() for c in df.columns]
    return df


def _tumour_filter(df: pd.DataFrame) -> pd.Series:
    """Return a boolean Series marking tumour samples.

    Checks `tissue` and `diagnosis` columns case-insensitively for HCC
    tumour markers. Always returns a Series of length len(df) (default
    True if neither column present).
    """
    n = len(df)
    if "tissue" in df.columns:
        s = df["tissue"].astype(str).str.lower()
        return s.str.contains("tumor|primary hepatocellular|hcc", regex=True, na=False)
    if "diagnosis" in df.columns:
        s = df["diagnosis"].astype(str).str.lower()
        return s.str.contains("tumor|primary hepatocellular|hcc", regex=True, na=False)
    return pd.Series([True] * n, index=df.index)


def _extract_clinical_GSE14520(meta: pd.DataFrame, supplement_path: Path | None = None) -> pd.DataFrame:
    """GSE14520 clinical = supplementary spreadsheet keyed on Affy_GSM."""
    df_basic = _extract_characteristics(meta)
    df_basic["tumour"] = _tumour_filter(df_basic)
    if supplement_path is None or not supplement_path.exists():
        return df_basic
    sup = pd.read_csv(supplement_path, sep="\t", compression="infer")
    sup.columns = [c.strip() for c in sup.columns]
    gsm_col = next((c for c in sup.columns if c.lower() == "affy_gsm"), None)
    if gsm_col is None:
        return df_basic
    sup = sup.set_index(gsm_col)
    merged = df_basic.join(sup, how="left", rsuffix="_supp")
    # Refine the tumour mask using the supplement's "Tissue Type" column
    if "Tissue Type" in merged.columns:
        merged["tumour"] = merged["Tissue Type"].astype(str).str.lower().str.contains("tumor", na=False)
    return merged


def _extract_clinical_GSE76427(meta: pd.DataFrame, supplement_path: Path | None = None) -> pd.DataFrame:
    df = _extract_characteristics(meta)
    df["tumour"] = _tumour_filter(df)
    return df


# ----------------------------------------------------------------------
# Risk score application
# ----------------------------------------------------------------------

def _load_layer1_coefs() -> pd.DataFrame:
    return pd.read_csv(RES / "tcga_model_coefs.tsv", sep="\t")


def _apply_risk_score(expr_g: pd.DataFrame, coefs_df: pd.DataFrame) -> tuple[pd.Series, dict]:
    """expr_g: samples x genes (one expression per sample). Returns z-scored risk per sample."""
    sig_genes = coefs_df["covariate"].tolist()
    present = [g for g in sig_genes if g in expr_g.columns]
    missing = [g for g in sig_genes if g not in expr_g.columns]
    coverage = len(present) / len(sig_genes)
    cov_info = {
        "n_signature_genes": len(sig_genes),
        "n_present": len(present),
        "coverage": coverage,
        "missing_genes": missing,
    }
    # Z-score within cohort, per gene
    z = (expr_g[present] - expr_g[present].mean()) / expr_g[present].std().replace(0, 1)
    # Apply coefficients
    coef_map = coefs_df.set_index("covariate")["coef"]
    score = (z * coef_map[present]).sum(axis=1)
    return score, cov_info


# ----------------------------------------------------------------------
# Stats
# ----------------------------------------------------------------------

def _c_index(score: np.ndarray, t: np.ndarray, e: np.ndarray) -> float:
    return float(concordance_index(t, -score, e))


def _delta_c(df: pd.DataFrame, score_col: str, time_col: str = "os_time", event_col: str = "os_event") -> dict:
    """ΔC: AJCC + score vs AJCC alone, on df.

    df has columns: time, event, ajcc_stage_num, score (HCC-TRS).
    """
    d = df.dropna(subset=[time_col, event_col, "ajcc_stage_num", score_col])
    if len(d) < 20:
        return {"n": len(d), "c_baseline": None, "c_combined": None, "delta_c": None}
    cph_b = CoxPHFitter(penalizer=0.01).fit(d[[time_col, event_col, "ajcc_stage_num"]], time_col, event_col)
    risk_b = cph_b.predict_partial_hazard(d[["ajcc_stage_num"]]).values
    cph_c = CoxPHFitter(penalizer=0.01).fit(d[[time_col, event_col, "ajcc_stage_num", score_col]], time_col, event_col)
    risk_c = cph_c.predict_partial_hazard(d[["ajcc_stage_num", score_col]]).values
    c_b = float(concordance_index(d[time_col].values, -risk_b, d[event_col].values))
    c_c = float(concordance_index(d[time_col].values, -risk_c, d[event_col].values))
    return {"n": int(len(d)), "c_baseline": c_b, "c_combined": c_c, "delta_c": c_c - c_b}


def _bootstrap_delta_c(df: pd.DataFrame, score_col: str,
                        time_col: str = "os_time", event_col: str = "os_event",
                        n_boot: int = N_BOOTSTRAP, seed: int = SEED) -> dict:
    rng = np.random.default_rng(seed)
    point = _delta_c(df, score_col, time_col, event_col)
    deltas = []
    n = len(df)
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        sub = df.iloc[idx]
        try:
            res = _delta_c(sub, score_col, time_col, event_col)
            if res["delta_c"] is not None:
                deltas.append(res["delta_c"])
        except Exception:
            pass
    deltas = np.array(deltas)
    return {
        "point": point,
        "ci_lo": float(np.percentile(deltas, 2.5)),
        "ci_hi": float(np.percentile(deltas, 97.5)),
        "n_bootstrap_iters": int(len(deltas)),
        "reject_h0": bool(np.percentile(deltas, 2.5) > 0),
    }


# ----------------------------------------------------------------------
# Cohort drivers
# ----------------------------------------------------------------------

def _run_cohort(name: str, spec: dict) -> dict:
    """Download, parse, derive score for one cohort. Returns a dict with
    per-sample frame `df` (samples x [os_time, os_event, ajcc_stage_num, score])
    and metadata."""
    print(f"\n=== {name} ===")
    matrix_path = RAW / Path(spec["matrix_url"]).name
    gpl_path = RAW / Path(spec["gpl_url"]).name
    _download(spec["matrix_url"], matrix_path)
    _download(spec["gpl_url"], gpl_path)
    supp_path: Path | None = None
    if spec.get("supplement_url"):
        supp_path = RAW / Path(spec["supplement_url"]).name
        _download(spec["supplement_url"], supp_path)
    print("parsing matrix")
    expr, meta = _parse_series_matrix(matrix_path)
    print(f"  expression: {expr.shape[0]} probes x {expr.shape[1]} samples")
    print("parsing GPL annot")
    probe_to_gene = _parse_gpl_annot(gpl_path)
    print(f"  probe->gene map: {len(probe_to_gene)} entries")
    # Map probes to genes
    expr_g = expr.copy()
    expr_g["gene"] = [probe_to_gene.get(p, None) for p in expr_g.index]
    expr_g = expr_g[expr_g["gene"].notna()]
    expr_g = expr_g.groupby("gene").max(numeric_only=True)
    print(f"  after probe->gene collapse: {expr_g.shape[0]} genes x {expr_g.shape[1]} samples")
    # Apply scale guard (microarray data should be log-scaled already; if max > 50, log2)
    arr = expr_g.values
    if np.nanmax(arr) > 50:
        print(f"  max={np.nanmax(arr):.1f}; applying log2(x+1)")
        expr_g = np.log2(expr_g.clip(lower=0) + 1)
    coefs = _load_layer1_coefs()
    # Need samples x genes for scoring
    score, cov_info = _apply_risk_score(expr_g.T, coefs)
    print(f"  HCC-TRS coverage: {cov_info['coverage']*100:.1f}% ({cov_info['n_present']}/{cov_info['n_signature_genes']})")
    # Clinical extraction (cohort-specific)
    if name == "GSE14520":
        clin = _extract_clinical_GSE14520(meta, supp_path)
    elif name == "GSE76427":
        clin = _extract_clinical_GSE76427(meta)
    else:
        clin = pd.DataFrame(index=meta.index)
    # Save raw clinical for inspection
    (PROC / f"layer3_{name}_clinical_raw.tsv").write_text(clin.to_csv(sep="\t"))
    print(f"  clinical columns: {list(clin.columns)[:14]}...")
    # Assemble per-sample frame; filter to tumour samples
    df = pd.DataFrame(index=score.index)
    df["score"] = score
    df = df.join(clin, how="inner")
    if "tumour" in df.columns:
        n_pre = len(df)
        df = df[df["tumour"].fillna(False)]
        print(f"  filtered to tumour samples: {n_pre} -> {len(df)}")
    return {"df": df, "clin_columns": list(clin.columns), "coverage": cov_info}


def _harmonise_clinical(name: str, df: pd.DataFrame) -> pd.DataFrame:
    """Per-cohort harmonisation to (os_time months, os_event, ajcc_stage_num).

    AJCC is encoded as the TNM-derived stage (I=1, II=2, III=3, IV=4), the
    same scale Roessler 2010 reports. Per docs/prereg.md the baseline is
    AJCC pathologic stage; both cohorts deposit TNM staging which underpins
    AJCC, and we use that.
    """
    df = df.copy()
    if name == "GSE14520":
        # Supplement columns: "Survival months", "Survival status",
        # "TNM staging", "BCLC staging"
        t_col = next((c for c in df.columns if c.strip().lower() == "survival months"), None)
        e_col = next((c for c in df.columns if c.strip().lower() == "survival status"), None)
        s_col = next((c for c in df.columns if c.strip().lower() == "tnm staging"), None)
    elif name == "GSE76427":
        # Series-matrix characteristics: event_os 0/1, duryears_os in years,
        # tnm_staging_clinical / bclc_staging
        t_col = next((c for c in df.columns if "duryears_os" in c.lower()), None)
        e_col = next((c for c in df.columns if c.lower() == "event_os"), None)
        s_col = next((c for c in df.columns if "tnm_staging" in c.lower()), None)
    else:
        t_col = e_col = s_col = None

    if t_col:
        t = pd.to_numeric(df[t_col], errors="coerce")
        # GSE76427 reports duryears; convert to months for pooled analysis
        if name == "GSE76427":
            t = t * 12.0
        df["os_time"] = t
    else:
        df["os_time"] = np.nan
    if e_col:
        evt_str = df[e_col].astype(str).str.lower()
        df["os_event"] = evt_str.map(lambda s: 1 if any(k in s for k in ("dead", "death", "deceased", "1")) else 0)
    else:
        df["os_event"] = np.nan
    if s_col:
        stage_str = df[s_col].astype(str).str.upper().str.strip()
        def _stage_num(s: str) -> float:
            # Order matters: check IV before I.
            for k, v in [("IV", 4), ("III", 3), ("II", 2), ("I", 1)]:
                if s.startswith(k) or s == k:
                    return v
            return np.nan
        df["ajcc_stage_num"] = stage_str.map(_stage_num)
    else:
        df["ajcc_stage_num"] = np.nan
    df["cohort"] = name
    return df


def main() -> None:
    print(f"Layer 3 external validation; seed={SEED}, n_bootstrap={N_BOOTSTRAP}")
    print(f"Threshold delta_c >= {DELTA_C_THRESHOLD} (preregistered)")

    cohort_dfs = []
    cohort_meta = {}
    coverage_info = {}
    for name, spec in COHORTS.items():
        try:
            result = _run_cohort(name, spec)
            df = result["df"]
            df = _harmonise_clinical(name, df)
            df_clean = df.dropna(subset=["os_time", "os_event", "ajcc_stage_num", "score"])
            print(f"  {name} after harmonise: {len(df_clean)} samples with complete data")
            df_out = df_clean[["score", "os_time", "os_event", "ajcc_stage_num", "cohort"]].copy()
            df_out.to_csv(PROC / f"layer3_{name}.tsv", sep="\t")
            cohort_dfs.append(df_out)
            cohort_meta[name] = {"n_with_complete_data": int(len(df_clean)), "clin_columns": result["clin_columns"]}
            coverage_info[name] = result["coverage"]
        except Exception as exc:
            print(f"  ERROR processing {name}: {exc}")
            cohort_meta[name] = {"error": str(exc)}
            coverage_info[name] = {"error": str(exc)}

    if not cohort_dfs:
        print("FATAL: no cohorts produced usable data")
        sys.exit(2)

    pooled = pd.concat(cohort_dfs, ignore_index=False)
    print(f"\nPooled n = {len(pooled)}")
    print(f"Events: {int(pooled['os_event'].sum())}")
    pooled.to_csv(PROC / "layer3_pooled.tsv", sep="\t")

    # Primary outcome
    print("\n=== Primary outcome (preregistered) ===")
    primary = _bootstrap_delta_c(pooled, "score")
    print(f"point delta_c = {primary['point']['delta_c']:.4f}")
    print(f"95% CI = [{primary['ci_lo']:.4f}, {primary['ci_hi']:.4f}]")
    print(f"reject H0 (CI > 0): {primary['reject_h0']}")
    primary_decision = "positive" if primary['reject_h0'] else "null"

    # Cohort-specific secondaries
    print("\n=== Cohort-specific delta_c ===")
    secondaries = {}
    for df_c in cohort_dfs:
        cname = df_c["cohort"].iloc[0]
        sec = _bootstrap_delta_c(df_c, "score")
        secondaries[f"S_{cname}_delta_c"] = sec
        print(f"  {cname}: delta_c = {sec['point']['delta_c']} CI=[{sec['ci_lo']:.4f}, {sec['ci_hi']:.4f}] n={sec['point']['n']}")

    # Output JSON
    payload = {
        "preregistration_anchor_commit": "88d6d15",
        "preregistration_path": "docs/prereg.md",
        "seed": SEED,
        "n_bootstrap": N_BOOTSTRAP,
        "delta_c_threshold": DELTA_C_THRESHOLD,
        "alpha": ALPHA,
        "cohorts": cohort_meta,
        "coverage": coverage_info,
        "pooled_n": int(len(pooled)),
        "pooled_events": int(pooled["os_event"].sum()),
        "primary_outcome": primary,
        "primary_decision": primary_decision,
        "secondaries": secondaries,
        "layer1_risk_score_source": "case-study/data/results/tcga_model_coefs.tsv",
        "layer1_release_tag": "case-study-v1.0.0",
        "completed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    out_path = RES / "layer3_validation.json"
    out_path.write_text(json.dumps(payload, indent=2))
    print(f"\nwrote {out_path}")
    print(f"DECISION: {primary_decision}")


if __name__ == "__main__":
    main()
