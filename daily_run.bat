@echo off
REM Daily Article Generator - Windows Scheduled Task Runner
REM Runs daily at 06:00 AM to generate fresh travel content
cd /d "C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"

echo [%date% %time%] ========================================
echo [%date% %time%] Starting Daily Article Generator
echo [%date% %time%] ========================================

REM Step 1: Generate new articles
echo.
echo [Step 1/4] Generating articles...
python daily_generator_v3.py
if errorlevel 1 (
    echo ERROR: Article generation failed!
    goto :error
)

REM Step 2: Update sitemap
echo.
echo [Step 2/4] Updating sitemap...
python update_sitemap.py

REM Step 3: Build dist for deployment
echo.
echo [Step 3/4] Building deployment package...
if exist dist rmdir /s /q dist
mkdir dist
mkdir dist\articles
mkdir dist\assets

copy index.html dist\
copy sitemap.xml dist\
copy robots.txt dist\
copy .nojekyll dist\
copy googlea89fd78636d38c3a.html dist\ 2>nul
xcopy /E /I /Y articles\* dist\articles\
xcopy /E /I /Y assets\* dist\assets\

REM Step 4: Deploy to Cloudflare Pages
echo.
echo [Step 4/4] Deploying to Cloudflare Pages...
set CLOUDFLARE_API_TOKEN=ENV_CF_TOKEN
npx wrangler pages deploy dist --project-name travel-guide-esimart --branch main --commit-dirty=true
if errorlevel 1 (
    echo ERROR: Deployment failed!
    goto :error
)

REM Commit and push
git add -A
git commit -m "daily: %date% %time% - articles generated" 2>nul
git push origin main 2>nul

echo.
echo [%date% %time%] ========================================
echo [%date% %time%] Daily generation complete!
echo [%date% %time%] Site: https://travel-guide-esimart.pages.dev/
echo [%date% %time%] ========================================
goto :end

:error
echo.
echo [%date% %time%] ERROR occurred. Check logs above.

:end
pause

