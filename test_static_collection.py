#!/usr/bin/env python
"""
Test script to verify static file collection
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.settings')

# Setup Django
django.setup()

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError

def test_static_collection():
    """Test static file collection"""
    print("=== Testing Static File Collection ===")
    
    # Check settings
    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print(f"STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"DEVELOPMENT: {settings.DEVELOPMENT}")
    
    # Create staticfiles directory if it doesn't exist
    os.makedirs(settings.STATIC_ROOT, exist_ok=True)
    
    # Clear staticfiles directory
    import shutil
    if os.path.exists(settings.STATIC_ROOT):
        shutil.rmtree(settings.STATIC_ROOT)
    os.makedirs(settings.STATIC_ROOT)
    
    print(f"\nCleared {settings.STATIC_ROOT}")
    
    # Collect static files
    try:
        call_command('collectstatic', '--noinput', '--verbosity=2')
        print("✓ Static files collected successfully")
    except CommandError as e:
        print(f"✗ Error collecting static files: {e}")
        return False
    
    # Check if admin static files were collected
    admin_css_path = os.path.join(settings.STATIC_ROOT, 'admin', 'css', 'base.css')
    admin_js_path = os.path.join(settings.STATIC_ROOT, 'admin', 'js', 'admin', 'urlify.js')
    
    print(f"\nChecking admin static files:")
    print(f"Admin CSS exists: {os.path.exists(admin_css_path)}")
    print(f"Admin JS exists: {os.path.exists(admin_js_path)}")
    
    if os.path.exists(admin_css_path):
        print(f"✓ Admin CSS file found: {admin_css_path}")
    else:
        print(f"✗ Admin CSS file missing: {admin_css_path}")
    
    if os.path.exists(admin_js_path):
        print(f"✓ Admin JS file found: {admin_js_path}")
    else:
        print(f"✗ Admin JS file missing: {admin_js_path}")
    
    # List some files in staticfiles
    print(f"\nFiles in {settings.STATIC_ROOT}:")
    for root, dirs, files in os.walk(settings.STATIC_ROOT):
        level = root.replace(settings.STATIC_ROOT, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:  # Show first 5 files
            print(f"{subindent}{file}")
        if len(files) > 5:
            print(f"{subindent}... and {len(files) - 5} more files")
    
    return True

if __name__ == '__main__':
    test_static_collection() 