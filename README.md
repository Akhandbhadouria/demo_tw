# Django Twitter Clone 🐦

A full-featured Twitter/X clone built with Django, featuring tweets, real-time chat, user profiles, and Google OAuth authentication.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.8-green.svg)

## ✨ Features

- **Tweets**: Create, view, delete tweets with text and images (240 char limit)
- **User Profiles**: Custom profiles with bio, photos, follow/unfollow system
- **Social Engagement**: Like tweets, follow users, view timelines
- **Real-time Chat**: Live messaging with Django Channels and WebSocket
- **Authentication**: Username/password login + Google OAuth integration
- **Security**: CSRF protection, XSS filtering, production-ready settings

## 🛠️ Tech Stack

- **Backend**: Django 5.2.8, Channels, Allauth, Gunicorn
- **Database**: SQLite (dev), PostgreSQL/MySQL (production)
- **Frontend**: HTML, CSS, JavaScript
- **Real-time**: Redis (production), In-memory (dev)
- **Deployment**: WhiteNoise, PythonAnywhere

## � Quick Start

### 1. Setup

```bash
# Clone and navigate
git clone <repository-url>
cd tweet_copy_2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. Initialize Database

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --no-input
```

### 4. Run Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

## 📁 Project Structure

```
tweet_copy_2/
├── chat/              # Real-time chat app
├── tweet/             # Main tweet app (models, views, forms)
├── tax_fare_django/   # Project settings
├── templates/         # Global templates
├── static/            # CSS, JS, images
├── media/             # User uploads
└── requirements.txt   # Dependencies
```

## 🔐 Google OAuth (Optional)

1. Create project at [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Google+ API and create OAuth credentials
3. Add redirect URI: `http://localhost:8000/accounts/google/login/callback/`
4. Add credentials to `.env`:
```env
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-secret
```

## 🌐 Deployment

See [`DEPLOYMENT_PYTHONANYWHERE.md`](./DEPLOYMENT_PYTHONANYWHERE.md) for detailed PythonAnywhere deployment guide.

**Quick deploy checklist:**
- Set `DEBUG=False` in production
- Configure `DATABASE_URL` for PostgreSQL/MySQL
- Set up Redis for real-time chat
- Add production domain to `ALLOWED_HOSTS`
- Configure `CSRF_TRUSTED_ORIGINS`

## 📝 Key Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (True/False) | No |
| `DATABASE_URL` | Database connection | No (uses SQLite) |
| `ALLOWED_HOSTS` | Allowed domains | Yes (prod) |
| `REDIS_URL` | Redis for chat | No (uses in-memory) |

## 🐛 Troubleshooting

**Missing packages:**
```bash
pip install -r requirements.txt
```

**Database issues:**
```bash
python manage.py migrate --run-syncdb
```

**Static files not loading:**
```bash
python manage.py collectstatic --clear
```

## � License

MIT License

---

**Built with ❤️ using Django**
