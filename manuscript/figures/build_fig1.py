"""Build Figure 1 — the artefact ledger.

Reads the repository's git log and the contents of `reviewer-logs/` to
produce the chronological artefact ledger that the Viewpoint's
Figure 1 visualises. Output: `manuscript/figures/fig1-artifact-ledger.pdf`.

The figure is two-axis:
  - Vertical: time, top to bottom (commit timestamp).
  - Horizontal: three swimlanes (Layer 1 / Layer 2 / Layer 3).
Glyphs encode commit author type (operator vs AI-assisted commits, both
identified by the `Co-Authored-By: Claude Opus 4.7` trailer), reviewer
rounds, audit checkpoints, and tagged releases.

The figure is deterministic for a given repository state. Re-running on
the same commit produces a byte-identical PDF (within matplotlib
backend tolerance).

Usage:
    uv run python manuscript/figures/build_fig1.py
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = REPO_ROOT / "manuscript" / "figures" / "fig1-artifact-ledger.pdf"

LAYER_MARKERS = {
    "viewpoint": ("Operator / Viewpoint", "#5a4fcf"),
    "layer1": ("Layer 1 (pipeline)", "#1f8a3a"),
    "layer2": ("Layer 2 (audit)", "#c54a2c"),
    "layer3": ("Layer 3 (validation)", "#1c5d8c"),
    "review": ("Reviewer subagent", "#b08a00"),
    "release": ("Tagged release", "#000000"),
}


def git_log() -> list[dict]:
    """Return list of commits with date, hash, subject, paths, ai_assisted."""
    fmt = "%H%x1f%aI%x1f%s%x1f%(trailers:key=Co-Authored-By,valueonly,separator=|)"
    raw = subprocess.check_output(
        ["git", "-C", str(REPO_ROOT), "log", "--reverse", f"--pretty=format:{fmt}"],
        text=True,
    )
    commits = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        h, date, subject, trailers = line.split("\x1f", 3)
        paths_raw = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "show", "--name-only",
             "--pretty=format:", h],
            text=True,
        )
        paths = [p.strip() for p in paths_raw.splitlines() if p.strip()]
        commits.append({
            "hash": h[:7],
            "date": datetime.fromisoformat(date).astimezone(timezone.utc),
            "subject": subject,
            "paths": paths,
            "ai_assisted": "Claude" in trailers,
        })
    return commits


def classify(commit: dict) -> str:
    paths = commit["paths"]
    if any(p.startswith("case-study/") for p in paths):
        return "layer1"
    if any(p.startswith("reviewer-logs/audit/") for p in paths):
        return "layer2"
    if "data/results/layer3" in " ".join(paths):
        return "layer3"
    if any(p.startswith("reviewer-logs/") for p in paths):
        return "review"
    return "viewpoint"


def git_tags() -> list[tuple[str, datetime]]:
    """Return list of (tag_name, tag_date) tuples."""
    raw = subprocess.check_output(
        ["git", "-C", str(REPO_ROOT), "for-each-ref",
         "--format=%(refname:short)%x1f%(creatordate:iso-strict)",
         "refs/tags"],
        text=True,
    )
    out = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        name, date = line.split("\x1f", 1)
        out.append((name, datetime.fromisoformat(date).astimezone(timezone.utc)))
    return out


def main() -> None:
    commits = git_log()
    tags = git_tags()
    if not commits:
        raise SystemExit("no commits found")

    fig, ax = plt.subplots(figsize=(8.5, max(6.0, 0.22 * len(commits))))

    swimlanes = ["viewpoint", "layer1", "review", "layer2", "layer3"]
    swimlane_x = {name: i for i, name in enumerate(swimlanes)}

    earliest = commits[0]["date"]
    latest = commits[-1]["date"]
    span = max((latest - earliest).total_seconds(), 1.0)

    def y(date: datetime) -> float:
        return -((date - earliest).total_seconds() / span)

    # Background swimlanes
    for name, x in swimlane_x.items():
        ax.axvline(x, color="#dddddd", linewidth=0.5, zorder=0)
        ax.text(x, 0.04, LAYER_MARKERS[name][0], rotation=0,
                ha="center", va="bottom", fontsize=8,
                color=LAYER_MARKERS[name][1])

    # Commit markers
    for c in commits:
        layer = classify(c)
        x = swimlane_x.get(layer, 0)
        color = LAYER_MARKERS[layer][1]
        marker = "o" if c["ai_assisted"] else "s"
        ax.scatter(x, y(c["date"]), s=36, c=color, marker=marker,
                   edgecolors="black", linewidths=0.4, zorder=3)
        ax.text(x + 0.12, y(c["date"]),
                f"{c['hash']} {c['subject'][:48]}",
                ha="left", va="center", fontsize=6.5, color="#222")

    # Tags as horizontal markers
    for tag, tdate in tags:
        ax.axhline(y(tdate), color="black", linewidth=0.6,
                   linestyle="--", alpha=0.4, zorder=1)
        ax.text(len(swimlanes) - 0.4, y(tdate), tag, ha="right",
                va="bottom", fontsize=7, color="black")

    # Legend
    handles = [
        mpatches.Patch(color=LAYER_MARKERS[k][1], label=LAYER_MARKERS[k][0])
        for k in swimlanes
    ]
    handles.append(mpatches.Patch(color="white",
                                  label="square = operator-only commit"))
    handles.append(mpatches.Patch(color="white",
                                  label="circle = AI-co-authored commit"))
    ax.legend(handles=handles, loc="lower left", fontsize=7,
              bbox_to_anchor=(0.0, -0.04), ncol=2, frameon=False)

    ax.set_xlim(-0.5, len(swimlanes) - 0.3)
    ax.set_ylim(-1.05, 0.10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_title("Disclosure 2.0 artefact ledger", fontsize=11)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")

    # Sidecar manifest for re-execution audit
    sidecar = OUT.with_suffix(".manifest.json")
    sidecar.write_text(json.dumps({
        "generated_from_commit": commits[-1]["hash"],
        "total_commits": len(commits),
        "ai_co_authored_commits": sum(1 for c in commits if c["ai_assisted"]),
        "operator_only_commits": sum(1 for c in commits if not c["ai_assisted"]),
        "tags": [t[0] for t in tags],
        "earliest_commit": earliest.isoformat(),
        "latest_commit": latest.isoformat(),
    }, indent=2))
    print(f"wrote {OUT}")
    print(f"wrote {sidecar}")


if __name__ == "__main__":
    main()
