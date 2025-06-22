#!/usr/bin/env python3
"""
Test script to verify static file collection for Unfold admin theme
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.settings')
django.setup()

from django.conf import settings
from django.core.management import call_command
from django.contrib.staticfiles.finders import find

def test_static_collection():
    """Test static file collection"""
    print("Testing static file collection...")
    
    # Check if staticfiles directory exists
    staticfiles_dir = Path(settings.STATIC_ROOT)
    print(f"STATIC_ROOT: {staticfiles_dir}")
    print(f"STATIC_ROOT exists: {staticfiles_dir.exists()}")
    
    # Check if staticfiles/unfold directory exists
    unfold_dir = staticfiles_dir / 'unfold'
    print(f"Unfold directory: {unfold_dir}")
    print(f"Unfold directory exists: {unfold_dir.exists()}")
    
    if unfold_dir.exists():
        # List contents of unfold directory
        print("\nUnfold directory contents:")
        for item in unfold_dir.iterdir():
            print(f"  {item.name}")
            
        # Check specific files that were failing
        critical_files = [
            'unfold/css/styles.css',
            'unfold/fonts/inter/styles.css',
            'unfold/fonts/material-symbols/styles.css',
            'unfold/css/simplebar/simplebar.css',
            'unfold/js/simplebar/simplebar.js',
            'unfold/js/chart/chart.js',
            'unfold/js/htmx/htmx.js',
            'unfold/js/app.js',
            'unfold/js/alpine/alpine.js',
        ]
        
        print("\nChecking critical files:")
        for file_path in critical_files:
            full_path = staticfiles_dir / file_path
            exists = full_path.exists()
            print(f"  {file_path}: {'✓' if exists else '✗'}")
            
            if not exists:
                # Try to find it using Django's static file finders
                found_path = find(file_path)
                if found_path:
                    print(f"    Found at: {found_path}")
                else:
                    print(f"    Not found by Django static file finders")
    
    # Test collectstatic command
    print("\nRunning collectstatic...")
    try:
        call_command('collectstatic', '--noinput', '--clear', verbosity=2)
        print("✓ collectstatic completed successfully")
    except Exception as e:
        print(f"✗ collectstatic failed: {e}")

if __name__ == '__main__':
    test_static_collection() 