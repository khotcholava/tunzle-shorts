#!/usr/bin/env bash
# Tunzle daily job for Linux: renders tomorrow's 5 Shorts, Qwen writes titles, pushes to GitHub.
# Called by the tunzle-daily systemd timer; also fine to run by hand. Extra args go to daily.py.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO/tool"
exec >> daily.log 2>&1
echo "===== $(date '+%F %T') ====="

# video_url in the schedule always points at the main branch on GitHub, so batches must be pushed from main.
branch="$(git -C "$REPO" rev-parse --abbrev-ref HEAD)"
if [ "$branch" != "main" ] && [[ " $* " != *" --no-push "* ]]; then
  echo "ERROR: repo is on branch '$branch', not main — not pushing. Run: git -C $REPO switch main"
  exit 1
fi

[ -x .venv/bin/python ] || { python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt; }
.venv/bin/python daily.py "$@"
