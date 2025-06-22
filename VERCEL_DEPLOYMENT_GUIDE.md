# Vercel Deployment Guide for Django

## Overview
This guide explains how to properly deploy a Django application on Vercel with static files support.

## Issues Fixed

### 1. Static Files Not Loading (404 Errors)
The main issue was that static files were not being collected and served properly in the Vercel environment.

### 2. Configuration Changes Made

#### Settings.py Updates
- Fixed `os.makedirs()` calls with `exist_ok=True` parameter
- Updated static files storage for Vercel compatibility
- Added proper environment detection

#### Vercel.json Updates
- Added `DEVELOPMENT=False` environment variable
- Configured proper static file routing

## Deployment Steps

### 1. Pre-deployment Checklist
- [ ] All static files are in the `static/` directory
- [ ] `staticfiles/` directory exists (will be created during build)
- [ ] `vercel.json` is properly configured
- [ ] Environment variables are set in Vercel dashboard

### 2. Environment Variables
Set these in your Vercel project settings:
```
DJANGO_SECRET_KEY=your_secret_key_here
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
DEVELOPMENT=False
VERCEL_ENV=production
```

### 3. Build Process
The build process should:
1. Install dependencies from `requirements.txt`
2. Run `python manage.py collectstatic --noinput`
3. Run `python manage.py migrate --noinput`

### 4. Static Files Configuration
- **Development**: Uses Django's default static files storage
- **Production**: Uses WhiteNoise for static file serving
- **Static URL**: `/static/`
- **Static Root**: `staticfiles/`

## Troubleshooting

### Static Files Still Not Loading
1. Check if `staticfiles/` directory exists and contains files
2. Verify Vercel routing in `vercel.json`
3. Ensure `DEVELOPMENT=False` is set in environment variables
4. Check if WhiteNoise is properly configured

### Build Failures
1. Check if all dependencies are in `requirements.txt`
2. Verify Python version compatibility (3.11.9)
3. Ensure database connection is working
4. Check for syntax errors in settings.py

### Database Issues
1. Verify database credentials in environment variables
2. Check if database is accessible from Vercel
3. Ensure migrations are running successfully

## File Structure
```
project/
├── static/                 # Source static files
│   ├── css/
│   ├── js/
│   └── images/
├── staticfiles/           # Collected static files (created during build)
├── setting/
│   ├── settings.py       # Django settings
│   └── wsgi.py          # WSGI configuration
├── vercel.json          # Vercel configuration
├── requirements.txt     # Python dependencies
└── manage.py           # Django management script
```

## Key Configuration Files

### vercel.json
```json
{
    "version": 2,
    "builds": [
        {
            "src": "setting/wsgi.py",
            "use": "@vercel/python",
            "config": {
                "maxLambdaSize": "15mb",
                "runtime": "python3.11.9"
            }
        }
    ],
    "routes": [
        {
            "src": "/static/(.*)",
            "dest": "/staticfiles/$1"
        },
        {
            "src": "/media/(.*)",
            "dest": "/media/$1"
        },
        {
            "src": "/(.*)",
            "dest": "setting/wsgi.py"
        }
    ],
    "env": {
        "PYTHONPATH": "/var/task",
        "DJANGO_SETTINGS_MODULE": "setting.settings",
        "VERCEL_ENV": "production",
        "DEVELOPMENT": "False"
    }
}
```

### settings.py (Static Files Section)
```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Create static directories if they don't exist (only in development)
if DEVELOPMENT:
    try:
        os.makedirs(STATIC_ROOT, exist_ok=True)
        os.makedirs(os.path.join(BASE_DIR, 'static'), exist_ok=True)
    except OSError:
        pass

# Enable WhiteNoise for static files
if not DEVELOPMENT:
    STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True
    WHITENOISE_ROOT = os.path.join(BASE_DIR, 'staticfiles')
else:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
```

## Testing
Run the test script to verify static files:
```bash
python test_static_files.py
```

## Common Issues and Solutions

### Issue: Static files return 404
**Solution**: Ensure `DEVELOPMENT=False` is set and static files are collected during build.

### Issue: Build fails with filesystem errors
**Solution**: The `exist_ok=True` parameter prevents directory creation errors in read-only environments.

### Issue: WhiteNoise not serving files
**Solution**: Use `StaticFilesStorage` instead of `CompressedManifestStaticFilesStorage` for simpler deployment.

## Support
If you continue to have issues:
1. Check Vercel deployment logs
2. Verify all environment variables are set
3. Test locally with `DEVELOPMENT=False`
4. Ensure all static files are committed to the repository 