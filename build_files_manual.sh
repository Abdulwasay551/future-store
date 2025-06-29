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
sleep 2

# Apply migrations
python3 manage.py migrate --noinput

echo "Collecting static files manually..."

# Clear staticfiles directory
rm -rf staticfiles/*
mkdir -p staticfiles

# Copy Unfold static files first
echo "Copying Unfold static files..."
if [ -d "venv/Lib/site-packages/unfold/static" ]; then
    cp -r venv/Lib/site-packages/unfold/static/* staticfiles/
    echo "✓ Unfold static files copied"
else
    echo "✗ Unfold static files not found in venv"
    exit 1
fi

# Copy your custom static files
echo "Copying custom static files..."
if [ -d "static" ]; then
    cp -r static/* staticfiles/
    echo "✓ Custom static files copied"
else
    echo "⚠ Custom static directory not found"
fi

# Collect Django admin static files
echo "Collecting Django admin static files..."
python3 manage.py collectstatic --noinput --verbosity=2 --ignore=unfold/* --ignore=static/*

echo "Build completed successfully!" 