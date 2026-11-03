# Run Tunzle on your PC with Hermes Agent + Ollama (no Claude needed)

```
11:30  Hermes cron (script job)  → python3 daily.py: renders tomorrow's 5 Shorts, Qwen writes titles, git push
12:15  Hermes cron (agent job)   → Qwen + Metricool MCP: schedules the 5 posts (16:00, 18:00, 21:00, 00:00, 03:00)
12:38  Claude task (safety net)  → skips posts that are already scheduled; turn it off once Hermes works 3 days in a row
```

Hermes Agent does not run on native Windows — everything below runs **inside WSL2 (Ubuntu)**.
Ollama stays on Windows (it uses your RTX 3070).

---

## 1. WSL2 + Ubuntu (PowerShell as Administrator)

```powershell
wsl --install -d Ubuntu
```
Reboot if asked, open **Ubuntu** from the Start menu, create a username/password.

**Let WSL reach Ollama on Windows** – create `C:\Users\<you>\.wslconfig` with:
```ini
[wsl2]
networkingMode=mirrored
```
then in PowerShell: `wsl --shutdown` and reopen Ubuntu.
(Windows 10 / no mirrored mode? Instead set the Windows env var `OLLAMA_HOST=0.0.0.0`, restart Ollama,
and in step 4 use `http://$(ip route show | grep default | awk '{print $3}'):11434` instead of localhost.)

Test from Ubuntu: `curl http://localhost:11434/api/tags` → should list your models.

## 2. Ollama model (PowerShell on Windows)

Agents need a long context. Make a 16K-context copy of Qwen (fits the 3070's 8 GB):
```powershell
ollama pull qwen3:8b
"FROM qwen3:8b`nPARAMETER num_ctx 16384" | Out-File -Encoding ascii Modelfile
ollama create qwen3-8b-16k -f Modelfile
```
(If Hermes complains the context is too small, use `num_ctx 32768` – it will run a bit slower.)

## 3. Project + tools (Ubuntu)

```bash
sudo apt update && sudo apt install -y git python3-pip python3-venv ffmpeg
git clone https://github.com/khotcholava/tunzle-shorts ~/tunzle-shorts
cd ~/tunzle-shorts/tool
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
git config --global user.name "khotcholava"
git config --global user.email "<your GitHub email>"
```
GitHub login for pushing: create a token at github.com → Settings → Developer settings → Fine-grained token
(only repo *tunzle-shorts*, permission *Contents: Read and write*), then:
```bash
git config --global credential.helper store
cd ~/tunzle-shorts && git push   # username: khotcholava, password: paste the token (saved after this once)
```
Set the model in `tool/config.json`: `"ollama_model": "qwen3-8b-16k"`.

**Test the video job (no AI agent involved yet):**
```bash
cd ~/tunzle-shorts/tool
.venv/bin/python daily.py --date 2026-11-06 --no-push
```
Open `\\wsl$\Ubuntu\home\<you>\tunzle-shorts\videos\2026-11-06` in Windows Explorer and play the videos.
Look at `schedule/2026-11-06.json` → the titles there were written by Qwen (if Ollama was reachable).

## 4. Hermes Agent (Ubuntu)

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc
hermes model
```
Choose **Custom OpenAI-compatible endpoint** → Base URL `http://localhost:11434/v1`, API key `ollama`,
model `qwen3-8b-16k`.

Chat test: run `hermes` and ask "list the files in ~/tunzle-shorts/schedule". If it answers correctly, tool calling works.

## 5. Connect Metricool to Hermes

```bash
hermes mcp add metricool --url https://ai.metricool.com/mcp
hermes mcp test metricool
```
A browser login should open – sign in to Metricool and allow access (works on the free plan).
In `hermes`, ask: "use metricool getBrandSettings" → you should see brand id 7843998.

> If Hermes can't do the Metricool login (no browser window / auth error): keep the Claude task for
> the scheduling step – it's ~5 tool calls a day. Everything else still runs on your PC.

## 6. Install the skill and the two daily jobs

```bash
mkdir -p ~/.hermes/skills && cp -r ~/tunzle-shorts/hermes/tunzle-scheduler ~/.hermes/skills/
chmod +x ~/tunzle-shorts/hermes/make_batch.sh
hermes cron create "30 11 * * *" "Run ~/tunzle-shorts/hermes/make_batch.sh in the terminal and report the last 10 lines of output." --name "Tunzle make batch" --workdir $HOME/tunzle-shorts
hermes cron create "15 12 * * *" "Schedule tomorrow's Tunzle Shorts." --skill tunzle-scheduler --name "Tunzle schedule" --workdir $HOME/tunzle-shorts
hermes gateway install      # keeps Hermes running in the background (cron needs the gateway)
hermes cron list
```
Times are your PC's clock – check `date` in Ubuntu shows Tbilisi time (`sudo timedatectl set-timezone Asia/Tbilisi` if not).

**Test both jobs now** (it's safe – the duplicate check prevents double posts):
```bash
hermes cron run <id of "Tunzle make batch">
hermes cron run <id of "Tunzle schedule">
```
Results land in `~/.hermes/cron/output/`. Check https://app.metricool.com planner that the posts appear.

## 7. Switch Claude off

After 3 days where the 12:15 Hermes job scheduled all 5 posts (Claude's 12:38 run will then report
"already scheduled, skipped"), tell Claude: **"pause the Tunzle daily scheduling task"**.

## Troubleshooting

| Problem | Fix |
|---|---|
| `curl localhost:11434` fails in Ubuntu | `.wslconfig` mirrored mode + `wsl --shutdown`, or the OLLAMA_HOST route above |
| Hermes prints JSON instead of calling tools | Use a model with tool calling (qwen3, hermes3) and the `/v1` endpoint |
| Context / truncation errors | Rebuild the model with `num_ctx 32768` |
| Cron didn't fire | PC asleep or gateway stopped → `hermes gateway start`, then `hermes cron run <id>` |
| Videos missing on GitHub | `cd ~/tunzle-shorts/tool && .venv/bin/python daily.py` and read the error |
