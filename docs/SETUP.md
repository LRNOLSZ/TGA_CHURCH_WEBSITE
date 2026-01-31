# Setup & Installation Guide

Complete guide to set up the TGA Church Management System for development and production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Database Configuration](#database-configuration)
4. [Environment Variables](#environment-variables)
5. [Running Migrations](#running-migrations)
6. [Creating Admin User](#creating-admin-user)
7. [Running the Server](#running-the-server)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

- **Python 3.12+** ([Download](https://www.python.org/downloads/))
- **PostgreSQL 12+** ([Download](https://www.postgresql.org/download/))
- **Git** ([Download](https://git-scm.com/))
- **Virtual Environment Tool** (venv - comes with Python)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/LRNOLSZ/TGA_CHURCH_WEBSITE.git
cd "TGA website"
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Main Dependencies:**
- Django 5.2.8
- djangorestframework
- django-cors-headers
- django-unfold
- psycopg2-binary (PostgreSQL driver)
- python-decouple (environment variable management)
- Pillow (image processing)

## Database Configuration

### 1. Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE church_db;
CREATE USER church_user WITH PASSWORD 'your-secure-password';
ALTER ROLE church_user SET client_encoding TO 'utf8';
ALTER ROLE church_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE church_user SET default_transaction_deferrable TO on;
ALTER ROLE church_user SET default_transaction_read_only TO off;
GRANT ALL PRIVILEGES ON DATABASE church_db TO church_user;

# Exit psql
\q
```

### 2. Verify Connection

```bash
psql -U church_user -d church_db -c "\l"
```

Should list the database without errors.

## Environment Variables

### 1. Create .env File

Copy the template:

```bash
cp .env.example .env
```

### 2. Configure .env

Edit `.env` with your values:

```env
# Security - CHANGE IN PRODUCTION!
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=True

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=church_db
DB_USER=church_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS Origins
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# File Upload Limits (bytes)
MAX_IMAGE_SIZE=10485760
MAX_DOCUMENT_SIZE=10485760

# Email (optional, for production)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**⚠️ Security Notes:**
- Never commit `.env` to git (it's in `.gitignore`)
- Generate SECRET_KEY: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Use strong database passwords
- In production, set `DEBUG=False`

## Running Migrations

### 1. Create Migrations

```bash
python manage.py makemigrations
```

This creates migration files from your models. Output should show:
```
Migrations for 'api':
  ...
```

### 2. Apply Migrations

```bash
python manage.py migrate
```

This creates all database tables. Output shows:
```
Running migrations:
  ...
  Applying auth.0001_initial... OK
  Applying api.0001_initial... OK
  ...
```

### 3. Verify Database

```bash
python manage.py dbshell
# Lists all tables
\dt

# Exit
\q
```

## Creating Admin User

```bash
python manage.py createsuperuser
```

Prompts for:
- Username
- Email
- Password (enter twice)

Example:
```
Username: admin
Email: admin@example.com
Password: 
Password (again):
Superuser created successfully.
```

## Running the Server

### Development Server

```bash
python manage.py runserver
```

Output:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Access Points

- **Admin Panel:** http://127.0.0.1:8000/admin/
- **API Root:** http://127.0.0.1:8000/api/
- **API Docs:** http://127.0.0.1:8000/api/docs/ (if configured)

### Run on Different Port

```bash
python manage.py runserver 8080
```

## Production Deployment

### 1. Update Environment

```env
DEBUG=False
SECRET_KEY=generate-new-key-for-production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 2. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

Creates `/staticfiles/` directory with compressed assets.

### 3. Use Production Server (Gunicorn)

```bash
pip install gunicorn

gunicorn church_backend.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### 4. Set Up Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/project/staticfiles/;
    }

    location /media/ {
        alias /path/to/project/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5. Enable HTTPS

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com
```

Update `settings.py`:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Troubleshooting

### Issue: "relation does not exist"

**Cause:** Migrations not applied
**Solution:**
```bash
python manage.py migrate
```

### Issue: "could not connect to database"

**Cause:** PostgreSQL not running or wrong credentials
**Solution:**
```bash
# Start PostgreSQL (Windows)
pg_ctl -D "C:\Program Files\PostgreSQL\data" start

# Or macOS
brew services start postgresql

# Test connection
psql -U church_user -d church_db -c "SELECT 1"
```

### Issue: "no such table: api_userprofile"

**Cause:** Missing migration
**Solution:**
```bash
python manage.py makemigrations api
python manage.py migrate
```

### Issue: "ModuleNotFoundError" for dependencies

**Cause:** Virtual environment not activated or dependencies not installed
**Solution:**
```bash
# Activate venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# Install requirements
pip install -r requirements.txt
```

### Issue: "SECRET_KEY not found in environment"

**Cause:** Missing `.env` file
**Solution:**
```bash
cp .env.example .env
# Edit .env with your values
```

### Issue: Admin page shows 500 error

**Check logs:**
```bash
tail -f logs/django.log
```

Common causes:
- Database not migrated
- Missing environment variables
- File permission issues for logs/media directories

## Next Steps

1. [Read API Documentation](API.md) to understand available endpoints
2. [Review Architecture](ARCHITECTURE.md) to understand the codebase
3. [Check Security Guide](SECURITY.md) for production deployment best practices

---

**Last Updated:** January 2026
