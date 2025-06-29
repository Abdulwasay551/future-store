#!/usr/bin/env python3
"""
Mobile Corner - Mobile App Build Script
This script helps build and prepare the mobile app for deployment
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path

class MobileAppBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.www_dir = self.project_root / "www"
        self.static_dir = self.project_root / "static"
        self.resources_dir = self.project_root / "resources"
        
    def check_prerequisites(self):
        """Check if all required tools are installed"""
        print("🔍 Checking prerequisites...")
        
        # Check Node.js
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Node.js: {result.stdout.strip()}")
            else:
                print("❌ Node.js not found")
                return False
        except FileNotFoundError:
            print("❌ Node.js not found")
            return False
        
        # Check npm
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ npm: {result.stdout.strip()}")
            else:
                print("❌ npm not found")
                return False
        except FileNotFoundError:
            print("❌ npm not found")
            return False
        
        # Check Capacitor CLI
        try:
            result = subprocess.run(['npx', 'cap', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Capacitor CLI: {result.stdout.strip()}")
            else:
                print("❌ Capacitor CLI not found")
                return False
        except FileNotFoundError:
            print("❌ Capacitor CLI not found")
                return False
        
        return True
    
    def install_dependencies(self):
        """Install npm dependencies"""
        print("📦 Installing dependencies...")
        
        try:
            result = subprocess.run(['npm', 'install'], cwd=self.project_root, check=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def setup_capacitor(self):
        """Initialize Capacitor project"""
        print("🔧 Setting up Capacitor...")
        
        # Initialize Capacitor if not already done
        if not (self.project_root / "capacitor.config.js").exists():
            try:
                subprocess.run([
                    'npx', 'cap', 'init', 
                    'Mobile Corner', 
                    'com.mobilecorner.app', 
                    '--web-dir=www'
                ], cwd=self.project_root, check=True)
                print("✅ Capacitor initialized")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to initialize Capacitor: {e}")
                return False
        
        # Add Android platform
        android_dir = self.project_root / "android"
        if not android_dir.exists():
            try:
                subprocess.run(['npx', 'cap', 'add', 'android'], cwd=self.project_root, check=True)
                print("✅ Android platform added")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to add Android platform: {e}")
                return False
        
        # Add iOS platform (macOS only)
        if sys.platform == "darwin":
            ios_dir = self.project_root / "ios"
            if not ios_dir.exists():
                try:
                    subprocess.run(['npx', 'cap', 'add', 'ios'], cwd=self.project_root, check=True)
                    print("✅ iOS platform added")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Failed to add iOS platform: {e}")
        
        return True
    
    def prepare_assets(self):
        """Prepare and copy assets for mobile app"""
        print("🎨 Preparing assets...")
        
        # Create www directory if it doesn't exist
        self.www_dir.mkdir(exist_ok=True)
        
        # Create assets directories
        assets_dir = self.www_dir / "assets"
        icon_dir = assets_dir / "icon"
        splash_dir = assets_dir / "splash"
        
        icon_dir.mkdir(parents=True, exist_ok=True)
        splash_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy static files
        if self.static_dir.exists():
            static_www_dir = self.www_dir / "static"
            if static_www_dir.exists():
                shutil.rmtree(static_www_dir)
            shutil.copytree(self.static_dir, static_www_dir)
            print("✅ Static files copied")
        
        # Copy logo to assets
        logo_source = self.static_dir / "logo-light.JPG"
        if logo_source.exists():
            # Copy as icon
            shutil.copy2(logo_source, icon_dir / "icon-192x192.png")
            shutil.copy2(logo_source, icon_dir / "icon-512x512.png")
            print("✅ Logo copied to assets")
        
        return True
    
    def generate_icons(self):
        """Generate app icons and splash screens"""
        print("🖼️ Generating icons and splash screens...")
        
        try:
            # Generate Android icons
            subprocess.run([
                'npx', 'cordova-res', 'android', 
                '--skip-config', '--copy'
            ], cwd=self.project_root, check=True)
            print("✅ Android icons generated")
            
            # Generate iOS icons (macOS only)
            if sys.platform == "darwin":
                subprocess.run([
                    'npx', 'cordova-res', 'ios', 
                    '--skip-config', '--copy'
                ], cwd=self.project_root, check=True)
                print("✅ iOS icons generated")
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to generate icons: {e}")
            return False
    
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
    
    def build_android(self):
        """Build Android app"""
        print("🤖 Building Android app...")
        
        try:
            subprocess.run(['npx', 'cap', 'build', 'android'], cwd=self.project_root, check=True)
            print("✅ Android app built successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build Android app: {e}")
            return False
    
    def build_ios(self):
        """Build iOS app (macOS only)"""
        if sys.platform != "darwin":
            print("⚠️ iOS builds are only supported on macOS")
            return False
        
        print("🍎 Building iOS app...")
        
        try:
            subprocess.run(['npx', 'cap', 'build', 'ios'], cwd=self.project_root, check=True)
            print("✅ iOS app built successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build iOS app: {e}")
            return False
    
    def open_android_studio(self):
        """Open project in Android Studio"""
        print("🔧 Opening Android Studio...")
        
        try:
            subprocess.run(['npx', 'cap', 'open', 'android'], cwd=self.project_root, check=True)
            print("✅ Android Studio opened")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to open Android Studio: {e}")
            return False
    
    def open_xcode(self):
        """Open project in Xcode (macOS only)"""
        if sys.platform != "darwin":
            print("⚠️ Xcode is only available on macOS")
            return False
        
        print("🔧 Opening Xcode...")
        
        try:
            subprocess.run(['npx', 'cap', 'open', 'ios'], cwd=self.project_root, check=True)
            print("✅ Xcode opened")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to open Xcode: {e}")
            return False
    
    def serve_app(self):
        """Serve the app locally for testing"""
        print("🌐 Serving app locally...")
        
        try:
            subprocess.run(['npx', 'cap', 'serve'], cwd=self.project_root, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to serve app: {e}")
            return False
    
    def update_app_url(self, url):
        """Update the Django app URL in the mobile app"""
        print(f"🔗 Updating app URL to: {url}")
        
        index_html = self.www_dir / "index.html"
        if index_html.exists():
            try:
                with open(index_html, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace the placeholder URL
                content = content.replace(
                    'https://your-django-app-url.vercel.app',
                    url
                )
                
                with open(index_html, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("✅ App URL updated")
                return True
            except Exception as e:
                print(f"❌ Failed to update app URL: {e}")
                return False
        else:
            print("❌ index.html not found")
            return False
    
    def run_full_build(self, django_url=None):
        """Run the complete build process"""
        print("🚀 Starting full mobile app build...")
        print("=" * 50)
        
        steps = [
            ("Checking prerequisites", self.check_prerequisites),
            ("Installing dependencies", self.install_dependencies),
            ("Setting up Capacitor", self.setup_capacitor),
            ("Preparing assets", self.prepare_assets),
            ("Generating icons", self.generate_icons),
            ("Syncing project", self.sync_project),
        ]
        
        for step_name, step_func in steps:
            print(f"\n📋 {step_name}...")
            if not step_func():
                print(f"❌ Build failed at: {step_name}")
                return False
        
        if django_url:
            self.update_app_url(django_url)
        
        print("\n🎉 Mobile app build completed successfully!")
        print("\nNext steps:")
        print("1. Run 'python build_mobile.py --android' to build for Android")
        print("2. Run 'python build_mobile.py --ios' to build for iOS (macOS only)")
        print("3. Run 'python build_mobile.py --serve' to test locally")
        print("4. Run 'python build_mobile.py --open-android' to open in Android Studio")
        print("5. Run 'python build_mobile.py --open-ios' to open in Xcode (macOS only)")
        
        return True

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Mobile Corner Mobile App Builder')
    parser.add_argument('--android', action='store_true', help='Build Android app')
    parser.add_argument('--ios', action='store_true', help='Build iOS app')
    parser.add_argument('--serve', action='store_true', help='Serve app locally')
    parser.add_argument('--open-android', action='store_true', help='Open in Android Studio')
    parser.add_argument('--open-ios', action='store_true', help='Open in Xcode')
    parser.add_argument('--url', type=str, help='Django app URL')
    parser.add_argument('--full', action='store_true', help='Run full build process')
    
    args = parser.parse_args()
    
    builder = MobileAppBuilder()
    
    if args.full:
        builder.run_full_build(args.url)
    elif args.android:
        builder.build_android()
    elif args.ios:
        builder.build_ios()
    elif args.serve:
        builder.serve_app()
    elif args.open_android:
        builder.open_android_studio()
    elif args.open_ios:
        builder.open_xcode()
    elif args.url:
        builder.update_app_url(args.url)
    else:
        # Default: run full build
        builder.run_full_build(args.url)

if __name__ == "__main__":
    main() 