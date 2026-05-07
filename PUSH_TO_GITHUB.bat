@echo off
echo ========================================
echo GitHub Push Script
echo ========================================
echo.

echo Step 1: Initializing Git repository...
git init
echo.

echo Step 2: Adding files to Git...
git add .
echo.

echo Step 3: Creating initial commit...
git commit -m "Initial commit: GenTrack GPD Reporting System v2 - Complete system with e-signature functionality"
echo.

echo Step 4: Adding remote repository...
git remote add origin https://github.com/artchellapuz-commits/GenTrack_GPD_Reporting_System_v2.git
echo.

echo Step 5: Renaming branch to main...
git branch -M main
echo.

echo Step 6: Pushing to GitHub...
echo.
echo ⚠️  You will be prompted for your GitHub credentials:
echo    Username: artchellapuz-commits
echo    Password: [Use your Personal Access Token, NOT your GitHub password]
echo.
echo If you don't have a token, create one at:
echo https://github.com/settings/tokens
echo.
pause

git push -u origin main

echo.
echo ========================================
echo Done! Check your repository at:
echo https://github.com/artchellapuz-commits/GenTrack_GPD_Reporting_System_v2
echo ========================================
pause
