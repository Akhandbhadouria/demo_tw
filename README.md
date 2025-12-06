# Conecto – Social Media Platform

A modern full-stack social networking application built with Django, featuring real-time chat, posts, likes, follows, profiles, and production-ready deployment.

🔗 **Live Demo**: [https://lambardaar.pythonanywhere.com/](https://lambardaar.pythonanywhere.com/)

## ⭐ Features

- **Tweet/Post System** – text + images, like/unlike
- **User Profiles** – bio, profession, photo, verification badge
- **Real-Time Chat** – WebSockets using Django Channels
- **Authentication** – username/password + optional Google OAuth
- **Social Actions** – follow/unfollow, timelines
- **Responsive UI** – mobile-ready design

## 🛠 Tech Stack

- **Backend**: Django, Django Channels, Python
- **Realtime**: WebSockets, Redis
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (dev), PostgreSQL/MySQL (prod)
- **Deployment**: Gunicorn, WhiteNoise, environment variables

## 📁 Project Structure (Simplified)

```
project/
├── chat/            # Real-time messaging
├── tweet/           # Tweet & profile features
├── project_root/    # Settings, URLs, ASGI/WSGI
├── templates/
├── static/
├── media/
└── requirements.txt
```

## 🚀 Installation

```bash
git clone <repo-url>
cd project

python -m venv venv
source venv/bin/activate      # or venv\Scripts\activate on Windows

pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

**Visit:**
```
http://127.0.0.1:8000
```

## 🎮 How to Use

1. **Sign Up / Login** – Create an account or use Google OAuth
2. **Create Profile** – Add bio, profession, and profile photo
3. **Post Tweets** – Share text and images (240 char limit)
4. **Social Actions** – Like posts, follow users, view timelines
5. **Real-Time Chat** – Message other users instantly
6. **Explore** – Discover content and connect with others

## 🔒 Security

- CSRF protection
- XSS filtering
- Secure cookies (production)
- WhiteNoise static serving

## � Future Enhancements

- Notifications
- Hashtags
- Retweets
- Group chat
- API for mobile apps

## 📝 License

MIT License. Feel free to use and modify.
