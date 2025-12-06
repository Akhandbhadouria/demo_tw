# PythonAnywhere Deployment - Quick Start

Your Django Twitter clone is now configured to work with both **Render (PostgreSQL)** and **PythonAnywhere (MySQL)**.

## What's New for PythonAnywhere

### MySQL Database Support
- ✅ Added `mysqlclient==2.2.8` to requirements.txt
- ✅ Database configuration automatically detects MySQL via `DATABASE_URL`
- ✅ Updated `.env.example` with MySQL connection string format

### Configuration Updates
The existing `dj-database-url` library supports both PostgreSQL and MySQL, so your `settings.py` works for both platforms without modification.

---

## Deployment Steps Summary

Follow the complete guide in the `/deploy` workflow. Here's a quick overview:

### 1. Sign Up & Prepare
- Create account at https://www.pythonanywhere.com
- Push your code to Git (GitHub/GitLab/Bitbucket)

### 2. Upload Code
```bash
# In PythonAnywhere Bash console
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

### 3. Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.12 myenv
pip install -r requirements.txt
```

### 4. Create MySQL Database
- Go to **Databases** tab
- Set MySQL password
- Create database: `yourusername$twitter_clone`
- Note credentials

### 5. Create `.env` File
```bash
nano .env
```

Add:
```bash
SECRET_KEY=your-new-secret-key
DEBUG=False
ALLOWED_HOSTS=.pythonanywhere.com,yourusername.pythonanywhere.com
DATABASE_URL=mysql://yourusername:password@yourusername.mysql.pythonanywhere-services.com/yourusername$twitter_clone
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-secret
CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
```

### 6. Run Setup Commands
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 7. Configure WSGI
- **Web** tab → Add new web app → Manual configuration (Python 3.12)
- Edit WSGI file (see full workflow for code)
- Set virtualenv path: `/home/yourusername/.virtualenvs/myenv`

### 8. Configure Static Files
On **Web** tab, add static file mappings:
- URL: `/static/` → Directory: `/home/yourusername/your-project/staticfiles`
- URL: `/media/` → Directory: `/home/yourusername/your-project/media`

### 9. Update Google OAuth
Add to authorized redirect URIs:
- `https://yourusername.pythonanywhere.com/accounts/google/login/callback/`

### 10. Reload & Test
- Click **Reload** on Web tab
- Visit `https://yourusername.pythonanywhere.com`

---

## Key Differences: PythonAnywhere vs Render

| Feature | PythonAnywhere | Render |
|---------|----------------|--------|
| **Database** | MySQL (free) | PostgreSQL (90-day trial) |
| **Setup** | Manual WSGI config | Automated with build script |
| **Env Vars** | `.env` file | Dashboard UI |
| **Static Files** | Manual mapping | Automatic with WhiteNoise |
| **Free Tier** | Limited CPU quota | App sleeps after 15min |
| **Price** | $5/month (Hacker) | $7/month (Starter) |

---

## Important Files

- **Deployment Guide**: `.agent/workflows/deploy.md` (access with `/deploy`)
- **Environment Template**: `.env.example`
- **Requirements**: `requirements.txt` (includes mysqlclient)
- **Settings**: `tax_fare_django/settings.py` (supports both databases)

---

## Troubleshooting

**Import Error: mysqlclient**
```bash
# On your local Mac, you might need:
brew install mysql
pip install mysqlclient
```

**On PythonAnywhere**, mysqlclient should install without issues.

**Database Connection Failed**
- Verify `DATABASE_URL` format in `.env`
- Check MySQL credentials on Databases tab
- Ensure database name includes username prefix: `username$dbname`

---

## Next Steps

1. **Read the full workflow**: Type `/deploy` or view `.agent/workflows/deploy.md`
2. **Follow the 12 steps** carefully
3. **Test thoroughly** after deployment
4. **Monitor error logs** on PythonAnywhere Web tab

Your project is ready to deploy! 🚀
