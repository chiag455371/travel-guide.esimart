@echo off
REM Daily article generator - runs daily at scheduled time
cd /d "C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"

REM Generate new articles
python daily_articles.py

REM Update sitemap
python update_sitemap.py

REM Commit and push
git add -A
git commit -m "daily articles %date% %time%"
git push origin main

echo Done at %date% %time%
