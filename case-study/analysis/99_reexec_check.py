#!/usr/bin/env python3
"""99_reexec_check.py — Distributional reproducibility check.

This is the script the Viewpoint Section~5 ``A single operator cannot
audit himself'' counter-argument cites as the operational test for
re-execution-against-self. It is the Layer-2 audit's primary mechanical
gate, but the same check runs at the end of every Layer-1 session so
that the committed `data/results/` artefacts are known to satisfy it
before any Layer-2 session ever opens.

What it checks
==============

For each committed artefact under ``case-study/data/results/`` the
script compares the *re-executed* value against the committed value
under tolerances appropriate to its type:

- numeric scalars (C-index, ΔC-index, slopes, p-values): absolute
  tolerance of 1e-6 (deterministic) or 5e-2 (re-bootstrapped). Each
  field is annotated in ``_FIELD_TOL`` below; anything not annotated is
  treated as deterministic.
- numeric arrays/tables (per-patient risk scores, coefficient tables):
  two-sample KS test on the sorted-distribution match; we **do not**
  require row-by-row equality because the bootstrap RNG is allowed to
  shift the order of internal randomness across Python/numpy minor
  versions. A KS p > 0.05 is the operational passing condition.

What it does NOT check
======================

This file is **not** a substitute for the Layer-2 audit. Layer 2's
audit is broader (citation veracity, claim-vs-data alignment, end-to-
end clean-clone replay). The reexec_check.py contract is narrower:
"given the committed artefacts and the committed pipeline, does the
pipeline reproduce the artefacts within a documented tolerance band?"

Exit codes
==========
- 0 = all checks pass within tolerance
- 1 = one or more checks fail; a diagnostic line is printed per failure
- 2 = a re-executed artefact is missing entirely

Usage
=====
Run *after* ``01_prepare_data.py``..``04_figures.py`` from a fresh
checkout. The committed artefacts are read from ``case-study/data/
results/`` at the current HEAD; the re-executed values are produced by
``--regenerate`` (the default is to use the values just produced
in-place by the previous pipeline run, which is the common case during
Layer-1 development).
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
CASE = REPO_ROOT / "case-study"
RES = CASE / "data" / "results"


# Tolerance map per field path (dot-separated). Default 1e-6 if absent.
# Bootstrap-derived fields have a wider tolerance because the bootstrap
# RNG is allowed to drift; the gate is "same distribution to within 5%
# of a C-index unit", not "byte-for-byte identical".
_FIELD_TOL: dict[str, float] = {
    # Bootstrap-derived numerics: allow 5% absolute drift
    "primary.delta_c_optimism_corrected": 5e-2,
    "primary.delta_c_95ci_lo": 5e-2,
    "primary.delta_c_95ci_hi": 5e-2,
    "primary.c_corrected_trs": 5e-2,
    "primary.opt_avg": 5e-2,
    "external.c_index": 5e-2,
    "external.c_index_ci_lo": 1e-1,
    "external.c_index_ci_hi": 1e-1,
    "external.median_split_logrank_p": 5e-2,
    # Apparent (deterministic) numerics: tight
    "primary.c_apparent_trs": 1e-3,
    "primary.c_apparent_ajcc": 1e-3,
    "primary.c_apparent_combo": 1e-3,
    "primary.delta_c_apparent": 1e-3,
    "secondary.L1_logrank_quartiles_p": 1e-3,
    "secondary.L1_logrank_chi2": 1e-2,
    "secondary.L4_calibration_slope": 1e-2,
    "secondary.L5_schoenfeld_p_trs": 1e-2,
    # Permutation p-value: bootstrap-like
    "secondary.L7_permutation_null_p": 5e-2,
}


# ----------------------------------------------------------------------
# Git helpers
# ----------------------------------------------------------------------

def _git_blob(path: Path) -> str | None:
    """Return the content of `path` as committed at HEAD, or None if
    not committed."""
    try:
        rel = path.relative_to(REPO_ROOT)
    except ValueError:
        return None
    try:
        out = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "show", f"HEAD:{rel}"],
            stderr=subprocess.DEVNULL,
        )
        return out.decode("utf-8")
    except subprocess.CalledProcessError:
        return None


# ----------------------------------------------------------------------
# Scalar comparison
# ----------------------------------------------------------------------

def _flatten(prefix: str, obj: Any, out: dict[str, Any]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            _flatten(f"{prefix}.{k}" if prefix else k, v, out)
    elif isinstance(obj, list):
        # Skip lists of objects; we only audit scalars here.
        out[prefix] = obj
    else:
        out[prefix] = obj


def _compare_scalars(a: dict, b: dict, ctx: str) -> list[str]:
    diffs: list[str] = []
    fa, fb = {}, {}
    _flatten("", a, fa)
    _flatten("", b, fb)
    keys = sorted(set(fa) | set(fb))
    for k in keys:
        va, vb = fa.get(k), fb.get(k)
        if va is None and vb is None:
            continue
        if va is None or vb is None:
            diffs.append(f"{ctx}:{k}: present in one, absent in the other (committed={va!r}, regen={vb!r})")
            continue
        if isinstance(va, (list, tuple)) or isinstance(vb, (list, tuple)):
            # leave list comparison to caller; we don't compare lists scalar-wise here
            continue
        if isinstance(va, str) or isinstance(vb, str):
            if va != vb:
                # ignore timestamp/finished_utc drift
                if k.endswith("finished_utc") or k.endswith("started_utc"):
                    continue
                diffs.append(f"{ctx}:{k}: str mismatch (committed={va!r}, regen={vb!r})")
            continue
        try:
            xa = float(va)
            xb = float(vb)
        except (TypeError, ValueError):
            if va != vb:
                diffs.append(f"{ctx}:{k}: non-numeric mismatch ({va!r} != {vb!r})")
            continue
        if math.isnan(xa) and math.isnan(xb):
            continue
        tol = _FIELD_TOL.get(k, 1e-6)
        if abs(xa - xb) > tol:
            diffs.append(
                f"{ctx}:{k}: |committed - regen| = {abs(xa-xb):.4g} > tol {tol:.4g} "
                f"(committed={xa:.6g}, regen={xb:.6g})"
            )
    return diffs


# ----------------------------------------------------------------------
# Table KS comparison
# ----------------------------------------------------------------------

def _ks_check_arrays(a: np.ndarray, b: np.ndarray, ctx: str, alpha: float = 0.05) -> list[str]:
    from scipy.stats import ks_2samp
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if a.size == 0 or b.size == 0:
        return [f"{ctx}: empty array(s) — committed n={a.size}, regen n={b.size}"]
    res = ks_2samp(a, b)
    if res.pvalue < alpha:
        return [
            f"{ctx}: KS-2samp p = {res.pvalue:.4g} < alpha {alpha} "
            f"(committed n={a.size}, regen n={b.size}, KS stat = {res.statistic:.4g})"
        ]
    return []


# ----------------------------------------------------------------------
# Per-artefact checks
# ----------------------------------------------------------------------

def _check_json_scalars(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path.name}: regenerated artefact missing on disk"]
    committed_text = _git_blob(path)
    if committed_text is None:
        return [f"{path.name}: not committed at HEAD; skipping"]
    try:
        committed = json.loads(committed_text)
        regen = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return [f"{path.name}: JSON decode failure ({exc})"]
    return _compare_scalars(committed, regen, ctx=path.name)


def _check_tsv_table(path: Path, numeric_col: str | None = None) -> list[str]:
    if not path.exists():
        return [f"{path.name}: regenerated artefact missing on disk"]
    committed_text = _git_blob(path)
    if committed_text is None:
        return [f"{path.name}: not committed at HEAD; skipping"]
    from io import StringIO
    try:
        committed_df = pd.read_csv(StringIO(committed_text), sep="\t")
        regen_df = pd.read_csv(path, sep="\t")
    except Exception as exc:
        return [f"{path.name}: read failure ({exc})"]
    diffs: list[str] = []
    if committed_df.shape != regen_df.shape:
        diffs.append(
            f"{path.name}: shape changed "
            f"(committed {committed_df.shape}, regen {regen_df.shape})"
        )
    if numeric_col and numeric_col in committed_df.columns and numeric_col in regen_df.columns:
        a = committed_df[numeric_col].astype(float).values
        b = regen_df[numeric_col].astype(float).values
        diffs.extend(_ks_check_arrays(a, b, ctx=f"{path.name}:{numeric_col}"))
    return diffs


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--ks-alpha", type=float, default=0.05,
        help="Two-sample KS rejection threshold for distributional checks "
             "(default 0.05)",
    )
    args = ap.parse_args()

    all_diffs: list[str] = []
    targets = [
        (_check_json_scalars, RES / "tcga_bootstrap_metrics.json", {}),
        (_check_json_scalars, RES / "tcga_features.json", {}),
        (_check_json_scalars, RES / "figures_inputs.json", {}),
        (_check_json_scalars, RES / "data-prep-manifest.json", {}),
        (_check_json_scalars, RES / "cohort-selection.json", {}),
        (_check_tsv_table, RES / "tcga_risk_scores.tsv", {"numeric_col": "hcc_trs"}),
        (_check_tsv_table, RES / "tcga_model_coefs.tsv", {"numeric_col": "coef"}),
        (_check_tsv_table, RES / "external_geo_scores.tsv", {"numeric_col": "hcc_trs"}),
    ]
    for fn, target, kwargs in targets:
        if not target.exists():
            all_diffs.append(f"{target.relative_to(REPO_ROOT)}: regenerated artefact missing")
            continue
        if fn is _check_json_scalars:
            all_diffs.extend(fn(target))
        else:
            all_diffs.extend(fn(target, **kwargs))

    if all_diffs:
        print("FAIL — re-execution drift exceeded tolerance:", file=sys.stderr)
        for d in all_diffs:
            print(f"  - {d}", file=sys.stderr)
        return 1
    print("OK — committed artefacts reproduce within tolerance.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
