const config = {
  appId: 'com.mobilecorner.app',
  appName: 'Mobile Corner',
  webDir: 'www',
  server: {
    androidScheme: 'https',
    iosScheme: 'https',
    cleartext: false,
    allowNavigation: [
      '*.mobilecorner.com',
      '*.vercel.app',
      'future-store-one.vercel.app',
      'https://future-store-one.vercel.app',
      'https://*.vercel.app',
      'localhost:*',
      '127.0.0.1:*'
    ]
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 3000,
      launchAutoHide: true,
      backgroundColor: "#000000",
      androidSplashResourceName: "splash",
      androidScaleType: "CENTER_CROP",
      showSpinner: true,
      androidSpinnerStyle: "large",
      iosSpinnerStyle: "small",
      spinnerColor: "#ffffff",
      splashFullScreen: true,
      splashImmersive: true,
      layoutName: "launch_screen",
      useDialog: true,
    },
    StatusBar: {
      style: 'dark',
      backgroundColor: '#000000',
      overlaysWebView: false,
    },
    Keyboard: {
      resize: 'body',
      style: 'dark',
      resizeOnFullScreen: true,
    },
    App: {
      urlOpen: {
        appId: 'com.mobilecorner.app',
        appName: 'Mobile Corner',
      },
    },
    PushNotifications: {
      presentationOptions: ["badge", "sound", "alert"],
    },
    LocalNotifications: {
      smallIcon: "ic_stat_icon_config_sample",
      iconColor: "#488AFF",
      sound: "beep.wav",
    },
    Camera: {
      permissions: ['camera', 'photos'],
    },
    Geolocation: {
      permissions: ['location'],
    },
    Network: {
      networkStatus: true,
    },
    Device: {
      deviceInfo: true,
    },
    Haptics: {
      hapticsImpact: true,
    },
    Browser: {
      url: 'https://mobilecorner.com',
    },
    Share: {
      shareOptions: ['email', 'sms', 'social'],
    },
    ActionSheet: {
      title: 'Mobile Corner',
      message: 'Choose an action',
    },
    Toast: {
      duration: 'short',
      position: 'bottom',
    },
    Dialog: {
      title: 'Mobile Corner',
      message: 'Welcome to Mobile Corner!',
    },
    Preferences: {
      storage: 'local',
    },
  },
  ios: {
    contentInset: 'always',
    backgroundColor: '#000000',
    scheme: 'mobilecorner',
    limitsNavigationsToAppBoundDomains: false,
    webView: {
      allowsBackForwardNavigationGestures: true,
      allowsLinkPreview: true,
    },
  },
  android: {
    backgroundColor: '#000000',
    allowMixedContent: true,
    captureInput: true,
    webContentsDebuggingEnabled: true,
    initialFocus: false,
    mixedContentMode: 'compatibility',
    overridesUserAgent: false,
    appendUserAgent: 'Mobile Corner App',
    allowNavigation: [
      '*.mobilecorner.com',
      '*.vercel.app',
      'future-store-one.vercel.app',
      'https://future-store-one.vercel.app',
      'https://*.vercel.app',
      'localhost:*',
      '127.0.0.1:*'
    ],
  },
};

module.exports = config; 