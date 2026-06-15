
@echo off
rem Automatic push helper — runs non-interactively using embedded Git identity
rem Run this from the repository folder: double-click or run in PowerShell/CMD

set GIT_EMAIL=sajjanyadav.witted@gmail.com
set GIT_NAME=sajjan001

git --version >nul 2>&1 || (
  echo Git not found on PATH. Install Git and re-run this script.
  pause
  exit /b 1
)

git rev-parse --is-inside-work-tree >nul 2>&1 || git init
git config user.email "%GIT_EMAIL%"
git config user.name "%GIT_NAME%"
git rm --cached .env 2>nul || rem ignore
git add .
git commit -m "fix: migrate SQLite to PostgreSQL for persistent storage on Render" 2>nul || echo No changes to commit
git branch -M main
git remote remove origin 2>nul || rem ignore
git remote add origin https://github.com/Sajjan001/auto_content_system.git 2>nul
git push -u origin main

echo Done. Press any key to close.
pause >nul
