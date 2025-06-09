#!/bin/bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
mkdir -p staticfiles
python3 manage.py collectstatic --noinput --clear 
python3 manage.py migrate