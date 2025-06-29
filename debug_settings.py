#!/usr/bin/env python
"""
Debug script to check Django settings and environment variables
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

print("=== Django Settings Debug ===")
print(f"DEBUG: {settings.DEBUG}")
print(f"DEVELOPMENT: {settings.DEVELOPMENT}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"SECURE_SSL_REDIRECT: {settings.SECURE_SSL_REDIRECT}")
print(f"SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
print(f"CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")

print("\n=== Environment Variables ===")
print(f"DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")
print(f"DEBUG (env): {os.getenv('DEBUG')}")
print(f"DEVELOPMENT (env): {os.getenv('DEVELOPMENT')}")
print(f"ALLOWED_HOSTS (env): {os.getenv('ALLOWED_HOSTS')}")

print("\n=== Current Host Info ===")
import socket
hostname = socket.gethostname()
print(f"Hostname: {hostname}")
print(f"Hostname in ALLOWED_HOSTS: {hostname in settings.ALLOWED_HOSTS}")
print(f"Wildcard in ALLOWED_HOSTS: {'*' in settings.ALLOWED_HOSTS}") 