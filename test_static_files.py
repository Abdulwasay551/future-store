#!/usr/bin/env python3
"""
Test script to verify static files are being collected and served correctly.
"""

import os
import sys
from pathlib import Path

def test_static_files_collection():
    """Test that static files are collected in the staticfiles directory."""
    base_dir = Path(__file__).parent
    staticfiles_dir = base_dir / 'staticfiles'
    static_dir = base_dir / 'static'
    
    print("Testing static files collection...")
    print(f"Base directory: {base_dir}")
    print(f"Static files directory: {staticfiles_dir}")
    print(f"Static directory: {static_dir}")
    
    # Check if staticfiles directory exists
    if not staticfiles_dir.exists():
        print("❌ staticfiles directory does not exist!")
        return False
    
    # Check if static directory exists
    if not static_dir.exists():
        print("❌ static directory does not exist!")
        return False
    
    # Check for specific files that were failing
    required_files = [
        'js/tailwind.js',
        'js/htmx.js', 
        'js/alpine.min.js',
        'js/dark_mode_toggle.js',
        'css/skeleton.css',
        'logo-light.JPG',
        'logo-dark.JPG',
        'card-back.jpg',
        'card.jpg'
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
        print(f"\n❌ Missing files: {missing_files}")
        return False
    else:
        print("\n✅ All required static files are present!")
        return True

def test_static_files_in_source():
    """Test that static files exist in the source static directory."""
    base_dir = Path(__file__).parent
    static_dir = base_dir / 'static'
    
    print("\nTesting source static files...")
    
    required_files = [
        'js/tailwind.js',
        'js/htmx.js', 
        'js/alpine.min.js',
        'js/dark_mode_toggle.js',
        'css/skeleton.css',
        'logo-light.JPG',
        'logo-dark.JPG',
        'card-back.jpg',
        'card.jpg'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = static_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path} exists in source")
        else:
            print(f"❌ {file_path} missing in source")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing source files: {missing_files}")
        return False
    else:
        print("\n✅ All required source static files are present!")
        return True

if __name__ == "__main__":
    print("Static Files Test")
    print("=" * 50)
    
    source_test = test_static_files_in_source()
    collection_test = test_static_files_collection()
    
    print("\n" + "=" * 50)
    if source_test and collection_test:
        print("✅ All tests passed! Static files should work correctly.")
    else:
        print("❌ Some tests failed. Please check the static files configuration.") 