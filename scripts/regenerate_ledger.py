#!/usr/bin/env python3
"""Regenerate `docs/ledger.md` from `git log`.

The Viewpoint argues that the artefact ledger is the chronological
narrative behind Figure 1 and is regenerable on demand from the
committed state of the repository. This script is the regenerator;
the build_fig1 script in `manuscript/figures/` consumes the same
git data to render the figure.

Usage:
    uv run python scripts/regenerate_ledger.py

Output: `docs/ledger.md` (overwritten in place).
"""
from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT = REPO_ROOT / "docs" / "ledger.md"


def commit_rows() -> list[tuple[str, datetime, str, str, bool, str]]:
    """Return rows: (short_sha, date, layer, subject, ai, paths_signature)."""
    fmt = "%H%x1f%aI%x1f%s%x1f%(trailers:key=Co-Authored-By,valueonly,separator=|)"
    raw = subprocess.check_output(
        ["git", "-C", str(REPO_ROOT), "log", "--reverse", f"--pretty=format:{fmt}"],
        text=True,
    )
    out = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        h, date_s, subject, trailers = line.split("\x1f", 3)
        paths_raw = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "show", "--name-only",
             "--pretty=format:", h],
            text=True,
        )
        paths = [p.strip() for p in paths_raw.splitlines() if p.strip()]
        layer = _classify(paths)
        ai = "Claude" in trailers
        sig = _path_signature(paths)
        out.append((h[:7], datetime.fromisoformat(date_s).astimezone(timezone.utc),
                    layer, subject, ai, sig))
    return out


def _classify(paths: list[str]) -> str:
    if any(p.startswith("case-study/") for p in paths):
        return "Layer 1"
    if any(p.startswith("reviewer-logs/audit/") for p in paths):
        return "Layer 2"
    if any("layer3" in p for p in paths):
        return "Layer 3"
    if any(p.startswith("reviewer-logs/") for p in paths):
        return "Reviewer"
    if any(p.startswith("manuscript/") for p in paths):
        return "Viewpoint"
    if any(p.startswith("prompts/") for p in paths):
        return "Prompts"
    if any(p.startswith("docs/") for p in paths):
        return "Docs"
    return "Operator"


def _path_signature(paths: list[str]) -> str:
    top = {p.split("/", 1)[0] for p in paths if p}
    return ", ".join(sorted(top))


def tag_rows() -> list[tuple[str, datetime]]:
    """Return (tag_name, creatordate) pairs.

    git for-each-ref does not interpret %xNN escapes the way git log
    does, so we use a literal tab as the separator.
    """
    raw = subprocess.check_output(
        ["git", "-C", str(REPO_ROOT), "for-each-ref",
         "--format=%(refname:short)\t%(creatordate:iso-strict)",
         "refs/tags"],
        text=True,
    )
    out = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        name, date_s = parts
        try:
            out.append((name, datetime.fromisoformat(date_s).astimezone(timezone.utc)))
        except ValueError:
            continue
    return out


def main() -> None:
    commits = commit_rows()
    tags = tag_rows()

    n_total = len(commits)
    n_ai = sum(1 for c in commits if c[4])
    n_op = n_total - n_ai

    lines: list[str] = []
    lines.append("# Artefact Ledger")
    lines.append("")
    lines.append("Regenerated from `git log` by "
                 "`scripts/regenerate_ledger.py`. Re-run after every commit "
                 "or at release time. This file is the source of truth "
                 "behind Figure 1 in the Viewpoint and is referenced from "
                 "`docs/design.md` Section ``Repository as artefact ledger''.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total commits: **{n_total}**")
    lines.append(f"- AI-co-authored commits: **{n_ai}**")
    lines.append(f"- Operator-only commits: **{n_op}**")
    if tags:
        lines.append(f"- Tags: {', '.join(t[0] for t in tags)}")
    else:
        lines.append("- Tags: (none yet)")
    if commits:
        lines.append(f"- First commit: {commits[0][1].isoformat()}")
        lines.append(f"- Latest commit: {commits[-1][1].isoformat()}")
    lines.append("")
    lines.append("## Chronological narrative")
    lines.append("")
    lines.append("| # | Time (UTC) | SHA | Layer | Author | Subject |")
    lines.append("|---:|---|---|---|---|---|")
    for i, (sha, dt, layer, subject, ai, _sig) in enumerate(commits, start=1):
        author = "AI-co-authored" if ai else "operator-only"
        # Markdown-escape pipes in subject
        safe_subject = subject.replace("|", "\\|")
        lines.append(f"| {i} | {dt.strftime('%Y-%m-%d %H:%M')} | "
                     f"`{sha}` | {layer} | {author} | {safe_subject} |")
    lines.append("")

    if tags:
        lines.append("## Tags")
        lines.append("")
        for name, dt in tags:
            lines.append(f"- **{name}** — {dt.isoformat()}")
        lines.append("")
    else:
        lines.append("## Tags")
        lines.append("")
        lines.append("None yet. The first tag will be `viewpoint-v1.0.0` at "
                     "submission state.")
        lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT} ({len(commits)} commits, {len(tags)} tags)")


if __name__ == "__main__":
    main()
