"""Build Figure 2 — policy-gap visualisation for the Viewpoint.

Static figure comparing the Lancet group's current generative-AI
policy classification against the Disclosure 2.0 standard the
Viewpoint proposes. No external data is required; this figure is a
schematic and is reproducible from its source row data only.

Usage:
    uv run python figures/build_fig2.py
Produces figures/fig2-policy-gap.pdf.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent

ACTIVITIES = [
    "Language editing",
    "Grammar repair",
    "Prose polishing",
    "Reference reformatting",
    "Argument development",
    "Methods drafting",
    "Literature review",
    "Claim selection",
    "Manuscript drafting",
    "Reviewer-subagent critique",
    "Image / figure generation",
    "Listing model as author",
]

# 0 = permitted (green), 1 = prohibited (red), 2 = required under Disclosure 2.0 (blue)
CURRENT_POLICY = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
DISCLOSURE_TWO = [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 1, 1]

LABELS = {0: "Permitted with brief\nacknowledgement",
          1: "Prohibited",
          2: "Permitted with full\nDisclosure 2.0 manifest"}
COLOR = {0: "#bfe5b4", 1: "#f4b5b5", 2: "#b9d6f2"}


def main() -> None:
    fig, ax = plt.subplots(figsize=(8.5, 6.0))
    n = len(ACTIVITIES)
    height = 0.42

    for i, activity in enumerate(ACTIVITIES):
        y = n - 1 - i
        ax.add_patch(Rectangle((0, y - height / 2), 1, height,
                               facecolor=COLOR[CURRENT_POLICY[i]],
                               edgecolor="#444", linewidth=0.6))
        ax.add_patch(Rectangle((1.05, y - height / 2), 1, height,
                               facecolor=COLOR[DISCLOSURE_TWO[i]],
                               edgecolor="#444", linewidth=0.6))
        ax.text(-0.05, y, activity, ha="right", va="center", fontsize=9)

    ax.text(0.5, n - 0.2, "Current Lancet AI policy", ha="center",
            fontsize=10, fontweight="bold")
    ax.text(1.55, n - 0.2, "Disclosure 2.0 (proposed)", ha="center",
            fontsize=10, fontweight="bold")

    ax.set_xlim(-2.3, 2.2)
    ax.set_ylim(-1.4, n)
    ax.axis("off")

    handles = [mpatches.Patch(color=COLOR[k], label=LABELS[k])
               for k in (0, 2, 1)]
    ax.legend(handles=handles, loc="lower center",
              bbox_to_anchor=(0.55, -0.05), ncol=3, frameon=False,
              fontsize=8.5)

    fig.tight_layout()
    out = HERE / "fig2-policy-gap.pdf"
    fig.savefig(out, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
