@echo off
REM Daily article generator - runs daily at scheduled time
cd /d "C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"

echo [%date% %time%] Starting daily article generation...

REM Generate new articles with verified images
python daily_generator_v2.py

REM Update sitemap
python update_sitemap.py

REM Commit and push
git add -A
git commit -m "daily: %date% %time% - articles generated with verified images" 2>&1
git push origin main

echo [%date% %time%] Done!
