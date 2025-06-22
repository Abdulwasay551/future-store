# Django Vercel Deployment Guide

## Current Issues and Solutions

### 1. **500 Internal Server Error - FUNCTION_INVOCATION_FAILED**

This error typically occurs due to one of these issues:

#### **A. Missing Environment Variables**
You need to set these environment variables in your Vercel dashboard:

**Required Environment Variables:**
```
DJANGO_SECRET_KEY=your-secure-secret-key-here
DEBUG=False
DEVELOPMENT=False
VERCEL_ENV=production
```

**Database Variables (if using PostgreSQL):**
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=your-database-host
DB_PORT=5432
```

**Email Variables:**
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### **B. Database Connection Issues**
- **Problem**: Your app is configured for PostgreSQL but you might not have a database set up
- **Solution**: Either set up a PostgreSQL database or temporarily use SQLite for testing

#### **C. Static Files Issues**
- **Problem**: WhiteNoise configuration might be causing issues
- **Solution**: The updated settings now use a simpler WhiteNoise configuration for Vercel

### 2. **Step-by-Step Fix Process**

#### **Step 1: Test Locally**
Run the debug script to check your configuration:
```bash
python debug_deployment.py
```

#### **Step 2: Set Environment Variables in Vercel**
1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add all the required variables listed above

#### **Step 3: Database Setup**
**Option A: Use SQLite (for testing)**
- No additional setup needed, the app will use SQLite locally

**Option B: Use PostgreSQL (recommended for production)**
- Set up a PostgreSQL database (Vercel Postgres, Supabase, etc.)
- Add the database credentials to environment variables
- Run migrations on the production database

#### **Step 4: Deploy and Test**
1. Push your changes to GitHub
2. Vercel will automatically redeploy
3. Test the `/store/test/` endpoint first
4. Check Vercel logs for any errors

### 3. **Testing Endpoints**

After deployment, test these endpoints in order:

1. **Test endpoint**: `https://your-domain.vercel.app/store/test/`
   - Should return "Store app is working!"

2. **Main store**: `https://your-domain.vercel.app/store/`
   - Should show the product list

3. **Admin**: `https://your-domain.vercel.app/admin/`
   - Should show the admin interface

### 4. **Common Error Solutions**

#### **Import Errors**
- Make sure all apps are properly installed
- Check that all dependencies are in `requirements.txt`

#### **Database Errors**
- Verify database credentials
- Ensure database is accessible from Vercel
- Check if migrations have been applied

#### **Static File Errors**
- The updated WhiteNoise configuration should handle this
- Make sure `STATIC_ROOT` directory exists

#### **Template Errors**
- Check that all template files exist
- Verify template syntax

### 5. **Vercel-Specific Configuration**

The updated `vercel.json` now includes:
- Proper static file routing
- Environment variable for production detection
- Simplified build configuration

### 6. **Debugging Steps**

If you still get errors:

1. **Check Vercel Logs**
   - Go to your Vercel dashboard
   - Click on the latest deployment
   - Check the "Functions" tab for error logs

2. **Test the Test Endpoint**
   - Visit `/store/test/` first
   - This simple endpoint should work even if others fail

3. **Check Environment Variables**
   - Verify all variables are set correctly
   - Make sure there are no typos

4. **Database Connection**
   - Test database connectivity
   - Ensure migrations are applied

### 7. **Production Checklist**

Before going live:
- [ ] All environment variables set
- [ ] Database configured and accessible
- [ ] Static files collected and served
- [ ] All migrations applied
- [ ] Test endpoints working
- [ ] Admin interface accessible
- [ ] Email configuration working (if needed)

### 8. **Emergency Fallback**

If you need to get the app working quickly:
1. Set `DEBUG=True` temporarily to see detailed error messages
2. Use SQLite database instead of PostgreSQL
3. Disable email functionality temporarily

Remember to change these back for production!

---

**Need Help?**
- Check Vercel logs for specific error messages
- Run the debug script locally
- Test each endpoint individually
- Verify all environment variables are set 