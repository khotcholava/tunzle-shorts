@echo off
REM Tunzle daily job - renders tomorrow's 5 Shorts, writes titles with Qwen, pushes to GitHub.
cd /d "%~dp0"
echo ===== %date% %time% ===== >> daily.log
python daily.py >> daily.log 2>&1
