@echo off
REM Mobile Corner - Mobile App Setup Script (Windows)
REM This script sets up Capacitor for converting your Django web app to mobile

echo 🚀 Setting up Mobile Corner Mobile App...
echo ==========================================

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    echo    Download from: https://nodejs.org/
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not installed. Please install npm first.
    pause
    exit /b 1
)

echo ✅ Node.js and npm are installed
for /f "tokens=*" %%i in ('node --version') do echo Node.js version: %%i
for /f "tokens=*" %%i in ('npm --version') do echo npm version: %%i

REM Install dependencies
echo.
echo 📦 Installing dependencies...
call npm install

REM Initialize Capacitor
echo.
echo 🔧 Initializing Capacitor...
call npx cap init "Mobile Corner" "com.mobilecorner.app" --web-dir=www

REM Add Android platform
echo.
echo 🤖 Adding Android platform...
call npx cap add android

REM Sync the project
echo.
echo 🔄 Syncing project...
call npx cap sync

REM Generate icons and splash screens
echo.
echo 🎨 Generating app icons and splash screens...
call npx cordova-res android --skip-config --copy

REM Copy Django static files to www directory
echo.
echo 📁 Copying Django static files...
if not exist "www\static" mkdir www\static
if exist "static" xcopy /E /I /Y static www\static >nul 2>&1

REM Create assets directory structure
echo.
echo 📂 Creating assets directory structure...
if not exist "www\assets\icon" mkdir www\assets\icon
if not exist "www\assets\splash" mkdir www\assets\splash

REM Copy logo to assets
if exist "static\logo-light.JPG" (
    echo 📸 Copying logo to assets...
    copy "static\logo-light.JPG" "www\assets\icon\icon-192x192.png" >nul
    copy "static\logo-light.JPG" "www\assets\icon\icon-512x512.png" >nul
)

REM Update the iframe URL in index.html
echo.
echo 🔗 Updating app URL...
set /p APP_URL="Enter your Django app URL (e.g., https://your-app.vercel.app): "

if not "%APP_URL%"=="" (
    REM Replace the placeholder URL in index.html
    powershell -Command "(Get-Content 'www\index.html') -replace 'https://your-django-app-url.vercel.app', '%APP_URL%' | Set-Content 'www\index.html'"
    echo ✅ Updated app URL to: %APP_URL%
) else (
    echo ⚠️  Please manually update the URL in www\index.html
)

REM Create .gitignore for mobile-specific files
echo.
echo 📝 Creating .gitignore for mobile files...
echo. >> .gitignore
echo # Mobile App Files >> .gitignore
echo android/ >> .gitignore
echo ios/ >> .gitignore
echo www/assets/ >> .gitignore
echo www/capacitor.js >> .gitignore
echo node_modules/ >> .gitignore
echo package-lock.json >> .gitignore

echo.
echo 🎉 Mobile app setup completed!
echo ==========================================
echo.
echo Next steps:
echo 1. Update your Django app URL in www\index.html
echo 2. Replace placeholder images in resources\ with your actual assets
echo 3. Run 'npm run build:android' to build for Android
echo 4. Run 'npm run open:android' to open in Android Studio
echo.
echo For development:
echo 1. Run 'npm run serve' to serve the app locally
echo 2. Run 'npm run preview' to preview on device
echo.
echo Happy coding! 🚀
pause 