#!/usr/bin/env bash
# Renders tomorrow's Tunzle batch, gets titles from Qwen, pushes to GitHub.
set -e
cd "$HOME/tunzle-shorts/tool"
PY=".venv/bin/python"; [ -x "$PY" ] || PY=python3
"$PY" daily.py "$@" 2>&1 | tee -a daily.log
