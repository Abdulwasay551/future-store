#!/usr/bin/env python3
"""
Deployment test script to verify Vercel deployment configuration.
This script simulates the Vercel environment to test static file collection.
"""

import os
import sys
from pathlib import Path

def test_vercel_environment():
    """Test the application in a Vercel-like environment."""
    print("🧪 Testing Vercel deployment environment...")
    
    # Set Vercel environment variables
    os.environ['VERCEL_ENV'] = 'production'
    os.environ['DEVELOPMENT'] = 'False'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'setting.settings'
    
    # Add project directory to Python path
    project_dir = Path(__file__).parent
    sys.path.insert(0, str(project_dir))
    
    try:
        # Import and test Django setup
        import django
        django.setup()
        print("✅ Django setup successful")
        
        # Test settings import
        from django.conf import settings
        print(f"✅ Settings loaded: DEBUG={settings.DEBUG}")
        print(f"✅ Static files storage: {settings.STATICFILES_STORAGE}")
        print(f"✅ Static root: {settings.STATIC_ROOT}")
        
        # Test static file collection
        from django.core.management import call_command
        call_command('collectstatic', '--noinput', '--clear')
        print("✅ Static files collected successfully")
        
        # Verify static files
        staticfiles_dir = Path(settings.STATIC_ROOT)
        if staticfiles_dir.exists():
            files = list(staticfiles_dir.rglob('*'))
            file_count = len([f for f in files if f.is_file()])
            print(f"✅ Found {file_count} static files in {staticfiles_dir}")
            
            # Check for specific files
            required_files = [
                'js/tailwind.js',
                'js/htmx.js',
                'js/alpine.min.js',
                'css/skeleton.css',
                'logo-light.JPG'
            ]
            
            missing_files = []
            for file_path in required_files:
                full_path = staticfiles_dir / file_path
                if full_path.exists():
                    print(f"✅ {file_path} exists")
                else:
                    print(f"❌ {file_path} missing")
                    missing_files.append(file_path)
            
            if missing_files:
                print(f"⚠️  Missing files: {missing_files}")
            else:
                print("✅ All required static files are present")
        
        # Test WSGI application
        from setting.wsgi import application
        print("✅ WSGI application loaded successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in Vercel environment test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_static_file_serving():
    """Test that static files can be served correctly."""
    print("\n🌐 Testing static file serving...")
    
    try:
        from django.conf import settings
        from django.contrib.staticfiles.handlers import StaticFilesHandler
        from django.test import RequestFactory
        
        # Create a test request
        factory = RequestFactory()
        request = factory.get('/static/js/tailwind.js')
        
        # Test static file serving
        handler = StaticFilesHandler(settings.STATICFILES_STORAGE)
        response = handler.serve(request, 'js/tailwind.js')
        
        if response.status_code == 200:
            print("✅ Static file serving works correctly")
            return True
        else:
            print(f"❌ Static file serving failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing static file serving: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Vercel Deployment Test")
    print("=" * 50)
    
    env_test = test_vercel_environment()
    serving_test = test_static_file_serving()
    
    print("\n" + "=" * 50)
    if env_test and serving_test:
        print("🎉 All tests passed! Deployment should work correctly.")
    else:
        print("❌ Some tests failed. Please check the configuration.") 