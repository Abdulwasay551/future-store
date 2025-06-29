#!/bin/bash

# Mobile Corner - Mobile App Setup Script
# This script sets up Capacitor for converting your Django web app to mobile

echo "🚀 Setting up Mobile Corner Mobile App..."
echo "=========================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Download from: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js and npm are installed"
echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

# Initialize Capacitor
echo ""
echo "🔧 Initializing Capacitor..."
npx cap init "Mobile Corner" "com.mobilecorner.app" --web-dir=www

# Add Android platform
echo ""
echo "🤖 Adding Android platform..."
npx cap add android

# Add iOS platform (only on macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo "🍎 Adding iOS platform..."
    npx cap add ios
else
    echo ""
    echo "⚠️  Skipping iOS platform (macOS required)"
fi

# Sync the project
echo ""
echo "🔄 Syncing project..."
npx cap sync

# Generate icons and splash screens
echo ""
echo "🎨 Generating app icons and splash screens..."
npx cordova-res android --skip-config --copy
if [[ "$OSTYPE" == "darwin"* ]]; then
    npx cordova-res ios --skip-config --copy
fi

# Copy Django static files to www directory
echo ""
echo "📁 Copying Django static files..."
mkdir -p www/static
cp -r static/* www/static/ 2>/dev/null || echo "⚠️  No static files found to copy"

# Create assets directory structure
echo ""
echo "📂 Creating assets directory structure..."
mkdir -p www/assets/icon
mkdir -p www/assets/splash

# Copy logo to assets
if [ -f "static/logo-light.JPG" ]; then
    echo "📸 Copying logo to assets..."
    cp static/logo-light.JPG www/assets/icon/icon-192x192.png
    cp static/logo-light.JPG www/assets/icon/icon-512x512.png
fi

# Update the iframe URL in index.html
echo ""
echo "🔗 Updating app URL..."
read -p "Enter your Django app URL (e.g., https://your-app.vercel.app): " APP_URL

if [ ! -z "$APP_URL" ]; then
    # Replace the placeholder URL in index.html
    sed -i.bak "s|https://your-django-app-url.vercel.app|$APP_URL|g" www/index.html
    echo "✅ Updated app URL to: $APP_URL"
else
    echo "⚠️  Please manually update the URL in www/index.html"
fi

# Create .gitignore for mobile-specific files
echo ""
echo "📝 Creating .gitignore for mobile files..."
cat >> .gitignore << EOF

# Mobile App Files
android/
ios/
www/assets/
www/capacitor.js
node_modules/
package-lock.json
EOF

echo ""
echo "🎉 Mobile app setup completed!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Update your Django app URL in www/index.html"
echo "2. Replace placeholder images in resources/ with your actual assets"
echo "3. Run 'npm run build:android' to build for Android"
echo "4. Run 'npm run open:android' to open in Android Studio"
echo ""
echo "For iOS (macOS only):"
echo "1. Run 'npm run build:ios' to build for iOS"
echo "2. Run 'npm run open:ios' to open in Xcode"
echo ""
echo "For development:"
echo "1. Run 'npm run serve' to serve the app locally"
echo "2. Run 'npm run preview' to preview on device"
echo ""
echo "Happy coding! 🚀" 