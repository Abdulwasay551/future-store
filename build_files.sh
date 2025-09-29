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
echo "Contents of staticfiles directory:"
ls -la staticfiles/

if [ -d "staticfiles/wagtailadmin" ]; then
    echo "✓ Wagtail admin static files collected successfully"
    echo "Wagtail admin CSS files:"
    ls -la staticfiles/wagtailadmin/css/ 2>/dev/null || echo "No CSS directory found"
    echo "Wagtail admin JS files:"
    ls -la staticfiles/wagtailadmin/js/ | head -10 2>/dev/null || echo "No JS directory found"
else
    echo "⚠ WARNING: Wagtail admin static files not found!"
    echo "Available directories in staticfiles:"
    ls -la staticfiles/
fi

# Also verify critical files exist
echo "Checking for critical Wagtail files:"
test -f "staticfiles/wagtailadmin/css/core.css" && echo "✓ core.css found" || echo "✗ core.css missing"
test -f "staticfiles/wagtailadmin/js/core.js" && echo "✓ core.js found" || echo "✗ core.js missing"
test -f "staticfiles/wagtailadmin/js/icons.js" && echo "✓ icons.js found" || echo "✗ icons.js missing"

echo "Build completed successfully!" 