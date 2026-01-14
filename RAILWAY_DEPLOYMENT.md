# Railway Deployment Guide

This guide will walk you through deploying the gerber_to_scad web application to Railway.

## Prerequisites

1. A [Railway](https://railway.app/) account (sign up for free)
2. A GitHub account
3. This repository forked to your GitHub account (or access to the original repository)

## Deployment Steps

### 1. Create a New Railway Project

1. Log in to [Railway](https://railway.app/)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access your GitHub account if you haven't already
5. Select the `gerber_to_scad` repository

### 2. Configure the Deployment

Railway will automatically detect the `railway.toml` configuration file and use the Dockerfile for building.

The application will:
- Build using the Dockerfile
- Install OpenSCAD and all dependencies
- Start the gunicorn web server on the assigned port

### 3. Set Environment Variables (Optional but Recommended)

For production deployment, you should set the following environment variables:

1. In your Railway project dashboard, go to "Variables"
2. Add the following variables:

   - `SECRET_KEY` - A secure random string for Django (generate one using: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
   - `DJANGO_SETTINGS_MODULE` - Set to `gts_service.railway_settings` (Railway will use production settings)

Optional variables:
   - `PORT` - Railway sets this automatically, but you can override if needed (default: 8000)

### 4. Generate a Domain

1. In your Railway project dashboard, go to "Settings"
2. Click "Generate Domain" under the "Domains" section
3. Railway will provide you with a URL like `https://your-app-name.up.railway.app`

### 5. Access Your Application

Once the deployment is complete (this may take a few minutes):

1. Visit the generated Railway domain
2. Upload your gerber files (solderpaste and outline layers)
3. Configure stencil parameters
4. Download the generated STL file

## Configuration Details

### Railway Configuration (`railway.toml`)

The `railway.toml` file configures:
- Build method (Dockerfile)
- Start command (gunicorn with 1 worker and 8 threads)
- Restart policy (restarts on failure, max 10 retries)

### Django Settings (`gts_service/railway_settings.py`)

The Railway-specific settings include:
- `DEBUG = False` for production
- Allowed hosts configured for Railway domains
- Static files configuration
- OpenSCAD binary path set to `/usr/bin/openscad`
- CSRF trusted origins for Railway
- Security headers enabled

## Troubleshooting

### Build Failures

If the build fails:

1. Check the build logs in Railway dashboard
2. Ensure all dependencies in `pyproject.toml` are compatible
3. Verify that the Dockerfile is correct

### Application Crashes

If the application crashes after deployment:

1. Check the deployment logs in Railway dashboard
2. Verify environment variables are set correctly
3. Ensure `DJANGO_SETTINGS_MODULE` is set to `gts_service.railway_settings`

### Static Files Not Loading

If static files (CSS, JS) are not loading:

1. Railway should automatically collect static files during build
2. Check that `STATIC_ROOT` and `STATIC_URL` are configured in `railway_settings.py`
3. Verify the collectstatic command ran during build (check build logs)

### OpenSCAD Not Found

If you get errors about OpenSCAD not being available:

1. Verify the Dockerfile installs OpenSCAD: `apt-get install -y openscad`
2. Check that `OPENSCAD_BIN` is set to `/usr/bin/openscad` in settings
3. Review deployment logs for any installation errors

### Upload/Processing Errors

If file uploads or processing fails:

1. Check the deployment logs for error details
2. Ensure the `/tmp` directory is writable (it should be by default)
3. Verify that both gerber files are valid and in the correct format

## Updating Your Deployment

When you push changes to your GitHub repository:

1. Railway will automatically detect the changes
2. It will rebuild and redeploy your application
3. Monitor the deployment in the Railway dashboard

You can also manually trigger a deployment:
1. Go to your Railway project dashboard
2. Click "Deploy" in the deployments section
3. Select "Redeploy"

## Resource Usage

Railway's free tier includes:
- 500 hours of usage per month
- $5 of usage credit

The gerber_to_scad application is lightweight and should easily fit within these limits for personal use or low-traffic scenarios.

For higher traffic, consider:
- Upgrading to a paid Railway plan
- Increasing the number of gunicorn workers (edit `railway.toml` or `Dockerfile`)
- Using a CDN for static files

## Support

For issues specific to:
- **Railway platform**: Check [Railway documentation](https://docs.railway.app/)
- **This application**: Open an issue on the [GitHub repository](https://github.com/BeastModz/gerber_to_scad)
- **Gerber file processing**: Refer to the main README.md

## Advanced Configuration

### Custom Domain

To use a custom domain:

1. Go to your Railway project settings
2. Click "Add Custom Domain"
3. Follow Railway's instructions to configure DNS

### Scaling

To handle more traffic:

1. Edit the start command in `railway.toml` to increase workers:
   ```toml
   startCommand = "gunicorn --workers 4 --threads 8 --bind :$PORT gts_service.wsgi"
   ```

2. Consider using Railway's horizontal scaling features for multiple instances

### Environment-Specific Settings

You can create different settings files for different environments:
- Development: `gts_service.settings`
- Railway: `gts_service.railway_settings`
- Other cloud providers: Create similar settings files

Switch between them using the `DJANGO_SETTINGS_MODULE` environment variable.
