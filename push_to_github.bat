@echo off
rem Helper to initialize, commit, set remote, and push to GitHub
rem Run this from the repository folder: double-click or run in PowerShell/CMD

if "%~1"=="" (
  set /p GIT_EMAIL=Enter git email: 
) else set GIT_EMAIL=%~1

if "%~2"=="" (
  set /p GIT_NAME=Enter git name: 
) else set GIT_NAME=%~2

git --version >nul 2>&1 || (
  echo Git not found on PATH. Install Git and re-run this script.
  pause
  exit /b 1
)

git rev-parse --is-inside-work-tree >nul 2>&1 || git init
git config user.email "%GIT_EMAIL%"
git config user.name "%GIT_NAME%"
git add .gitignore 2>nul
git add .
git commit -m "chore: initial commit" 2>nul || echo No changes to commit
git branch -M main
git remote remove origin 2>nul || rem ignore error
git remote add origin https://github.com/Sajjan001/auto_content_system.git
git push -u origin main

echo Done. Press any key to close.
pause >nul
