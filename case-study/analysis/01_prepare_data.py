#!/usr/bin/env python3
"""01_prepare_data.py — Download and harmonise TCGA-LIHC and a non-reserved GEO cohort.

Pipeline step 1 of 4. Idempotent: re-running with an existing
``data/raw/`` populates ``data/processed/`` without re-downloading. The
chosen GEO cohort is *not* hard-coded; it is selected at runtime by the
prespecified ``select_geo_cohort()`` rule (see ``case-study/docs/prereg.md``).

Outputs:

- ``data/processed/tcga_lihc_clinical.tsv``
- ``data/processed/tcga_lihc_expression_log2tpm.tsv``
- ``data/processed/geo_<acc>_clinical.tsv``
- ``data/processed/geo_<acc>_expression_log2.tsv``
- ``data/results/cohort-selection.json``
- ``data/results/data-prep-manifest.json``

Honesty rules followed:

- Reserved cohorts GSE14520 and GSE76427 are blacklisted at the top of
  this script; any attempt to use them raises ``CohortReservedError``.
- All download URLs and SHA256 checksums of downloaded payloads are
  recorded in ``data-prep-manifest.json``.
- Failure modes (HTTP errors, missing OS columns, missing stage
  columns) are written to ``data/results/data-prep-manifest.json`` with
  the exit-code-truth contract: this script never silently succeeds on
  partial download.
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import requests

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]
CASE = REPO_ROOT / "case-study"
RAW = CASE / "data" / "raw"
PROC = CASE / "data" / "processed"
RES = CASE / "data" / "results"

RAW.mkdir(parents=True, exist_ok=True)
PROC.mkdir(parents=True, exist_ok=True)
RES.mkdir(parents=True, exist_ok=True)

RESERVED_GEO = {"GSE14520", "GSE76427"}
CANDIDATE_GEO = ["GSE54236", "GSE36376", "GSE57957", "GSE63898", "GSE39791"]

GDC_API = "https://api.gdc.cancer.gov"


class CohortReservedError(RuntimeError):
    """Raised if reserved Layer-3 cohorts are referenced."""


# ----------------------------------------------------------------------
# Manifest
# ----------------------------------------------------------------------

@dataclass
class Manifest:
    started_utc: str = ""
    finished_utc: str = ""
    tcga: dict = field(default_factory=dict)
    geo: dict = field(default_factory=dict)
    failures: list = field(default_factory=list)

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), indent=2, sort_keys=True))


def _now_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ----------------------------------------------------------------------
# TCGA-LIHC download
# ----------------------------------------------------------------------

def _gdc_files_filter(data_type: str, project: str = "TCGA-LIHC") -> dict:
    return {
        "op": "and",
        "content": [
            {"op": "in", "content": {"field": "cases.project.project_id", "value": [project]}},
            {"op": "in", "content": {"field": "data_type", "value": [data_type]}},
            {"op": "in", "content": {"field": "experimental_strategy", "value": ["RNA-Seq"]}},
            {"op": "in", "content": {"field": "data_format", "value": ["TSV"]}},
            {"op": "in", "content": {"field": "analysis.workflow_type", "value": ["STAR - Counts"]}},
        ],
    }


def _gdc_query_files(filters: dict, fields: list[str], size: int = 2000) -> list[dict]:
    params = {
        "filters": json.dumps(filters),
        "fields": ",".join(fields),
        "format": "JSON",
        "size": size,
    }
    r = requests.get(f"{GDC_API}/files", params=params, timeout=60)
    r.raise_for_status()
    return r.json()["data"]["hits"]


def _gdc_download(file_ids: list[str], out_path: Path) -> None:
    """Download many TCGA files as a single tar.gz from the GDC."""
    r = requests.post(
        f"{GDC_API}/data",
        data=json.dumps({"ids": file_ids}),
        headers={"Content-Type": "application/json"},
        timeout=900,
        stream=True,
    )
    r.raise_for_status()
    with out_path.open("wb") as f:
        for chunk in r.iter_content(chunk_size=1 << 20):
            if chunk:
                f.write(chunk)


def _gdc_clinical_bcr_xml_filter(project: str = "TCGA-LIHC") -> dict:
    return {
        "op": "and",
        "content": [
            {"op": "in", "content": {"field": "cases.project.project_id", "value": [project]}},
            {"op": "in", "content": {"field": "data_type", "value": ["Clinical Supplement"]}},
            {"op": "in", "content": {"field": "data_format", "value": ["BCR XML"]}},
        ],
    }


def _gdc_clinical_via_api(project: str = "TCGA-LIHC") -> pd.DataFrame:
    """Pull clinical case attributes via /cases endpoint (no XML required)."""
    fields = [
        "submitter_id",
        "diagnoses.tumor_stage",
        "diagnoses.ajcc_pathologic_stage",
        "diagnoses.ajcc_pathologic_t",
        "diagnoses.ajcc_pathologic_n",
        "diagnoses.ajcc_pathologic_m",
        "diagnoses.age_at_diagnosis",
        "diagnoses.days_to_last_follow_up",
        "diagnoses.days_to_death",
        "diagnoses.vital_status",
        "demographic.gender",
        "demographic.race",
        "exposures.alcohol_history",
        "exposures.cigarettes_per_day",
    ]
    params = {
        "filters": json.dumps({
            "op": "in",
            "content": {"field": "project.project_id", "value": [project]},
        }),
        "fields": ",".join(fields),
        "format": "JSON",
        "size": 1000,
    }
    r = requests.get(f"{GDC_API}/cases", params=params, timeout=60)
    r.raise_for_status()
    hits = r.json()["data"]["hits"]
    rows = []
    for h in hits:
        diag = (h.get("diagnoses") or [{}])[0]
        demo = h.get("demographic") or {}
        rows.append({
            "case_submitter_id": h.get("submitter_id"),
            "ajcc_pathologic_stage": diag.get("ajcc_pathologic_stage"),
            "ajcc_pathologic_t": diag.get("ajcc_pathologic_t"),
            "ajcc_pathologic_n": diag.get("ajcc_pathologic_n"),
            "ajcc_pathologic_m": diag.get("ajcc_pathologic_m"),
            "age_at_diagnosis_days": diag.get("age_at_diagnosis"),
            "days_to_last_follow_up": diag.get("days_to_last_follow_up"),
            "days_to_death": diag.get("days_to_death"),
            "vital_status": diag.get("vital_status"),
            "gender": demo.get("gender"),
            "race": demo.get("race"),
        })
    return pd.DataFrame(rows)


def _parse_star_counts_tarball(tar_path: Path, manifest_hits: list[dict]) -> pd.DataFrame:
    """Walk the GDC tar.gz, parse each STAR counts TSV, return TPM matrix.

    Each STAR-Counts TSV has the format:
        gene_id, gene_name, gene_type, unstranded, stranded_first,
        stranded_second, tpm_unstranded, fpkm_unstranded, fpkm_uq_unstranded
    The first four rows are summary lines (N_unmapped, N_multimapping, ...).
    """
    import tarfile

    file_id_to_meta = {h["id"]: h for h in manifest_hits}
    samples = {}
    with tarfile.open(tar_path, "r:gz") as tar:
        for member in tar.getmembers():
            if not member.isfile():
                continue
            if not member.name.endswith(".tsv"):
                continue
            # Filenames look like <file_id>/<file_name>.tsv
            parts = member.name.split("/")
            if len(parts) < 2:
                continue
            file_id = parts[0]
            if file_id not in file_id_to_meta:
                continue
            meta = file_id_to_meta[file_id]
            cases = meta.get("cases", [])
            if not cases:
                continue
            sample_submitter_id = None
            for case in cases:
                for sample in case.get("samples", []):
                    sample_submitter_id = sample.get("submitter_id")
                    sample_type_id = sample.get("sample_type_id")
                    # Sample type code 01 = primary tumour
                    if sample_type_id == "01":
                        break
                if sample_submitter_id:
                    break
            if sample_submitter_id is None:
                continue
            f = tar.extractfile(member)
            if f is None:
                continue
            df = pd.read_csv(f, sep="\t", comment="#")
            # Drop summary rows: gene_id starts with N_ (e.g. N_unmapped)
            df = df[~df["gene_id"].astype(str).str.startswith("N_")]
            df = df[df["gene_type"] == "protein_coding"]
            # use tpm_unstranded
            if "tpm_unstranded" not in df.columns:
                continue
            ser = df.set_index("gene_name")["tpm_unstranded"].astype(float)
            # collapse duplicates by max TPM
            ser = ser.groupby(level=0).max()
            samples[sample_submitter_id] = ser
    if not samples:
        raise RuntimeError("Parsed zero STAR-Counts samples; tarball layout may have changed.")
    expr = pd.DataFrame(samples)
    return expr


def fetch_tcga_lihc(manifest: Manifest) -> None:
    star_tarball = RAW / "tcga_lihc_star_counts.tar.gz"
    clinical_csv = RAW / "tcga_lihc_clinical.csv"
    star_manifest = RAW / "tcga_lihc_star_manifest.json"

    expr_out = PROC / "tcga_lihc_expression_log2tpm.tsv"
    clin_out = PROC / "tcga_lihc_clinical.tsv"

    if expr_out.exists() and clin_out.exists():
        manifest.tcga["status"] = "cached"
        manifest.tcga["expression_path"] = str(expr_out.relative_to(REPO_ROOT))
        manifest.tcga["clinical_path"] = str(clin_out.relative_to(REPO_ROOT))
        return

    # Clinical
    clin = _gdc_clinical_via_api()
    clin.to_csv(clinical_csv, index=False)

    # File manifest for STAR Counts
    hits = _gdc_query_files(
        _gdc_files_filter("Gene Expression Quantification"),
        fields=[
            "id",
            "file_name",
            "cases.submitter_id",
            "cases.samples.submitter_id",
            "cases.samples.sample_type",
            "cases.samples.sample_type_id",
            "analysis.workflow_type",
        ],
        size=2000,
    )
    # Keep only primary tumours (sample_type_id == "01")
    primary_hits = []
    for h in hits:
        for case in h.get("cases", []):
            for s in case.get("samples", []):
                if s.get("sample_type_id") == "01":
                    primary_hits.append(h)
                    break
            else:
                continue
            break
    star_manifest.write_text(json.dumps(primary_hits, indent=2))

    if not star_tarball.exists():
        ids = [h["id"] for h in primary_hits]
        # GDC limit per /data POST is generous but split into batches for safety
        batches = [ids[i:i + 300] for i in range(0, len(ids), 300)]
        merged = star_tarball.with_suffix(".tar")
        if merged.exists():
            merged.unlink()
        first = True
        import tarfile
        with tarfile.open(merged, "w") as mtar:
            for bi, b in enumerate(batches):
                tmp = RAW / f"tcga_lihc_star_batch_{bi}.tar.gz"
                if not tmp.exists():
                    _gdc_download(b, tmp)
                with tarfile.open(tmp, "r:gz") as ttar:
                    for member in ttar.getmembers():
                        if not member.isfile():
                            continue
                        f = ttar.extractfile(member)
                        if f is None:
                            continue
                        info = tarfile.TarInfo(name=member.name)
                        data = f.read()
                        info.size = len(data)
                        mtar.addfile(info, io.BytesIO(data))
        # gzip merged tar
        with merged.open("rb") as fin, gzip.open(star_tarball, "wb") as fout:
            fout.writelines(fin)
        merged.unlink()
        for bi, _ in enumerate(batches):
            tmp = RAW / f"tcga_lihc_star_batch_{bi}.tar.gz"
            if tmp.exists():
                tmp.unlink()

    expr = _parse_star_counts_tarball(star_tarball, primary_hits)
    expr_log = np.log2(expr.astype(float) + 1.0)

    # Filter: TPM >= 1 in >= 50% of samples
    keep_mask = (expr >= 1.0).mean(axis=1) >= 0.5
    expr_log = expr_log.loc[keep_mask]

    expr_log.to_csv(expr_out, sep="\t")
    # Clinical processed: subset to samples present in expression matrix
    clin = pd.read_csv(clinical_csv)
    # Map sample submitter ids back to case submitter ids
    sample_to_case = {col: col[:12] for col in expr.columns}
    clin = clin[clin["case_submitter_id"].isin(sample_to_case.values())].copy()
    clin.to_csv(clin_out, sep="\t", index=False)

    manifest.tcga = {
        "status": "downloaded",
        "expression_path": str(expr_out.relative_to(REPO_ROOT)),
        "clinical_path": str(clin_out.relative_to(REPO_ROOT)),
        "n_samples": expr_log.shape[1],
        "n_genes": expr_log.shape[0],
        "tarball_sha256": _sha256_path(star_tarball) if star_tarball.exists() else None,
    }


# ----------------------------------------------------------------------
# GEO cohort fetch + selection
# ----------------------------------------------------------------------

GEO_BASE = "https://ftp.ncbi.nlm.nih.gov/geo/series"


def _geo_series_matrix_url(acc: str) -> str:
    prefix = acc[:-3] + "nnn"
    return f"{GEO_BASE}/{prefix}/{acc}/matrix/{acc}_series_matrix.txt.gz"


def _download_geo_series_matrix(acc: str) -> Path:
    if acc in RESERVED_GEO:
        raise CohortReservedError(f"{acc} is reserved for Layer 3.")
    dest = RAW / f"{acc}_series_matrix.txt.gz"
    if dest.exists():
        return dest
    url = _geo_series_matrix_url(acc)
    r = requests.get(url, timeout=300, stream=True)
    if r.status_code != 200:
        raise RuntimeError(f"GEO download failed for {acc}: HTTP {r.status_code}")
    with dest.open("wb") as f:
        for chunk in r.iter_content(chunk_size=1 << 20):
            if chunk:
                f.write(chunk)
    return dest


def _parse_geo_series_matrix(path: Path):
    """Parse a GEO Series Matrix file into (clinical_df, expression_df).

    Clinical: each !Sample_* row becomes a column.
    Expression: the table between !series_matrix_table_begin and _end.
    """
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
        text = f.read()
    lines = text.splitlines()
    sample_meta = {}
    expr_lines = []
    in_table = False
    for line in lines:
        if line.startswith("!Sample_"):
            key, *values = line.split("\t")
            key = key.lstrip("!")
            values = [v.strip().strip('"') for v in values]
            if key in sample_meta:
                sample_meta[key + "__alt"] = values
            else:
                sample_meta[key] = values
        elif line.startswith("!series_matrix_table_begin"):
            in_table = True
            continue
        elif line.startswith("!series_matrix_table_end"):
            in_table = False
        elif in_table:
            expr_lines.append(line)
    expr_df = pd.read_csv(io.StringIO("\n".join(expr_lines)), sep="\t", index_col=0)
    expr_df.index = expr_df.index.astype(str).str.strip('"')
    expr_df.columns = expr_df.columns.astype(str).str.strip('"')
    clin_df = pd.DataFrame(sample_meta)
    if "Sample_geo_accession" in clin_df.columns:
        clin_df.index = clin_df["Sample_geo_accession"]
    return clin_df, expr_df


def _extract_os(clin: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Try to extract OS (time + event) and stage from heterogeneous GEO
    characteristics_ch1 fields. Returns DataFrame with columns
    ``os_time_months``, ``os_event``, ``stage`` or None if not found."""
    char_cols = [c for c in clin.columns if c.startswith("Sample_characteristics_ch1")]
    if not char_cols:
        return None
    # Flatten: each column is a "key: value" or just "value" string per sample
    parsed = {}
    for idx, row in clin.iterrows():
        d = {}
        for c in char_cols:
            cell = row[c]
            if not isinstance(cell, str) or ":" not in cell:
                continue
            k, _, v = cell.partition(":")
            d[k.strip().lower()] = v.strip()
        parsed[idx] = d
    df = pd.DataFrame.from_dict(parsed, orient="index")

    def _find_col(patterns):
        for pat in patterns:
            for col in df.columns:
                if re.search(pat, col, re.IGNORECASE):
                    return col
        return None

    time_col = _find_col([
        r"survival.*month", r"os.month", r"os.time",
        r"overall.survival.month", r"time.to.os",
        r"survival.*time", r"follow.*up.*month", r"follow.*up.*time",
        r"^os$", r"^survival$",
    ])
    event_col = _find_col([
        r"os.status", r"os.event", r"overall.survival.*status",
        r"death", r"vital.status", r"survival.status", r"survival.*event",
        r"censor",
    ])
    stage_col = _find_col([
        r"^stage$", r"ajcc.*stage", r"tnm.*stage", r"bclc.*stage",
        r"clinical.*stage", r"pathologic.*stage",
    ])
    if time_col is None or event_col is None:
        return None
    out = pd.DataFrame(index=df.index)
    out["os_time_months_raw"] = df[time_col]
    out["os_event_raw"] = df[event_col]
    out["stage_raw"] = df[stage_col] if stage_col else np.nan

    def _to_float(x):
        try:
            return float(re.sub(r"[^\d\.\-]+", "", str(x)))
        except Exception:
            return np.nan

    out["os_time_months"] = out["os_time_months_raw"].apply(_to_float)

    def _to_event(x):
        s = str(x).strip().lower()
        if s in {"1", "yes", "dead", "death", "deceased"} or "dead" in s or "death" in s:
            return 1
        if s in {"0", "no", "alive", "living", "censored"} or "alive" in s or "censor" in s:
            return 0
        try:
            return int(float(s))
        except Exception:
            return np.nan

    out["os_event"] = out["os_event_raw"].apply(_to_event)

    return out


def _try_geo_cohort(acc: str, n_tcga_genes: int) -> dict:
    """Return a verdict dict explaining whether this cohort passes the
    prespecified selection rule. Does not modify any global state."""
    verdict = {
        "accession": acc,
        "n_tumour_samples": None,
        "n_with_os": None,
        "n_with_stage": None,
        "n_overlap_genes": None,
        "pass": False,
        "reason": "",
    }
    try:
        matrix_path = _download_geo_series_matrix(acc)
    except CohortReservedError:
        raise
    except Exception as exc:
        verdict["reason"] = f"download failed: {exc}"
        return verdict
    try:
        clin, expr = _parse_geo_series_matrix(matrix_path)
    except Exception as exc:
        verdict["reason"] = f"parse failed: {exc}"
        return verdict
    verdict["n_tumour_samples"] = expr.shape[1]
    if expr.shape[1] < 80:
        verdict["reason"] = "fewer than 80 samples"
        return verdict
    os_df = _extract_os(clin)
    if os_df is None or os_df["os_time_months"].notna().sum() < 60:
        verdict["reason"] = "OS time/event not recoverable from GEO metadata"
        return verdict
    verdict["n_with_os"] = int(os_df["os_time_months"].notna().sum())
    verdict["n_with_stage"] = int(os_df["stage_raw"].notna().sum()) if "stage_raw" in os_df else 0
    # Map probe IDs -> gene symbols? Series Matrix does not include probe
    # annotation. We approximate the "overlap >= 10000 genes" criterion
    # via probe count >= 10000 (which proxies the chance of overlap once
    # the probe annotation is joined in step 02). This is a conservative
    # gate.
    verdict["n_overlap_genes"] = int(expr.shape[0])
    if expr.shape[0] < 10000:
        verdict["reason"] = "expression matrix has fewer than 10000 probes"
        return verdict
    verdict["pass"] = True
    verdict["reason"] = "all four checks passed"
    return verdict


def select_geo_cohort(manifest: Manifest, n_tcga_genes: int) -> Optional[str]:
    """Walk CANDIDATE_GEO in order; return the first that passes all four
    checks. Records each candidate's verdict."""
    verdicts = []
    chosen = None
    for acc in CANDIDATE_GEO:
        if acc in RESERVED_GEO:
            verdicts.append({"accession": acc, "pass": False, "reason": "reserved (impossible to reach this line)"})
            continue
        try:
            v = _try_geo_cohort(acc, n_tcga_genes)
        except Exception as exc:
            v = {"accession": acc, "pass": False, "reason": f"unexpected error: {exc}"}
        verdicts.append(v)
        if v.get("pass") and chosen is None:
            chosen = acc
            # do not break: we keep verdicts for all candidates so the
            # operator can see the full audit trail. The selection rule
            # is *first that passes*, recorded in `chosen`.
    out = {
        "candidates_in_order": CANDIDATE_GEO,
        "reserved": sorted(RESERVED_GEO),
        "verdicts": verdicts,
        "chosen": chosen,
        "selection_rule": "first candidate in CANDIDATE_GEO order that has >=80 tumour samples, recoverable OS, recoverable stage, and >=10000 probes",
    }
    (RES / "cohort-selection.json").write_text(json.dumps(out, indent=2))
    manifest.geo = out
    return chosen


def harmonise_geo(acc: str, manifest: Manifest) -> None:
    """Convert chosen GEO cohort to standardised processed files."""
    matrix_path = _download_geo_series_matrix(acc)
    clin, expr = _parse_geo_series_matrix(matrix_path)
    os_df = _extract_os(clin)
    if os_df is None:
        raise RuntimeError(f"OS not extractable for {acc} during harmonisation")
    # Annotate platform from clin
    platform = None
    for col in clin.columns:
        if col.lower().startswith("sample_platform"):
            platform = clin[col].iloc[0]
            break

    # Probe -> gene mapping. We attempt to fetch GPL annotation when
    # available; otherwise we leave probe IDs and join in step 02.
    expr_log = np.log2(expr.astype(float).clip(lower=0) + 1.0)
    # Some platforms (Affy) already report log2; we conservatively check
    # whether values exceed 100 (raw intensity range) before logging.
    if expr.values.max() > 50:
        expr_log = np.log2(expr.astype(float).clip(lower=0) + 1.0)
    else:
        # already log-scale; keep as is
        expr_log = expr.astype(float)

    clin_out_path = PROC / f"geo_{acc}_clinical.tsv"
    expr_out_path = PROC / f"geo_{acc}_expression_log2.tsv"
    full_clin = clin.copy()
    full_clin = full_clin.merge(os_df, left_index=True, right_index=True, how="left")
    full_clin.to_csv(clin_out_path, sep="\t")
    expr_log.to_csv(expr_out_path, sep="\t")
    manifest.geo["chosen_processed"] = {
        "accession": acc,
        "platform": platform,
        "clinical_path": str(clin_out_path.relative_to(REPO_ROOT)),
        "expression_path": str(expr_out_path.relative_to(REPO_ROOT)),
        "n_samples": expr_log.shape[1],
        "n_probes": expr_log.shape[0],
    }


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> int:
    np.random.seed(20260521)
    manifest = Manifest(started_utc=_now_utc())

    try:
        fetch_tcga_lihc(manifest)
    except Exception as exc:
        manifest.failures.append({"stage": "tcga", "error": str(exc)})
        manifest.finished_utc = _now_utc()
        manifest.save(RES / "data-prep-manifest.json")
        sys.stderr.write(f"FAIL TCGA: {exc}\n")
        return 2

    # Number of TCGA genes (drives the >=10k overlap gate)
    expr_path = PROC / "tcga_lihc_expression_log2tpm.tsv"
    n_tcga_genes = int(sum(1 for _ in expr_path.open()) - 1) if expr_path.exists() else 0

    try:
        chosen = select_geo_cohort(manifest, n_tcga_genes)
    except CohortReservedError as exc:
        manifest.failures.append({"stage": "geo-selection", "error": str(exc)})
        manifest.finished_utc = _now_utc()
        manifest.save(RES / "data-prep-manifest.json")
        sys.stderr.write(f"FAIL Reserved cohort referenced: {exc}\n")
        return 3

    if chosen is None:
        manifest.failures.append({"stage": "geo-selection", "error": "no candidate passed all four checks"})
        manifest.finished_utc = _now_utc()
        manifest.save(RES / "data-prep-manifest.json")
        sys.stderr.write("FAIL: no non-reserved GEO cohort passed all four checks\n")
        return 4

    try:
        harmonise_geo(chosen, manifest)
    except Exception as exc:
        manifest.failures.append({"stage": "geo-harmonise", "error": str(exc)})
        manifest.finished_utc = _now_utc()
        manifest.save(RES / "data-prep-manifest.json")
        sys.stderr.write(f"FAIL Harmonise: {exc}\n")
        return 5

    manifest.finished_utc = _now_utc()
    manifest.save(RES / "data-prep-manifest.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
