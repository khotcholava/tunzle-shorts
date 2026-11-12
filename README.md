# Tunzle – daily Shorts pipeline

> **On Linux (Fedora)?** Use the [Linux setup](#linux-setup-fedora) right below – it's the current setup.
> The Windows / WSL2 instructions further down are kept for reference.

## Linux setup (Fedora)

Current machine: Fedora 44, RTX 3070, Ollama as a system service, models and this repo on the NVMe (`/mnt/nvme`).

1. **Tools**: `ffmpeg`, `git`, `python3` (Fedora ships all of them). Ollama: `curl -fsSL https://ollama.com/install.sh | sh`, then `ollama pull qwen3:8b`.
2. **Project**:
   ```bash
   git clone git@github.com:khotcholava/tunzle-shorts.git /mnt/nvme/tunzle/tunzle-shorts
   cd /mnt/nvme/tunzle/tunzle-shorts/tool
   python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
   ```
   Pushing uses your GitHub SSH key (`ssh -T git@github.com` should greet you as khotcholava).
3. **Test run** (renders, no upload): `../linux/run_daily.sh --date 2026-11-06 --no-push`, then check `videos/2026-11-06/` and `tool/daily.log`.
4. **Daily at 11:30 Tbilisi time** (systemd user timer, no sudo):
   ```bash
   /mnt/nvme/tunzle/tunzle-shorts/linux/install.sh
   ```
   * If the PC is off at 11:30, the job runs as soon as you log in (`Persistent=true`).
   * `install.sh` also runs `loginctl enable-linger $USER`, so the job runs even when you are not logged in.
   * If a batch for tomorrow is already on `main` (e.g. made by the cloud fallback), the job just exits.
   * The job refuses to push unless the repo is on `main` (the schedule's video URLs point at `main`).

| Want to… | Run |
|---|---|
| See when it runs next / last run | `systemctl --user list-timers tunzle-daily.timer` |
| Run today's job now | `systemctl --user start tunzle-daily.service` |
| Read the log | `tail -50 /mnt/nvme/tunzle/tunzle-shorts/tool/daily.log` |
| Turn it off | `systemctl --user disable --now tunzle-daily.timer` |

Qwen (via Ollama) writes each title + hook. It gets up to 3 tries (`ollama_retries` in `config.json`) before a built-in title is used.

---

> **Running it with Hermes Agent + Ollama instead of Claude?** Follow [hermes/HERMES_SETUP.md](hermes/HERMES_SETUP.md) (WSL2) instead of the Windows setup below. On Linux, skip the WSL2 steps – Ollama is on `localhost` already.

Your PC makes the videos; Claude only schedules them in Metricool.

```
11:30  Windows PC  → renders tomorrow's 5 Shorts, Qwen writes titles, pushes videos/ + schedule/ to GitHub
12:36  Claude task → reads schedule/<tomorrow>.json and schedules the 5 posts in Metricool (16:00, 18:00, 21:00, 00:00, 03:00)
```

## Folder layout

| Path | What it is |
|---|---|
| `tool/daily.py` | The daily job |
| `tool/render.py` | Video renderer (marble staircase, bright Tunzle style) |
| `tool/melodies.py` | Melody library – note strings for every melody (all public domain) |
| `tool/calendar.csv` | Which melody/format/level goes in each slot, Nov 5–30 |
| `tool/make_calendar.py` | Regenerates `calendar.csv` (edit it to plan December) |
| `tool/config.json` | Settings (Ollama model, timezone, repo) |
| `videos/<date>/` | Rendered Shorts (Metricool downloads them from here) |
| `schedule/<date>.json` | Titles, descriptions and post times for that batch |

## One-time setup on Windows (≈20 min)

1. **Install the tools** (PowerShell):
   ```powershell
   winget install Python.Python.3.12
   winget install Git.Git
   winget install Gyan.FFmpeg
   ```
   Close and reopen PowerShell afterwards so `python`, `git` and `ffmpeg` are on your PATH.
2. **Ollama model** – pick a Qwen model of about 7–8B (fits fully on the RTX 3070's 8 GB):
   ```powershell
   ollama pull qwen3:8b
   ```
   If that tag doesn't exist, pick the newest 7–8B Qwen from the Ollama library and put its name in `tool/config.json` → `ollama_model`.
3. **Get the project**:
   ```powershell
   cd C:\
   git clone https://github.com/khotcholava/tunzle-shorts
   cd C:\tunzle-shorts\tool
   python -m pip install -r requirements.txt
   ```
4. **Test run** (renders, no upload):
   ```powershell
   python daily.py --date 2026-11-06 --no-push
   ```
   Check `C:\tunzle-shorts\videos\2026-11-06\` – play a video, confirm the melody sounds right.
   Then run it for real once (the first push opens a GitHub sign-in window – sign in as khotcholava):
   ```powershell
   python daily.py --date 2026-11-06
   ```
5. **Run it automatically every day at 11:30**:
   ```powershell
   schtasks /Create /TN "Tunzle daily" /TR "C:\tunzle-shorts\tool\run_daily.bat" /SC DAILY /ST 11:30
   ```
   The PC must be on (or wake) at 11:30. Logs go to `tool\daily.log`. Missed a day? Run `python daily.py` before 12:30.

## Everyday commands

| Want to… | Run |
|---|---|
| Make tomorrow's batch now | `python daily.py` |
| Make a specific day | `python daily.py --date 2026-11-12` |
| Re-render a day (after editing a melody) | `python daily.py --date 2026-11-12 --force` |
| Test without Qwen / without uploading | `--no-ollama` / `--no-push` |

## Notes

* **Qwen only writes titles + the hook line.** If Ollama is off, or Qwen's title is too long or gives away the answer, a safe built-in title is used instead – the job never fails because of Qwen.
* **Melodies marked `check=True`** in `melodies.py` are ones worth a quick listen before they go out.
* **Adding melodies**: copy an entry in `melodies.py`, write the notes (`E4/1 D#4/.5 R/1 …`), then run `python make_calendar.py`. Only use music that is public domain (composer died 70+ years ago).
* All Shorts post as public, *not made for kids*, category Entertainment.

## YouTube uploader (replaces Metricool)

`tool/youtube_upload.py` uploads every Short in `schedule/*.json` straight to YouTube. Upcoming posts go up as
private with a publish time, so YouTube makes them public on schedule. Overdue posts are published right away.
What's been uploaded is tracked in `schedule/uploaded.json`, so nothing goes up twice.
It runs in GitHub Actions (`.github/workflows/youtube-upload.yml`) whenever a new batch is pushed to `main`, and once
a day at 13:17 Tbilisi time to pick up anything left over. The PC doesn't need to be on.

**One-time setup**

1. In [Google Cloud Console](https://console.cloud.google.com/), create a project and enable **YouTube Data API v3**.
2. **OAuth consent screen**: External, add your Google account as a test user, then press **Publish app**
   (in "Testing" mode the token stops working after 7 days). The "unverified app" warning on sign-in is fine for your own use.
3. **Credentials → Create credentials → OAuth client ID → Desktop app**. Copy the client ID and secret.
4. On the PC: `cd tool && .venv/bin/python youtube_auth.py CLIENT_ID CLIENT_SECRET`, sign in with the account that owns
   @tunzlequiz, and copy the printed refresh token.
5. GitHub → repo **Settings → Secrets and variables → Actions**: add `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`.
6. **Actions → Upload Shorts to YouTube → Run workflow** to test.
7. Fill in the [YouTube API audit form](https://support.google.com/youtube/contact/yt_api_form). Until the project
   passes it, YouTube locks API uploads to **private**, so the videos won't go public on their own.

**Limits**: one upload costs 1600 of the default 10,000 daily quota units, so about 6 uploads a day. The 5-a-day batch
fits; an overdue backlog drains at about 1 a day.

| Want to… | Run |
|---|---|
| See what would be uploaded | `python tool/youtube_upload.py --dry-run` |
| Mark posts as done (you uploaded them by hand) | `python tool/youtube_upload.py --mark-done 2026-11-12T16:00` then commit `schedule/uploaded.json` |
| Skip the backlog | `python tool/youtube_upload.py --since 2026-11-13` |
