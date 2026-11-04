#!/usr/bin/env bash
# Installs the Tunzle daily timer for the current user (no sudo needed).
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
chmod +x "$REPO/linux/run_daily.sh"
mkdir -p "$HOME/.config/systemd/user"
sed "s|@REPO@|$REPO|g" "$REPO/linux/tunzle-daily.service" > "$HOME/.config/systemd/user/tunzle-daily.service"
cp "$REPO/linux/tunzle-daily.timer" "$HOME/.config/systemd/user/"
systemctl --user daemon-reload
systemctl --user enable --now tunzle-daily.timer
systemctl --user list-timers tunzle-daily.timer --no-pager
