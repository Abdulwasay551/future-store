# 🚀 Quick Start - Mobile Corner Mobile App

Get your Django web app running as a mobile app in 5 minutes!

## Prerequisites

1. **Node.js** (v16+) - [Download here](https://nodejs.org/)
2. **Android Studio** (for Android) - [Download here](https://developer.android.com/studio)
3. **Xcode** (for iOS, macOS only) - [Download here](https://developer.apple.com/xcode/)

## ⚡ Quick Setup

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
setup_mobile.bat
```

**macOS/Linux:**
```bash
chmod +x setup_mobile.sh
./setup_mobile.sh
```

### Option 2: Python Script

```bash
python build_mobile.py --full --url "https://your-django-app.vercel.app"
```

### Option 3: Manual Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Initialize Capacitor:**
   ```bash
   npx cap init "Mobile Corner" "com.mobilecorner.app" --web-dir=www
   ```

3. **Add platforms:**
   ```bash
   npx cap add android
   npx cap add ios  # macOS only
   ```

4. **Sync project:**
   ```bash
   npx cap sync
   ```

## 🔧 Configure Your App

1. **Update your Django app URL** in `www/index.html`:
   ```html
   <iframe src="https://your-actual-django-app.vercel.app" ...>
   ```

2. **Replace placeholder images** in `resources/` with your actual assets:
   - `resources/icon.png` (1024x1024)
   - `resources/splash.png` (2732x2732)
   - `resources/adaptive-icon.png` (1024x1024)

## 📱 Build & Test

### Android
```bash
# Build
npm run build:android

# Open in Android Studio
npm run open:android

# Run on device/emulator
npm run run:android
```

### iOS (macOS only)
```bash
# Build
npm run build:ios

# Open in Xcode
npm run open:ios

# Run on device/simulator
npm run run:ios
```

### Local Testing
```bash
# Serve locally
npm run serve

# Preview on device
npm run preview
```

## 🎯 Common Commands

```bash
# Sync changes
npm run sync

# Build for both platforms
npm run build

# Clean project
npm run clean

# Update app URL
python build_mobile.py --url "https://your-new-url.com"
```

## 🔍 Troubleshooting

### "Command not found: cap"
```bash
npm install -g @capacitor/cli
```

### Android build fails
- Install Android SDK (API level 33+)
- Set ANDROID_HOME environment variable
- Update Android Build Tools

### iOS build fails (macOS)
```bash
sudo xcodebuild -license accept
```

### WebView not loading
- Check internet connection
- Verify Django app URL
- Check CORS settings

## 📚 Next Steps

1. **Customize your app** - Edit `capacitor.config.js`
2. **Add mobile features** - Use Capacitor plugins
3. **Optimize for mobile** - Add `static/css/mobile.css` to your Django templates
4. **Deploy to stores** - Follow platform-specific guidelines

## 🆘 Need Help?

- 📖 [Full Documentation](MOBILE_SETUP.md)
- 🔧 [Capacitor Docs](https://capacitorjs.com/docs)
- 💬 Check the troubleshooting section in `MOBILE_SETUP.md`

---

**Happy coding! 🚀** 