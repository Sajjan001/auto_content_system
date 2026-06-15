@echo off
set GIT_EMAIL=sajjanyadav.witted@gmail.com
set GIT_NAME=sajjan001

git config user.email "%GIT_EMAIL%"
git config user.name "%GIT_NAME%"
git rm --cached .env 2>nul
git add .
git commit -m "updated db to use postgres on render" 2>nul || echo nothing to commit
git push origin main

pause >nul
