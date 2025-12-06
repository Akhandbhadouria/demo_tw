---
description: Deploy Django Twitter Clone to PythonAnywhere
---

# Deploy to PythonAnywhere

This workflow guides you through deploying your Django Twitter clone to PythonAnywhere with MySQL database.

## Prerequisites

- A PythonAnywhere account (sign up at https://www.pythonanywhere.com)
- Your code in a Git repository (GitHub, GitLab, or Bitbucket)
- Google OAuth credentials (already configured in your project)

## Step 1: Sign Up for PythonAnywhere

1. Go to https://www.pythonanywhere.com
2. Click **Pricing & signup** → Choose a plan:
   - **Free (Beginner)**: Good for testing, has limitations
   - **Hacker ($5/month)**: Better for production use
3. Complete the signup process

## Step 2: Upload Your Code

### Option A: Using Git (Recommended)

1. Open a **Bash console** from your PythonAnywhere dashboard
2. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

### Option B: Upload Files

1. Use the **Files** tab in PythonAnywhere
2. Upload your project files manually
3. Navigate to your project directory

## Step 3: Set Up Virtual Environment

In your PythonAnywhere Bash console:

```bash
# Navigate to your project directory
cd ~/your-project-name

# Create virtual environment with Python 3.12
mkvirtualenv --python=/usr/bin/python3.12 myenv

# Activate it (should auto-activate, but if not:)
workon myenv

# Install dependencies
pip install -r requirements.txt
```

## Step 4: Set Up MySQL Database

### Create Database

1. Go to **Databases** tab in PythonAnywhere dashboard
2. Scroll to **MySQL** section
3. If first time: Set a MySQL password (save this!)
4. Under "Create database", enter a name like: `yourusername$twitter_clone`
5. Click **Create**

### Get Database Credentials

Note down these values (shown on the Databases page):
- **Host**: `yourusername.mysql.pythonanywhere-services.com`
- **Database name**: `yourusername$twitter_clone`
- **Username**: `yourusername` (your PythonAnywhere username)
- **Password**: The password you set

## Step 5: Configure Environment Variables

PythonAnywhere doesn't have built-in env var management, so we'll use a `.env` file:

```bash
# In your Bash console, navigate to project directory
cd ~/your-project-name

# Create .env file
nano .env
```

Add the following (replace values with your actual credentials):

```bash
SECRET_KEY=your-new-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.pythonanywhere.com,yourusername.pythonanywhere.com

# MySQL Database
DATABASE_URL=mysql://yourusername:yourpassword@yourusername.mysql.pythonanywhere-services.com/yourusername$twitter_clone

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-secret

# CSRF
CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
```

**To generate a new SECRET_KEY:**
```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Save the file (Ctrl+X, then Y, then Enter).

## Step 6: Run Migrations

In your Bash console with virtual environment activated:

```bash
# Navigate to project directory
cd ~/your-project-name

# Make sure virtualenv is active
workon myenv

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

## Step 7: Configure WSGI File

1. Go to **Web** tab in PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration** (NOT Django - we'll configure ourselves)
4. Select **Python 3.12**
5. Click through to create

### Edit WSGI Configuration

1. On the Web tab, click on the **WSGI configuration file** link
2. **Delete all contents** and replace with:

```python
import os
import sys
from pathlib import Path

# Add your project directory to the sys.path
project_home = '/home/yourusername/your-project-name'  # CHANGE THIS
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'tax_fare_django.settings'

# Load environment variables from .env file
env_path = Path(project_home) / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key, value)

# Initialize Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

3. **Important**: Replace `yourusername` and `your-project-name` with your actual values
4. Click **Save**

## Step 8: Configure Virtual Environment

On the **Web** tab:

1. Scroll to **Virtualenv** section
2. Enter the path to your virtualenv:
   ```
   /home/yourusername/.virtualenvs/myenv
   ```
3. This tells PythonAnywhere to use your virtual environment

## Step 9: Configure Static Files

On the **Web** tab, scroll to **Static files** section:

Add these mappings:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/your-project-name/staticfiles` |
| `/media/` | `/home/yourusername/your-project-name/media` |

(Replace `yourusername` and `your-project-name` with your actual values)

## Step 10: Update Google OAuth

1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Navigate to **APIs & Services** → **Credentials**
3. Click on your OAuth 2.0 Client ID
4. Under **Authorized redirect URIs**, add:
   ```
   https://yourusername.pythonanywhere.com/accounts/google/login/callback/
   ```
5. Under **Authorized JavaScript origins**, add:
   ```
   https://yourusername.pythonanywhere.com
   ```
6. Click **Save**

## Step 11: Reload Web App

1. On the **Web** tab, scroll to the top
2. Click the big green **Reload yourusername.pythonanywhere.com** button
3. Wait for it to complete

## Step 12: Test Your Deployment

1. Visit your site: `https://yourusername.pythonanywhere.com`
2. Test the following:
   - ✅ Homepage loads
   - ✅ Static files (CSS, images) load
   - ✅ User registration works
   - ✅ Login works
   - ✅ Google OAuth works
   - ✅ Creating tweets works
   - ✅ Admin panel: `https://yourusername.pythonanywhere.com/admin/`

## Updating Your Code

When you make changes and want to deploy updates:

```bash
# SSH into PythonAnywhere bash console
cd ~/your-project-name

# Pull latest changes
git pull origin main

# Activate virtual environment
workon myenv

# Install any new dependencies
pip install -r requirements.txt

# Run migrations (if any)
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

Then go to **Web** tab and click **Reload**.

## Troubleshooting

### Static Files Not Loading

1. Check that `STATIC_ROOT` is set in settings.py
2. Run `python manage.py collectstatic --noinput`
3. Verify static file mappings on Web tab
4. Check error log on Web tab

### Database Connection Error

1. Verify MySQL credentials in `.env` file
2. Check that `mysqlclient` is installed: `pip list | grep mysqlclient`
3. Verify database exists in Databases tab
4. Check error log for specific error message

### 502 Bad Gateway

1. Check error log on Web tab for Python errors
2. Verify WSGI configuration paths are correct
3. Ensure virtual environment path is correct
4. Check that all dependencies installed: `pip install -r requirements.txt`

### Import Errors

1. Verify `sys.path` includes your project directory in WSGI file
2. Check that virtual environment is properly activated
3. Reinstall requirements: `pip install -r requirements.txt`

### Google OAuth Not Working

1. Verify redirect URIs in Google Cloud Console
2. Check `.env` file has correct GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
3. Ensure CSRF_TRUSTED_ORIGINS includes your PythonAnywhere URL

## PythonAnywhere Limitations

### Free Account
- Daily CPU quota (100 CPU seconds)
- One web app only
- MySQL database limited storage
- No outbound internet access (except whitelist)
- HTTPS only to your subdomain

### Paid Accounts ($5/month+)
- Higher CPU quota
- Multiple web apps
- More storage
- Full outbound internet access
- Custom domains supported

## Cost Estimate

**Free Tier**: 
- Good for learning and testing
- Limited resources

**Hacker Plan ($5/month)**:
- Recommended for production
- Custom domain support
- Better performance

**Web App Plan ($12/month)**:
- More CPU and storage
- Multiple workers

## Important Security Notes

> [!CAUTION]
> Make sure `.env` file is NOT committed to Git! It's in your `.gitignore`, but double-check.

> [!WARNING]
> Always use a NEW `SECRET_KEY` for production (don't use the default from settings.py)

> [!IMPORTANT]
> Set `DEBUG=False` in production to hide sensitive error information

## Next Steps After Deployment

1. **Set up regular backups**: Download your MySQL database regularly
2. **Monitor error logs**: Check the error log on Web tab periodically
3. **Update dependencies**: Keep your packages up to date for security
4. **Custom domain** (paid plans): Set up your own domain name
5. **SSL certificate**: Automatic for `.pythonanywhere.com`, configure for custom domains

---

**Need Help?** 
- PythonAnywhere Help: https://help.pythonanywhere.com/
- Forums: https://www.pythonanywhere.com/forums/
- Django deployment guide: https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/
