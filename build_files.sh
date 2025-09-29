#!/bin/bash

echo "Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "Creating directories..."
mkdir -p staticfiles
mkdir -p static

echo "Running migrations..."
# Remove existing migrations and create fresh ones
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
sleep 2

# Make fresh migrations
python3 manage.py makemigrations store --noinput
python3 manage.py makemigrations user_auth --noinput
python3 manage.py makemigrations inventory_erp --noinput
python3 manage.py makemigrations cms_store --noinput
sleep 2

# Apply migrations
python3 manage.py migrate --noinput

echo "Collecting static files..."

# Clear staticfiles directory
rm -rf staticfiles/*
mkdir -p staticfiles

# Collect all static files including Django admin and Wagtail
echo "Collecting all static files (Django, Wagtail, and custom)..."
python3 manage.py collectstatic --noinput --verbosity=2

# Verify Wagtail static files were collected
echo "Verifying Wagtail static files..."
if [ -d "staticfiles/wagtailadmin" ]; then
    echo "✓ Wagtail admin static files collected successfully"
    ls -la staticfiles/wagtailadmin/
else
    echo "⚠ WARNING: Wagtail admin static files not found!"
    echo "Available directories in staticfiles:"
    ls -la staticfiles/
fi

echo "Build completed successfully!" 