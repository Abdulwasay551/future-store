#!/usr/bin/env python3
"""
Debug script to check deployment configuration
Run this locally to identify potential issues before deploying to Vercel
"""

import os
import sys
import django
from pathlib import Path

def check_environment():
    """Check environment variables and configuration"""
    print("=== Environment Check ===")
    
    # Check if we're in production
    vercel_env = os.getenv('VERCEL_ENV')
    print(f"VERCEL_ENV: {vercel_env}")
    
    # Check Django settings
    django_settings = os.getenv('DJANGO_SETTINGS_MODULE')
    print(f"DJANGO_SETTINGS_MODULE: {django_settings}")
    
    # Check Python path
    print(f"Python path: {sys.path[:3]}...")
    
    # Check if we can import Django
    try:
        import django
        print(f"Django version: {django.get_version()}")
    except ImportError as e:
        print(f"Error importing Django: {e}")
        return False
    
    return True

def check_database():
    """Check database configuration"""
    print("\n=== Database Check ===")
    
    try:
        # Set up Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.settings')
        django.setup()
        
        from django.db import connection
        from django.conf import settings
        
        print(f"Database engine: {settings.DATABASES['default']['ENGINE']}")
        print(f"Database name: {settings.DATABASES['default']['NAME']}")
        
        # Try to connect
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("Database connection: SUCCESS")
            
    except Exception as e:
        print(f"Database connection: FAILED - {e}")
        return False
    
    return True

def check_static_files():
    """Check static files configuration"""
    print("\n=== Static Files Check ===")
    
    try:
        from django.conf import settings
        from django.contrib.staticfiles.finders import find
        
        print(f"STATIC_URL: {settings.STATIC_URL}")
        print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
        print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        print(f"STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
        
        # Check if static root exists
        static_root = Path(settings.STATIC_ROOT)
        if static_root.exists():
            print(f"STATIC_ROOT exists: YES")
        else:
            print(f"STATIC_ROOT exists: NO")
            
    except Exception as e:
        print(f"Static files check: FAILED - {e}")
        return False
    
    return True

def check_apps():
    """Check if all apps can be imported"""
    print("\n=== Apps Check ===")
    
    apps = ['user_auth', 'store', 'chatbot', 'inventory_erp']
    
    for app in apps:
        try:
            __import__(app)
            print(f"{app}: SUCCESS")
        except ImportError as e:
            print(f"{app}: FAILED - {e}")
            return False
    
    return True

def main():
    """Run all checks"""
    print("Django Deployment Debug Script")
    print("=" * 40)
    
    checks = [
        check_environment,
        check_database,
        check_static_files,
        check_apps,
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✅ All checks passed!")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
    
    return all_passed

if __name__ == "__main__":
    main() 