#!/usr/bin/env python3
"""
Mobile Corner - Release Build Script
This script helps build release versions of your mobile app
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class ReleaseBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.android_dir = self.project_root / "android"
        self.ios_dir = self.project_root / "ios"
        
    def check_prerequisites(self):
        """Check if all required tools are installed"""
        print("🔍 Checking prerequisites...")
        
        # Check if platforms exist
        if not self.android_dir.exists():
            print("❌ Android platform not found. Run 'npx cap add android' first.")
            return False
            
        if sys.platform == "darwin" and not self.ios_dir.exists():
            print("⚠️ iOS platform not found. Run 'npx cap add ios' first.")
        
        return True
    
    def sync_project(self):
        """Sync the Capacitor project"""
        print("🔄 Syncing project...")
        
        try:
            subprocess.run(['npx', 'cap', 'sync'], cwd=self.project_root, check=True)
            print("✅ Project synced")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to sync project: {e}")
            return False
    
    def build_android_debug(self):
        """Build Android debug APK"""
        print("🤖 Building Android debug APK...")
        
        try:
            # Sync first
            subprocess.run(['npx', 'cap', 'sync'], cwd=self.project_root, check=True)
            
            # Build debug APK
            subprocess.run(['npx', 'cap', 'build', 'android'], cwd=self.project_root, check=True)
            
            print("✅ Android debug APK built successfully")
            print("📱 APK location: android/app/build/outputs/apk/debug/app-debug.apk")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build Android APK: {e}")
            return False
    
    def build_android_release(self):
        """Build Android release APK"""
        print("🤖 Building Android release APK...")
        
        try:
            # Sync first
            subprocess.run(['npx', 'cap', 'sync'], cwd=self.project_root, check=True)
            
            # Build release APK
            subprocess.run(['npx', 'cap', 'build', 'android'], cwd=self.project_root, check=True)
            
            # Generate release APK
            subprocess.run(['./gradlew', 'assembleRelease'], cwd=self.android_dir, check=True)
            
            print("✅ Android release APK built successfully")
            print("📱 APK location: android/app/build/outputs/apk/release/app-release.apk")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build Android release APK: {e}")
            return False
    
    def build_android_bundle(self):
        """Build Android App Bundle (for Play Store)"""
        print("🤖 Building Android App Bundle...")
        
        try:
            # Sync first
            subprocess.run(['npx', 'cap', 'sync'], cwd=self.project_root, check=True)
            
            # Build release bundle
            subprocess.run(['./gradlew', 'bundleRelease'], cwd=self.android_dir, check=True)
            
            print("✅ Android App Bundle built successfully")
            print("📦 Bundle location: android/app/build/outputs/bundle/release/app-release.aab")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build Android bundle: {e}")
            return False
    
    def build_ios(self):
        """Build iOS app (macOS only)"""
        if sys.platform != "darwin":
            print("⚠️ iOS builds are only supported on macOS")
            return False
        
        print("🍎 Building iOS app...")
        
        try:
            # Sync first
            subprocess.run(['npx', 'cap', 'sync'], cwd=self.project_root, check=True)
            
            # Build iOS
            subprocess.run(['npx', 'cap', 'build', 'ios'], cwd=self.project_root, check=True)
            
            print("✅ iOS app built successfully")
            print("🍎 Open Xcode to archive and distribute:")
            print("   npm run open:ios")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build iOS app: {e}")
            return False
    
    def copy_apk_to_desktop(self):
        """Copy APK to desktop for easy access"""
        try:
            apk_source = self.android_dir / "app" / "build" / "outputs" / "apk" / "release" / "app-release.apk"
            desktop = Path.home() / "Desktop"
            apk_dest = desktop / "MobileCorner.apk"
            
            if apk_source.exists():
                shutil.copy2(apk_source, apk_dest)
                print(f"✅ APK copied to Desktop: {apk_dest}")
                return True
            else:
                print("❌ APK not found. Build the release APK first.")
                return False
        except Exception as e:
            print(f"❌ Failed to copy APK: {e}")
            return False
    
    def show_distribution_guide(self):
        """Show distribution guide"""
        print("\n" + "="*60)
        print("📱 MOBILE APP DISTRIBUTION GUIDE")
        print("="*60)
        
        print("\n🔧 ANDROID DISTRIBUTION:")
        print("1. Debug APK (for testing):")
        print("   - Location: android/app/build/outputs/apk/debug/app-debug.apk")
        print("   - Share directly with users")
        print("   - Users enable 'Install from unknown sources'")
        
        print("\n2. Release APK (for direct distribution):")
        print("   - Location: android/app/build/outputs/apk/release/app-release.apk")
        print("   - Upload to Google Drive, Dropbox, or your website")
        print("   - Users download and install")
        
        print("\n3. Google Play Store (recommended):")
        print("   - Create Google Play Developer account ($25)")
        print("   - Upload AAB file to Google Play Console")
        print("   - Users download from Play Store")
        
        if sys.platform == "darwin":
            print("\n🍎 IOS DISTRIBUTION:")
            print("1. TestFlight (for testing):")
            print("   - Create Apple Developer account ($99/year)")
            print("   - Upload to TestFlight via Xcode")
            print("   - Invite users to test")
            
            print("\n2. App Store (for public release):")
            print("   - Archive app in Xcode")
            print("   - Upload to App Store Connect")
            print("   - Submit for review")
            print("   - Users download from App Store")
        
        print("\n🚀 QUICK START:")
        print("1. For testing: python build_release.py --android-debug")
        print("2. For direct distribution: python build_release.py --android-release")
        print("3. For Play Store: python build_release.py --android-bundle")
        if sys.platform == "darwin":
            print("4. For iOS: python build_release.py --ios")
        
        print("\n📞 SUPPORT:")
        print("- Android: https://developer.android.com/guide")
        print("- iOS: https://developer.apple.com/develop/")
        print("- Capacitor: https://capacitorjs.com/docs")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Mobile Corner Release Builder')
    parser.add_argument('--android-debug', action='store_true', help='Build Android debug APK')
    parser.add_argument('--android-release', action='store_true', help='Build Android release APK')
    parser.add_argument('--android-bundle', action='store_true', help='Build Android App Bundle')
    parser.add_argument('--ios', action='store_true', help='Build iOS app')
    parser.add_argument('--copy-apk', action='store_true', help='Copy APK to desktop')
    parser.add_argument('--guide', action='store_true', help='Show distribution guide')
    
    args = parser.parse_args()
    
    builder = ReleaseBuilder()
    
    if args.guide:
        builder.show_distribution_guide()
        return
    
    if not builder.check_prerequisites():
        return
    
    if args.android_debug:
        builder.build_android_debug()
    elif args.android_release:
        builder.build_android_release()
    elif args.android_bundle:
        builder.build_android_bundle()
    elif args.ios:
        builder.build_ios()
    elif args.copy_apk:
        builder.copy_apk_to_desktop()
    else:
        # Default: show guide
        builder.show_distribution_guide()

if __name__ == "__main__":
    main() 