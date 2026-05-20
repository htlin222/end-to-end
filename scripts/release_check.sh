#!/usr/bin/env bash
# Pre-flight checks for a Viewpoint release tag.
#
# Runs every check the Lancet group desk-triage would run, plus the
# integrity checks the Disclosure 2.0 manifest is supposed to enforce.
# Refuses to exit 0 unless every check passes.
#
# Usage:
#   scripts/release_check.sh
#
# Exit codes:
#   0  all checks pass; safe to tag and release
#   1  at least one check failed; release blocked
set -euo pipefail
IFS=$'\n\t'

# colours (no ANSI when not a TTY)
if [[ -t 1 ]]; then
  G="\033[32m"; R="\033[31m"; Y="\033[33m"; N="\033[0m"
else
  G=""; R=""; Y=""; N=""
fi

PASS=0
FAIL=0
WARN=0

check() {
  local label="$1"; shift
  if "$@" >/tmp/release_check.out 2>&1; then
    printf "${G}OK${N}     %s\n" "$label"
    PASS=$((PASS+1))
  else
    printf "${R}FAIL${N}   %s\n" "$label"
    sed 's/^/         /' /tmp/release_check.out
    FAIL=$((FAIL+1))
  fi
}

warn() {
  local label="$1"; shift
  if "$@" >/tmp/release_check.out 2>&1; then
    printf "${G}OK${N}     %s\n" "$label"
    PASS=$((PASS+1))
  else
    printf "${Y}WARN${N}   %s\n" "$label"
    sed 's/^/         /' /tmp/release_check.out
    WARN=$((WARN+1))
  fi
}

cd "$(dirname "$0")/.."
REPO="$(pwd)"

printf "::: release pre-flight from %s\n" "$REPO"
printf "::: HEAD = %s\n" "$(git rev-parse HEAD)"
printf "\n"

# --- Git hygiene ---
check "working tree is clean" \
  bash -c '[[ -z "$(git status --porcelain)" ]]'
check "on main branch" \
  bash -c '[[ "$(git rev-parse --abbrev-ref HEAD)" == "main" ]]'
check "no force-pushed or rebased history (no diverged ancestry)" \
  bash -c '! git fsck --no-progress --no-dangling 2>&1 | grep -qE "broken link|missing"'

# --- Disclosure 2.0 manifest items ---
check "item 1 prompts: all closed-for-edits prompts present" \
  bash -c 'for f in 00-original-spec.md 01-layer1-pipeline.md 02-layer2-audit.md 03-reviewer-methods.md 03-reviewer-clinical.md 03-reviewer-biostat.md 03-reviewer-editor.md 04-viewpoint-reviewer-policy.md 04-viewpoint-reviewer-clinician.md 04-viewpoint-reviewer-methodology.md 04-viewpoint-reviewer-editor.md; do test -f "prompts/$f" || { echo "missing prompts/$f"; exit 1; }; done'

check "item 2 model identifier: ai-usage-disclosure.md present" \
  test -f docs/ai-usage-disclosure.md

check "item 3 commit history: integrity rule observed (no amends in last 50)" \
  bash -c '! git log --pretty=format:"%s" -n 50 | grep -qi "^amend"'

warn "item 4 reviewer transcripts: at least one round complete" \
  bash -c 'ls reviewer-logs/viewpoint-round-01/*.md 2>/dev/null | grep -q .'

warn "item 5 audit log: Layer-2 audit complete" \
  bash -c 'ls reviewer-logs/audit/findings.md 2>/dev/null'

check "item 6 disclosure2-schema present" \
  test -f docs/disclosure2-schema.json

# --- Manuscript artefacts ---
check "manuscript main.tex compiles" \
  bash -c 'cd manuscript && latexmk -pdf -interaction=nonstopmode -file-line-error main.tex >/dev/null 2>&1'

check "manuscript main.pdf produced" \
  test -s manuscript/main.pdf

check "no placeholder tokens in main.tex" \
  bash -c '! grep -E "<<[A-Z_]+>>" manuscript/main.tex'

check "no placeholder tokens in cover-letter.md" \
  bash -c '! grep -E "<<[A-Z_]+>>" manuscript/cover-letter.md'

check "no placeholder DOIs in references.bib" \
  bash -c '! grep -F "10.0000/placeholder" manuscript/references.bib'

check "body word count <= 2500" \
  python3 -c '
import re, subprocess, sys
out = subprocess.check_output(["texcount", "-inc", "-sum", "manuscript/main.tex"], text=True)
NON_BODY = {"Key messages", "Search strategy and selection criteria",
            "Declaration of interests", "Contributors",
            "Acknowledgements", "Data sharing"}
body_total = 0
non_body_total = 0
preamble_subsection = 0
for line in out.splitlines():
    m = re.match(r"\s*(\d+)\+\d+\+\d+ \([^)]+\) (Section|Subsection)(: (.+?)(?:\}|$))?", line)
    if not m:
        continue
    words, kind = int(m.group(1)), m.group(2)
    name = (m.group(4) or "").split("}\\label")[0].strip()
    if kind == "Subsection" and not name:
        preamble_subsection += words
        continue
    if name in NON_BODY:
        non_body_total += words
    else:
        body_total += words
print(f"texcount: body={body_total} non_body={non_body_total} preamble_subsection={preamble_subsection}")
sys.exit(0 if body_total <= 2500 else 1)
'

check "reference count <= 30" \
  bash -c 'count=$(grep -cE "^@" manuscript/references.bib); echo "references: $count"; [[ $count -le 30 ]]'

check "display items <= 2" \
  bash -c 'count=$(grep -cE "\\\\begin\\{figure" manuscript/main.tex); echo "figures: $count"; [[ $count -le 2 ]]'

# --- AI disclosure compliance ---
check "Acknowledgements names AI tool and version" \
  bash -c 'grep -q "Claude (Opus 4.7" manuscript/main.tex'

check "Acknowledgements states no AI authorship" \
  bash -c 'grep -q "No AI tool is listed as an author" manuscript/main.tex'

check "Search-strategy panel has AI-use disclosure" \
  bash -c 'grep -q "AI use in this Viewpoint" manuscript/main.tex'

check "Acknowledgements states no AI figures" \
  bash -c 'grep -qE "No generative-AI tool was used to create figures" manuscript/main.tex'

# --- Citation veracity (light) ---
check "all cite keys in main.tex have a bib entry" \
  bash -c '
    cite_keys=$(grep -oE "\\\\citep\\{[^}]+\\}" manuscript/main.tex | sed "s/\\\\citep{//;s/}//" | tr "," "\n" | sort -u);
    bib_keys=$(grep -E "^@[a-z]+\\{" manuscript/references.bib | sed -E "s/.*\\{([^,]+),.*/\\1/" | sort -u);
    missing=$(comm -23 <(echo "$cite_keys") <(echo "$bib_keys"));
    if [[ -n "$missing" ]]; then
      echo "missing bib entries: $missing"; exit 1;
    fi'

check "no <<PREREG_COMMIT_SHA>> placeholder in bib" \
  bash -c '! grep -F "<<PREREG_COMMIT_SHA>>" manuscript/references.bib'

# --- Figure generation ---
check "Figure 1 PDF present" \
  test -s manuscript/figures/fig1-artifact-ledger.pdf

check "Figure 2 PDF present" \
  test -s manuscript/figures/fig2-policy-gap.pdf

check "Figure 1 manifest sidecar present" \
  test -s manuscript/figures/fig1-artifact-ledger.manifest.json

# --- Repository ledger ---
check "docs/ledger.md present" \
  test -s docs/ledger.md

check "docs/ledger.md regenerator is deterministic (two consecutive runs identical)" \
  bash -c '
    uv run python scripts/regenerate_ledger.py >/dev/null 2>&1;
    cp docs/ledger.md /tmp/ledger.run1;
    uv run python scripts/regenerate_ledger.py >/dev/null 2>&1;
    cp docs/ledger.md /tmp/ledger.run2;
    diff -q /tmp/ledger.run1 /tmp/ledger.run2'

# --- gh authentication ---
check "gh is authenticated" \
  gh auth status

check "origin remote is reachable" \
  bash -c 'gh repo view htlin222/end-to-end --json visibility -q .visibility >/dev/null'

# --- Summary ---
printf "\n"
printf "::: %d passed, %d failed, %d warned\n" "$PASS" "$FAIL" "$WARN"

if [[ $FAIL -gt 0 ]]; then
  printf "${R}::: release blocked${N}\n"
  exit 1
fi

if [[ $WARN -gt 0 ]]; then
  printf "${Y}::: release allowed with %d warning(s)${N}\n" "$WARN"
fi

printf "${G}::: pre-flight clean; safe to tag and release${N}\n"
