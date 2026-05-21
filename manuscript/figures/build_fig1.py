"""Build Figure 1 — the artefact ledger (compact swimlane).

Reads git log + tags. Each commit is a small marker in its layer
swimlane on the time axis. No per-commit text (too dense at 50+
commits); instead, a side legend explains the encoding and a small
right-hand event panel lists the milestone commits (tagged releases
+ first appearance of each layer).
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

LAYER_ORDER = ["viewpoint", "layer1", "review", "layer2", "layer3"]
LAYER_LABEL = {
    "viewpoint": "Operator / Viewpoint",
    "layer1": "Layer 1 (pipeline)",
    "review": "Reviewer subagent",
    "layer2": "Layer 2 (audit)",
    "layer3": "Layer 3 (validation)",
}
LAYER_COLOR = {
    "viewpoint": "#5a4fcf",
    "layer1": "#1f8a3a",
    "review": "#b08a00",
    "layer2": "#c54a2c",
    "layer3": "#1c5d8c",
}


def git_log() -> list[dict]:
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
            "full_hash": h,
            "date": datetime.fromisoformat(date).astimezone(timezone.utc),
            "subject": subject,
            "paths": paths,
            "ai_assisted": "Claude" in trailers,
        })
    return commits


def classify(commit: dict) -> str:
    """Layer attribution. Layer 3 is checked before Layer 1 because
    Layer-3 commits live under case-study/ paths (case-study/analysis/
    layer3_external_validation.py, case-study/data/results/layer3_*.json)
    and would otherwise be swept into Layer 1."""
    paths = commit["paths"]
    if any("layer3" in p.lower() for p in paths):
        return "layer3"
    if any(p.startswith("reviewer-logs/audit/") for p in paths):
        return "layer2"
    if any(p.startswith("case-study/") for p in paths):
        return "layer1"
    if any(p.startswith("reviewer-logs/") for p in paths):
        return "review"
    return "viewpoint"


def git_tags() -> list[tuple[str, datetime, str]]:
    raw = subprocess.check_output(
        ["git", "-C", str(REPO_ROOT), "for-each-ref",
         "--format=%(refname:short)\t%(creatordate:iso-strict)\t%(objectname)",
         "refs/tags"],
        text=True,
    )
    out = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 2)
        if len(parts) < 2:
            continue
        name = parts[0]
        try:
            date = datetime.fromisoformat(parts[1]).astimezone(timezone.utc)
        except ValueError:
            continue
        sha = parts[2] if len(parts) > 2 else ""
        out.append((name, date, sha[:7]))
    return sorted(out, key=lambda x: x[1])


def select_milestones(commits: list[dict], tags: list[tuple[str, datetime, str]]) -> list[dict]:
    """Pick the commits worth printing the subject of."""
    by_hash = {c["hash"]: c for c in commits}
    milestones: list[dict] = []
    seen_layers: set[str] = set()
    # First commit
    if commits:
        milestones.append({**commits[0], "label": "scaffold"})
    # First commit per layer
    for c in commits:
        layer = classify(c)
        if layer not in seen_layers and layer in {"layer1", "review", "layer2", "layer3"}:
            milestones.append({**c, "label": f"first {LAYER_LABEL[layer].lower()}"})
            seen_layers.add(layer)
    # Tags
    for name, dt, sha in tags:
        c = by_hash.get(sha)
        if c:
            milestones.append({**c, "label": f"tag {name}"})
    # Latest commit
    if commits:
        milestones.append({**commits[-1], "label": "HEAD"})
    # Dedupe by hash, keep first occurrence's label
    seen: set[str] = set()
    dedup = []
    for m in milestones:
        if m["hash"] in seen:
            continue
        seen.add(m["hash"])
        dedup.append(m)
    return dedup


def main() -> None:
    commits = git_log()
    tags = git_tags()
    if not commits:
        raise SystemExit("no commits found")

    fig = plt.figure(figsize=(10.5, 6.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.6, 1.0], wspace=0.02)
    ax = fig.add_subplot(gs[0, 0])
    ax_evt = fig.add_subplot(gs[0, 1])

    swimlane_x = {name: i for i, name in enumerate(LAYER_ORDER)}
    earliest = commits[0]["date"]
    latest = commits[-1]["date"]
    span = max((latest - earliest).total_seconds(), 1.0)

    def y(date: datetime) -> float:
        return -((date - earliest).total_seconds() / span)

    # Swimlane background
    for name, x in swimlane_x.items():
        ax.axvline(x, color="#e8e8e8", linewidth=8, zorder=0, solid_capstyle="butt", alpha=0.45)
    # Headers above plot area
    for name, x in swimlane_x.items():
        ax.text(x, 0.06, LAYER_LABEL[name].replace(" (", "\n("), ha="center",
                va="bottom", fontsize=8, fontweight="bold",
                color=LAYER_COLOR[name])

    # Commit dots
    for c in commits:
        layer = classify(c)
        x = swimlane_x[layer]
        color = LAYER_COLOR[layer]
        marker = "o" if c["ai_assisted"] else "s"
        ax.scatter(x, y(c["date"]), s=28, c=color, marker=marker,
                   edgecolors="white", linewidths=0.6, zorder=3)

    # Tags as horizontal lines + right-edge labels
    for name, dt, _sha in tags:
        yt = y(dt)
        ax.axhline(yt, color="#222", linewidth=0.5, linestyle="--",
                   alpha=0.45, zorder=1)
        ax.text(len(LAYER_ORDER) - 0.4, yt, name, ha="right", va="bottom",
                fontsize=7, color="#222",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#888",
                          alpha=0.85, linewidth=0.4))

    ax.set_xlim(-0.5, len(LAYER_ORDER) - 0.3)
    ax.set_ylim(-1.04, 0.18)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_title("Disclosure 2.0 artefact ledger", fontsize=12, loc="left",
                 fontweight="bold")

    # Time labels at left
    ax.text(-0.3, 0.0, earliest.strftime("%Y-%m-%d %H:%M"), ha="right",
            va="center", fontsize=7, color="#555")
    ax.text(-0.3, -1.0, latest.strftime("%Y-%m-%d %H:%M"), ha="right",
            va="center", fontsize=7, color="#555")

    # Legend
    legend_handles = [
        mpatches.Patch(color=LAYER_COLOR[k], label=LAYER_LABEL[k])
        for k in LAYER_ORDER
    ]
    legend_handles.append(plt.Line2D([0], [0], marker="o", color="w",
                                     markerfacecolor="#888", markersize=7,
                                     label="AI-co-authored commit"))
    legend_handles.append(plt.Line2D([0], [0], marker="s", color="w",
                                     markerfacecolor="#888", markersize=7,
                                     label="operator-only commit"))
    ax.legend(handles=legend_handles, loc="lower center",
              bbox_to_anchor=(0.5, -0.18), fontsize=7, ncol=2,
              frameon=False)

    # Right panel: milestone events
    ax_evt.axis("off")
    ax_evt.set_xlim(0, 1)
    ax_evt.set_ylim(-1.04, 0.18)
    ax_evt.set_title(
        f"Milestones  ({len(commits)} commits, {len(tags)} tags)",
        fontsize=10, loc="left", fontweight="bold"
    )

    milestones = select_milestones(commits, tags)
    # Stagger milestone labels vertically to avoid overlap when commits
    # cluster in time (each label takes ~0.06 of normalised y).
    min_gap = 0.075
    placed_y: list[float] = []
    for m in milestones:
        layer = classify(m)
        yt_raw = y(m["date"])
        # Find a non-overlapping y close to yt_raw
        yt = yt_raw
        while any(abs(yt - p) < min_gap for p in placed_y):
            yt -= 0.012
        placed_y.append(yt)
        color = LAYER_COLOR[layer]
        ax_evt.scatter(0.03, yt, s=24, c=color, marker="o" if m["ai_assisted"] else "s",
                       edgecolors="white", linewidths=0.5, zorder=3)
        text = f"{m['hash']}  {m['label']}"
        ax_evt.text(0.08, yt, text, ha="left", va="center", fontsize=7.5,
                    color="#222", fontweight="bold")
        subject = m["subject"][:60] + ("…" if len(m["subject"]) > 60 else "")
        ax_evt.text(0.08, yt - 0.028, subject, ha="left", va="top",
                    fontsize=6.2, color="#555", style="italic")
        # Track where the label landed so connection lines target it
        m["_label_y"] = yt
        m["_raw_y"] = yt_raw

    # Connecting lines between ax and ax_evt for milestones.
    # When the label was staggered downward, draw a subtle bent
    # leader so the reader can trace label -> ledger position.
    for m in milestones:
        layer = classify(m)
        y_raw = m.get("_raw_y", y(m["date"]))
        y_label = m.get("_label_y", y_raw)
        ax.plot([swimlane_x[layer] + 0.15, len(LAYER_ORDER) - 0.2],
                [y_raw, y_label], color="#cccccc", linewidth=0.4,
                zorder=1, alpha=0.4)

    fig.tight_layout(pad=0.5)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")

    sidecar = OUT.with_suffix(".manifest.json")
    sidecar.write_text(json.dumps({
        "generated_from_commit": commits[-1]["hash"],
        "total_commits": len(commits),
        "ai_co_authored_commits": sum(1 for c in commits if c["ai_assisted"]),
        "operator_only_commits": sum(1 for c in commits if not c["ai_assisted"]),
        "tags": [t[0] for t in tags],
        "milestones_shown": [m["hash"] for m in milestones],
        "earliest_commit": earliest.isoformat(),
        "latest_commit": latest.isoformat(),
    }, indent=2))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
