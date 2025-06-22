#!/bin/bash

echo "Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "Creating directories..."
mkdir -p staticfiles
mkdir -p media

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

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Build completed successfully!"