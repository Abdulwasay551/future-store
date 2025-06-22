import os
import sys
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

# Set environment variables for production
os.environ['VERCEL_ENV'] = 'production'
os.environ['DEVELOPMENT'] = 'False'
os.environ['DJANGO_SETTINGS_MODULE'] = 'setting.settings'

# Import Django and set up
import django
django.setup()

# Collect static files if they don't exist
staticfiles_dir = project_dir / 'staticfiles'
if not staticfiles_dir.exists() or not any(staticfiles_dir.iterdir()):
    from django.core.management import call_command
    call_command('collectstatic', '--noinput', '--clear')

# Import the WSGI application
from setting.wsgi import application

# For Vercel serverless function
def handler(request, context):
    return application(request, context) 