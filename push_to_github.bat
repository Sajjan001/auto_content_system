@echo off
git config user.email "sajjanyadav.witted@gmail.com"
git config user.name "sajjan001"
git rm --cached .env 2>nul
git add .
git commit -m "update" 2>nul || echo Nothing to commit
git push origin main
pause >nul
