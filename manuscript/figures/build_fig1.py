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

LAYER_ORDER = ["operator", "layer1", "review", "layer2", "layer3"]
LAYER_LABEL = {
    "operator": "Operator\n(prereg, fix, tag)",
    "layer1": "Layer 1\n(pipeline)",
    "review": "Reviewer\nsubagent",
    "layer2": "Layer 2\n(audit)",
    "layer3": "Layer 3\n(validation)",
}
LAYER_COLOR = {
    "operator": "#5a4fcf",
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


def is_case_study_scope(commit: dict) -> bool:
    """True if the commit is part of the case-study disclosure-2.0
    manifest. The Viewpoint manuscript and its own reviewer loop are
    intentionally excluded: this figure depicts the supporting case
    study's process, not the meta-process of writing the Viewpoint."""
    paths = commit["paths"]
    case_study_prefixes = (
        "case-study/",
        "reviewer-logs/audit/",
        "reviewer-logs/round-",  # case-study reviewer rounds (numeric)
    )
    if any(any(p.startswith(prefix) for prefix in case_study_prefixes)
           for p in paths):
        return True
    if any(p == "docs/prereg.md" for p in paths):
        return True  # Layer-3 preregistration anchor
    return False


def classify(commit: dict) -> str:
    """Layer attribution within the case-study scope.

    Layer 3 is checked before Layer 1 because Layer-3 commits live under
    case-study/ paths (case-study/analysis/layer3_external_validation.py,
    case-study/data/results/layer3_*.json) and would otherwise be swept
    into Layer 1.
    """
    paths = commit["paths"]
    subject = commit.get("subject", "").lower()
    if any("layer3" in p.lower() for p in paths) or "layer 3" in subject or "layer-3" in subject:
        return "layer3"
    if any(p.startswith("reviewer-logs/audit/") for p in paths):
        return "layer2"
    if any(p.startswith("reviewer-logs/round-") for p in paths):
        return "review"
    if any(p == "docs/prereg.md" for p in paths):
        return "operator"
    if any(p.startswith("case-study/") for p in paths):
        return "layer1"
    return "operator"


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
    all_commits = git_log()
    all_tags = git_tags()
    # Filter to case-study scope only: this figure documents the
    # supporting case study's Disclosure 2.0 manifest, not the Viewpoint's
    # own commit history.
    commits = [c for c in all_commits if is_case_study_scope(c)]
    case_study_tag_prefix = "case-study-"
    tags = [t for t in all_tags if t[0].startswith(case_study_tag_prefix)]
    if not commits:
        raise SystemExit("no case-study commits found")

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
    ax.set_title("Case-study Disclosure 2.0 artefact ledger",
                 fontsize=12, loc="left", fontweight="bold")

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
