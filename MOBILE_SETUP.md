# Mobile Corner - Mobile App Setup Guide

This guide will help you convert your Django web app into a native mobile app using Capacitor.

## 🚀 Quick Start

### Prerequisites

1. **Node.js** (v16 or higher)
   - Download from: https://nodejs.org/
   - Verify installation: `node --version`

2. **Android Studio** (for Android development)
   - Download from: https://developer.android.com/studio
   - Install Android SDK and build tools

3. **Xcode** (for iOS development - macOS only)
   - Download from: https://developer.apple.com/xcode/

### Automated Setup

#### Windows
```bash
setup_mobile.bat
```

#### macOS/Linux
```bash
chmod +x setup_mobile.sh
./setup_mobile.sh
```

### Manual Setup

If you prefer to set up manually, follow these steps:

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Initialize Capacitor**
   ```bash
   npx cap init "Mobile Corner" "com.mobilecorner.app" --web-dir=www
   ```

3. **Add platforms**
   ```bash
   npx cap add android
   npx cap add ios  # macOS only
   ```

4. **Sync project**
   ```bash
   npx cap sync
   ```

## 📱 App Configuration

### Update Your Django App URL

Edit `www/index.html` and replace the placeholder URL:
```html
<iframe 
    id="webview-container"
    src="https://your-actual-django-app.vercel.app"
    ...>
</iframe>
```

### App Icons and Splash Screens

Replace the placeholder files in `resources/` with your actual assets:

- `resources/icon.png` - 1024x1024 PNG (app icon)
- `resources/splash.png` - 2732x2732 PNG (splash screen)
- `resources/adaptive-icon.png` - 1024x1024 PNG (Android adaptive icon)

Generate all icon sizes:
```bash
npx cordova-res android --skip-config --copy
npx cordova-res ios --skip-config --copy  # macOS only
```

## 🛠️ Development

### Available Commands

```bash
# Build and sync
npm run sync

# Build for Android
npm run build:android

# Build for iOS (macOS only)
npm run build:ios

# Open in Android Studio
npm run open:android

# Open in Xcode (macOS only)
npm run open:ios

# Run on Android device/emulator
npm run run:android

# Run on iOS device/simulator (macOS only)
npm run run:ios

# Serve locally for testing
npm run serve

# Preview on device
npm run preview
```

### Development Workflow

1. **Make changes to your Django app**
2. **Deploy to your hosting platform** (Vercel, etc.)
3. **Update the URL in `www/index.html`** if needed
4. **Sync the mobile app**
   ```bash
   npm run sync
   ```
5. **Test on device/emulator**
   ```bash
   npm run run:android
   # or
   npm run run:ios
   ```

## 📋 Platform-Specific Setup

### Android

1. **Install Android Studio**
   - Download from: https://developer.android.com/studio
   - Install Android SDK (API level 33 or higher)
   - Install Android Build Tools

2. **Set up environment variables**
   ```bash
   export ANDROID_HOME=$HOME/Android/Sdk
   export PATH=$PATH:$ANDROID_HOME/tools
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   ```

3. **Build and run**
   ```bash
   npm run build:android
   npm run open:android
   ```

### iOS (macOS only)

1. **Install Xcode**
   - Download from: https://developer.apple.com/xcode/
   - Install iOS Simulator
   - Accept Xcode license: `sudo xcodebuild -license accept`

2. **Build and run**
   ```bash
   npm run build:ios
   npm run open:ios
   ```

## 🔧 Customization

### Capacitor Configuration

Edit `capacitor.config.js` to customize:
- App ID and name
- Server settings
- Plugin configurations
- Platform-specific settings

### Mobile-Specific Features

The app includes these Capacitor plugins:
- **App**: App lifecycle management
- **StatusBar**: Status bar customization
- **SplashScreen**: Custom splash screen
- **Keyboard**: Keyboard handling
- **Haptics**: Haptic feedback
- **Device**: Device information
- **Network**: Network status
- **Storage**: Local storage
- **Camera**: Camera access
- **Geolocation**: Location services
- **Notifications**: Push and local notifications
- **Browser**: In-app browser
- **Share**: Native sharing
- **Toast**: Native toast messages
- **Dialog**: Native dialogs

### Styling

Customize the mobile app appearance in `www/index.html`:
- Loading screen design
- Status bar styling
- Safe area handling
- WebView container styling

## 🚀 Deployment

### Android

1. **Build release APK**
   ```bash
   npm run build:android
   cd android
   ./gradlew assembleRelease
   ```

2. **Find APK**
   - Location: `android/app/build/outputs/apk/release/app-release.apk`

3. **Upload to Google Play Console**
   - Sign up for Google Play Developer account
   - Create app listing
   - Upload APK/AAB file

### iOS

1. **Build for App Store**
   ```bash
   npm run build:ios
   # Open Xcode and archive
   ```

2. **Upload to App Store Connect**
   - Sign up for Apple Developer account
   - Create app in App Store Connect
   - Upload build via Xcode

## 🔍 Troubleshooting

### Common Issues

1. **"Command not found: cap"**
   ```bash
   npm install -g @capacitor/cli
   ```

2. **Android build fails**
   - Check Android SDK installation
   - Verify ANDROID_HOME environment variable
   - Update Android Build Tools

3. **iOS build fails**
   - Check Xcode installation
   - Accept Xcode license
   - Install iOS Simulator

4. **WebView not loading**
   - Check internet connection
   - Verify Django app URL
   - Check CORS settings on Django app

5. **App crashes on startup**
   - Check Capacitor configuration
   - Verify plugin installations
   - Review console logs

### Debug Mode

Enable debug mode in `capacitor.config.js`:
```javascript
android: {
  webContentsDebuggingEnabled: true,
}
```

### Logs

View logs:
```bash
# Android
adb logcat | grep -i capacitor

# iOS
# Use Xcode console or Safari Web Inspector
```

## 📚 Resources

- [Capacitor Documentation](https://capacitorjs.com/docs)
- [Android Development Guide](https://developer.android.com/guide)
- [iOS Development Guide](https://developer.apple.com/develop/)
- [Django Deployment Guide](https://docs.djangoproject.com/en/stable/howto/deployment/)

## 🤝 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Capacitor documentation
3. Check your Django app logs
4. Verify platform-specific requirements

---

**Happy coding! 🚀** 