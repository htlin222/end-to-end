"""Build Figure 1 — case-study artefact ledger.

Each commit occupies an equal vertical slot (ordinal axis); long
wall-clock gaps between commits do not produce empty bands and dense
clusters do not collapse onto one row. Time labels appear only where
they matter: at the first commit, at each tag, and at HEAD.

Filtered to case-study scope only (the Viewpoint manuscript's own
commits and tags are deliberately excluded). Five swimlanes:
Operator (preregistration / fixes / tag pushes), Layer 1 (autonomous
pipeline), Reviewer subagent (case-study reviewer rounds 1-N),
Layer 2 (sealed audit), Layer 3 (external validation).
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = REPO_ROOT / "manuscript" / "figures" / "fig1-artifact-ledger.pdf"

LAYER_ORDER = ["operator", "layer1", "review", "layer2", "layer3"]
LAYER_LABEL = {
    "operator": "Operator",
    "layer1": "Layer 1",
    "review": "Reviewer",
    "layer2": "Layer 2",
    "layer3": "Layer 3",
}
LAYER_SUBLABEL = {
    "operator": "prereg / fix / tag",
    "layer1": "pipeline",
    "review": "subagent",
    "layer2": "audit",
    "layer3": "validation",
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
    paths = commit["paths"]
    case_study_prefixes = (
        "case-study/",
        "reviewer-logs/audit/",
        "reviewer-logs/round-",
    )
    if any(any(p.startswith(prefix) for prefix in case_study_prefixes)
           for p in paths):
        return True
    if any(p == "docs/prereg.md" for p in paths):
        return True
    return False


def classify(commit: dict) -> str:
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


def find_tag_commit_index(tag_date: datetime, commits: list[dict]) -> int | None:
    """Return the ordinal index (0-based) of the commit closest to and
    not after the tag date. Returns None if no such commit exists."""
    best = None
    for i, c in enumerate(commits):
        if c["date"] <= tag_date:
            best = i
        else:
            break
    return best


def main() -> None:
    all_commits = git_log()
    all_tags = git_tags()
    commits = [c for c in all_commits if is_case_study_scope(c)]
    tags = [t for t in all_tags if t[0].startswith("case-study-")]
    if not commits:
        raise SystemExit("no case-study commits found")

    n = len(commits)
    n_ai = sum(1 for c in commits if c["ai_assisted"])
    n_op = n - n_ai
    # Ordinal y: index i -> y = -i/(n-1) (0 at top, -1 at bottom)
    def y_of(i: int) -> float:
        return -i / max(n - 1, 1)

    # Cap figure height so 50-commit case studies don't produce a 16-inch
    # banner; 8.5 inches is roughly Lancet-DH column-width-by-aspect.
    fig_height = min(8.8, max(6.2, 0.28 * n))
    fig = plt.figure(figsize=(11.0, fig_height))
    # Reserve a header row for title+legend on top of each panel and a
    # data row below; the explicit subplots_adjust call below pins the
    # margins so the legend never collides with the panel titles.
    gs = fig.add_gridspec(
        1, 2,
        width_ratios=[1.5, 1.0],
        wspace=0.04,
    )
    ax = fig.add_subplot(gs[0, 0])
    ax_evt = fig.add_subplot(gs[0, 1])

    swimlane_x = {name: i for i, name in enumerate(LAYER_ORDER)}

    # Subtle alternating row banding to help read across columns
    for i in range(n):
        if i % 2 == 0:
            ax.axhspan(y_of(i) - 0.5 / max(n - 1, 1),
                       y_of(i) + 0.5 / max(n - 1, 1),
                       color="#f4f4f4", zorder=0, alpha=0.45)

    # Swimlane backgrounds (vertical stripes)
    for name, x in swimlane_x.items():
        ax.axvline(x, color=LAYER_COLOR[name], linewidth=14, zorder=1,
                   solid_capstyle="butt", alpha=0.08)

    # Headers (two-line)
    header_y = 0.05
    for name, x in swimlane_x.items():
        ax.text(x, header_y, LAYER_LABEL[name], ha="center", va="bottom",
                fontsize=10, fontweight="bold", color=LAYER_COLOR[name])
        ax.text(x, header_y - 0.015, LAYER_SUBLABEL[name], ha="center",
                va="top", fontsize=8, color=LAYER_COLOR[name], alpha=0.85)

    # Tag horizontal dashed lines + right-anchored boxed labels
    tag_y_positions: dict[str, float] = {}
    for tag_name, tag_date, tag_sha in tags:
        idx = find_tag_commit_index(tag_date, commits)
        if idx is None:
            continue
        yt = y_of(idx)
        tag_y_positions[tag_name] = yt
        ax.axhline(yt, color="#222", linewidth=0.6, linestyle="--",
                   alpha=0.55, zorder=2)
        ax.text(len(LAYER_ORDER) - 0.45, yt + 0.012, tag_name, ha="right",
                va="bottom", fontsize=8, color="#222", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="#444",
                          alpha=0.95, linewidth=0.5))

    # Commit markers
    for i, c in enumerate(commits):
        layer = classify(c)
        x = swimlane_x[layer]
        color = LAYER_COLOR[layer]
        marker = "o" if c["ai_assisted"] else "s"
        ax.scatter(x, y_of(i), s=42, c=color, marker=marker,
                   edgecolors="white", linewidths=0.9, zorder=4)

    # Time labels on the left axis: first, every tag, and last
    left_x = -0.55
    earliest = commits[0]["date"]
    latest = commits[-1]["date"]

    def fmt_dt(dt: datetime) -> str:
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Build label set: index -> date string
    label_idx: dict[int, str] = {0: fmt_dt(earliest)}
    label_idx[n - 1] = fmt_dt(latest)
    for tag_name, tag_date, _sha in tags:
        idx = find_tag_commit_index(tag_date, commits)
        if idx is not None:
            label_idx[idx] = fmt_dt(commits[idx]["date"])

    for idx, txt in label_idx.items():
        yt = y_of(idx)
        ax.plot([left_x + 0.05, -0.35], [yt, yt],
                color="#999", linewidth=0.4, alpha=0.6)
        ax.text(left_x, yt, txt, ha="right", va="center", fontsize=7,
                color="#444")

    ax.set_xlim(-1.4, len(LAYER_ORDER) - 0.3)
    ax.set_ylim(-1.04, 0.13)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_title("Case-study Disclosure 2.0 artefact ledger",
                 fontsize=13, loc="left", fontweight="bold", pad=8)

    # Single figure-level legend at the very bottom, outside the panels,
    # so it never collides with milestone text.
    legend_handles = [
        mpatches.Patch(color=LAYER_COLOR[k], label=f"{LAYER_LABEL[k]} ({LAYER_SUBLABEL[k]})")
        for k in LAYER_ORDER
    ]
    legend_handles.append(plt.Line2D([0], [0], marker="o", color="w",
                                     markerfacecolor="#888", markersize=8,
                                     markeredgecolor="white", markeredgewidth=0.9,
                                     label=f"AI-co-authored commit ({n_ai})"))
    if n_op > 0:
        legend_handles.append(plt.Line2D([0], [0], marker="s", color="w",
                                         markerfacecolor="#888", markersize=8,
                                         markeredgecolor="white", markeredgewidth=0.9,
                                         label=f"operator-only commit ({n_op})"))
    fig.legend(handles=legend_handles, loc="lower center",
               bbox_to_anchor=(0.5, 0.0), ncol=len(legend_handles),
               fontsize=8, frameon=False, columnspacing=1.4,
               handletextpad=0.4)

    # ----- Right panel: milestone events -----
    ax_evt.axis("off")
    ax_evt.set_xlim(0, 1)
    ax_evt.set_ylim(-1.04, 0.13)
    op_str = f"{n_op} operator-only" if n_op > 0 else "no operator-only commits"
    ax_evt.set_title(
        f"Milestones  ({n} commits: {n_ai} AI-co-authored, {op_str};\n"
        f"{len(tags)} tagged releases)",
        fontsize=10, loc="left", fontweight="bold", pad=8
    )

    milestones = []
    seen_layers: set[str] = set()
    # First commit
    if commits:
        milestones.append({**commits[0], "label": "scaffold (first case-study commit)", "idx": 0})
    # First per layer
    for i, c in enumerate(commits):
        layer = classify(c)
        if layer not in seen_layers and layer in {"layer1", "review", "layer2", "layer3"}:
            milestones.append({**c, "label": f"first {LAYER_LABEL[layer]} ({LAYER_SUBLABEL[layer]})", "idx": i})
            seen_layers.add(layer)
    # Tags
    by_hash = {c["hash"]: (i, c) for i, c in enumerate(commits)}
    for tag_name, tag_date, tag_sha in tags:
        if tag_sha in by_hash:
            i, c = by_hash[tag_sha]
            milestones.append({**c, "label": f"tag {tag_name}", "idx": i})
        else:
            idx = find_tag_commit_index(tag_date, commits)
            if idx is not None:
                c = commits[idx]
                milestones.append({**c, "label": f"tag {tag_name} (at {c['hash']})", "idx": idx})
    # HEAD only if it is NOT already represented by a tag at the same idx
    tagged_idxs = {m["idx"] for m in milestones if m["label"].startswith("tag ")}
    if (n - 1) not in tagged_idxs:
        milestones.append({**commits[-1], "label": "HEAD", "idx": n - 1})
    # Dedupe by idx; if multiple labels share the idx, merge them into one entry
    by_idx: dict[int, dict] = {}
    for m in milestones:
        idx = m["idx"]
        if idx in by_idx:
            existing = by_idx[idx]
            existing["label"] = f"{existing['label']}; {m['label']}"
        else:
            by_idx[idx] = dict(m)
    milestones = sorted(by_idx.values(), key=lambda m: m["idx"])

    # Stagger labels vertically if too close (in ordinal y)
    min_gap = 0.085
    placed_y: list[float] = []
    for m in milestones:
        yt_raw = y_of(m["idx"])
        yt = yt_raw
        while any(abs(yt - p) < min_gap for p in placed_y):
            yt -= 0.012
        placed_y.append(yt)
        layer = classify(m)
        color = LAYER_COLOR[layer]
        marker = "o" if m["ai_assisted"] else "s"
        ax_evt.scatter(0.025, yt, s=34, c=color, marker=marker,
                       edgecolors="white", linewidths=0.7, zorder=3)
        text = f"{m['hash']}  {m['label']}"
        ax_evt.text(0.07, yt + 0.005, text, ha="left", va="bottom",
                    fontsize=8, color="#1a1a1a", fontweight="bold")
        subject = m["subject"]
        if len(subject) > 65:
            subject = subject[:64] + "…"
        ax_evt.text(0.07, yt - 0.005, subject, ha="left", va="top",
                    fontsize=6.5, color="#555", style="italic")
        m["_label_y"] = yt
        m["_raw_y"] = yt_raw

    # Leader lines from left swimlane to right milestone label
    for m in milestones:
        layer = classify(m)
        y_raw = m.get("_raw_y", y_of(m["idx"]))
        y_label = m.get("_label_y", y_raw)
        ax.plot([swimlane_x[layer] + 0.18, len(LAYER_ORDER) - 0.25],
                [y_raw, y_label], color="#bbbbbb", linewidth=0.5,
                zorder=2, alpha=0.55)

    # Leave room at the bottom for the figure-level legend, and at the
    # top for the section titles.
    fig.subplots_adjust(left=0.10, right=0.99, top=0.91, bottom=0.07,
                        wspace=0.04)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")

    sidecar = OUT.with_suffix(".manifest.json")
    sidecar.write_text(json.dumps({
        "scope": "case-study only (Viewpoint commits and tags excluded)",
        "axis": "ordinal commit index (equal spacing per commit)",
        "generated_from_commit": commits[-1]["hash"],
        "total_commits": n,
        "ai_co_authored_commits": n_ai,
        "operator_only_commits": n_op,
        "tags": [t[0] for t in tags],
        "milestones_shown": [m["hash"] for m in milestones],
        "earliest_commit": commits[0]["date"].isoformat(),
        "latest_commit": commits[-1]["date"].isoformat(),
    }, indent=2))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
