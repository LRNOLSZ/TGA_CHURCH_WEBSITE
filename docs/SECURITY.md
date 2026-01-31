# Security Guide & Hardening

Comprehensive guide to the security measures implemented in the TGA Church Management System.

## Table of Contents

1. [Overview](#overview)
2. [Environment Variables & Secrets](#environment-variables--secrets)
3. [Authentication & Authorization](#authentication--authorization)
4. [HTTPS & SSL/TLS](#https--ssltls)
5. [Cookie Security](#cookie-security)
6. [Security Headers](#security-headers)
7. [File Upload Security](#file-upload-security)
8. [Database Security](#database-security)
9. [Audit Logging](#audit-logging)
10. [Production Deployment Checklist](#production-deployment-checklist)

## Overview

The system implements defense-in-depth security with multiple layers:

```
┌─────────────────────────────────────┐
│    HTTPS/SSL Encryption             │
├─────────────────────────────────────┤
│    Security Headers (CSP, HSTS)     │
├─────────────────────────────────────┤
│    Cookie Hardening (Secure/SameSite)│
├─────────────────────────────────────┤
│    File Upload Validation           │
├─────────────────────────────────────┤
│    Environment-based Secrets        │
├─────────────────────────────────────┤
│    Audit Logging (all actions)      │
├─────────────────────────────────────┤
│    CSRF Protection                  │
├─────────────────────────────────────┤
│    SQL Injection Prevention (ORM)    │
└─────────────────────────────────────┘
```

## Environment Variables & Secrets

### Never Commit Secrets

**Problem:** Hardcoded secrets exposed in git history

**Solution:** Use `.env` file + `.gitignore`

```bash
# .gitignore
.env
.env.local
.env.*
!.env.example
```

### Create .env File

```bash
cp .env.example .env
# Edit with your actual values
```

### Required .env Variables

```env
# SECURITY - Change these!
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False

# Database credentials
DB_ENGINE=django.db.backends.postgresql
DB_NAME=church_db
DB_USER=church_user
DB_PASSWORD=your-very-strong-database-password
DB_HOST=localhost
DB_PORT=5432

# Allowed origins (your domain)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ORIGINS=https://yourdomain.com

# Email settings (for notifications)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Generate Secret Key

```python
# Python command
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

# Or bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy output to `.env`:
```env
SECRET_KEY=output-from-above-command
```

### Environment Configuration in Code

```python
# settings.py
from decouple import config

# Read from .env, fail if missing
SECRET_KEY = config('SECRET_KEY')

# With default fallback
DEBUG = config('DEBUG', default=False, cast=bool)

# Database
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```

## Authentication & Authorization

### Django's Built-in Auth

The system uses Django's authentication framework:

```python
# Login required for admin
/admin/ → Requires authentication

# Superuser only
Only users with is_staff=True can access admin

# Permissions system
Each model has add/change/delete permissions
```

### User Management

**Creating Admin User:**
```bash
python manage.py createsuperuser
```

**Creating Regular User (via admin):**
1. Go to `/admin/auth/user/add/`
2. Enter username, password
3. Set permissions (staff status, permissions)
4. Optional: Add profile picture via UserProfile inline

### Password Security

```python
# settings.py - Password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

**Password Requirements:**
- Minimum 8 characters
- Not similar to username/email
- Not a common password
- Not purely numeric

### Rotate Database Password Regularly

```bash
# In PostgreSQL
ALTER USER church_user WITH PASSWORD 'new-strong-password';

# Update .env
DB_PASSWORD=new-strong-password

# Restart application
```

## HTTPS & SSL/TLS

### Development (HTTP Only)

```python
# settings.py - local development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
```

### Production (HTTPS Required)

```python
# settings.py - production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Setup HTTPS with Let's Encrypt (Free)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate (for yourdomain.com)
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# Certificate stored at:
# /etc/letsencrypt/live/yourdomain.com/fullchain.pem
# /etc/letsencrypt/live/yourdomain.com/privkey.pem
```

### Configure Nginx with SSL

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Redirect HTTP to HTTPS
    if ($scheme != "https") {
        return 301 https://$server_name$request_uri;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Auto-Renew HTTPS Certificate

```bash
# Create cron job
sudo crontab -e

# Add this line (runs daily at 3am)
0 3 * * * certbot renew --quiet
```

## Cookie Security

### Session Cookies

```python
# settings.py
SESSION_COOKIE_SECURE = not DEBUG  # HTTPS only in production
SESSION_COOKIE_HTTPONLY = True     # Not accessible via JavaScript
SESSION_COOKIE_SAMESITE = 'Strict' # Prevent cross-site requests
SESSION_COOKIE_AGE = 900           # 15 minutes expiry
```

**What These Do:**
- `SECURE` - Only sent over HTTPS (prevents interception)
- `HTTPONLY` - JavaScript can't access (prevents XSS theft)
- `SAMESITE` - Only sent in same-site requests (prevents CSRF)
- `AGE` - Automatically expires after 15 minutes of inactivity

### CSRF Cookies

```python
# settings.py
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_AGE = 31449600  # 1 year
```

## Security Headers

### HTTP Security Headers

```python
# settings.py
SECURE_HSTS_SECONDS = 31536000        # 1 year
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'img-src': ("'self'", 'data:', 'https:'),
    'script-src': ("'self'", "'unsafe-inline'"),
    'style-src': ("'self'", "'unsafe-inline'"),
}
```

### What Each Header Does

| Header | Purpose |
|--------|---------|
| HSTS | Force HTTPS for 1 year (prevents SSL strip attacks) |
| X-Frame-Options | Prevent clickjacking (set to DENY) |
| X-Content-Type-Options | Prevent MIME sniffing (set to nosniff) |
| X-XSS-Protection | Enable browser's XSS filter |
| CSP | Whitelist resources (prevents XSS via inline scripts) |

### Test Security Headers

```bash
# Online tool
https://securityheaders.com/

# Or curl
curl -I https://yourdomain.com/

# Should show:
# Strict-Transport-Security: max-age=31536000
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
```

## File Upload Security

### Validation Layers

**Layer 1: File Extension Whitelist**
```python
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'}
```

**Layer 2: MIME Type Verification**
```python
ALLOWED_IMAGE_MIMES = {
    'image/jpeg', 'image/png', 'image/gif', 'image/webp'
}
```

**Layer 3: File Size Limits**
```python
MAX_IMAGE_SIZE = 10 * 1024 * 1024      # 10 MB
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024   # 10 MB
```

**Layer 4: Filename Sanitization**
```python
def sanitize_filename(filename):
    # Remove dangerous characters
    return re.sub(r'[^\w\s\-\.]', '', filename)
```

### Validators Applied

```python
# In models.py
class Event(models.Model):
    image = ImageField(
        upload_to='events/',
        validators=[validate_image_file],
        blank=True,
        null=True
    )
```

### Attack Prevention

| Attack | Prevention |
|--------|-----------|
| Upload executable | Extension & MIME checking |
| Oversized image DoS | File size limits (10MB) |
| Malformed image crash | Pillow validation |
| Path traversal | Sanitized filenames |
| User execution script | Upload to separate domain |

## Database Security

### Connection Security

```python
# .env
DB_ENGINE=django.db.backends.postgresql
DB_HOST=localhost  # Local: localhost
DB_HOST=db.yourdomain.com  # Production: separate DB server
```

### SQL Injection Prevention

Django ORM prevents SQL injection automatically:

```python
# SAFE - Django escapes values
Event.objects.filter(title="'; DROP TABLE users; --")

# DANGEROUS - Never do this!
Event.objects.raw("SELECT * FROM api_event WHERE title = " + title)
```

### User Permissions

```bash
# PostgreSQL - Least privilege principle
CREATE USER church_user WITH PASSWORD 'strong-pass';
GRANT CONNECT ON DATABASE church_db TO church_user;
GRANT USAGE ON SCHEMA public TO church_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES 
  IN SCHEMA public TO church_user;
```

### Backup Security

```bash
# Regular backups
pg_dump -U church_user church_db > backup.sql

# Encrypted backup (to AWS S3 or similar)
pg_dump -U church_user church_db | gpg -e -r admin@tga.church > backup.sql.gpg
```

## Audit Logging

### What's Logged

```python
AuditLog tracks:
├─ User authentication (LOGIN/LOGOUT)
├─ Model changes (CREATE/UPDATE/DELETE)
├─ IP address (source of request)
├─ User agent (browser/app info)
├─ Timestamp (when action occurred)
├─ What changed (JSON diff)
└─ Object identifier (which record was modified)
```

### Viewing Audit Logs

**In Admin:**
```
1. Go to /admin/api/auditlog/
2. Filter by action (CREATE, UPDATE, DELETE, LOGIN, LOGOUT)
3. Filter by date range
4. Search by username or IP
```

**Via Command Line:**
```bash
# See recent actions
python manage.py shell
>>> from api.models import AuditLog
>>> AuditLog.objects.all()[:10]

# Find suspicious activity
>>> AuditLog.objects.filter(action='DELETE', created_at__gte='2026-01-31')

# Export to file
>>> import csv
>>> qs = AuditLog.objects.all()
>>> writer = csv.writer(open('audit_export.csv', 'w'))
>>> for log in qs:
...     writer.writerow([log.user, log.action, log.created_at])
```

### Monitoring for Suspicious Activity

```python
# Multiple failed logins from same IP
from django.db.models import Count
suspicious_ips = AuditLog.objects.filter(
    action='PERMISSION_DENIED',
    created_at__gte='2026-01-31'
).values('ip_address').annotate(count=Count('id')).filter(count__gt=5)

# Large deletions
bulk_deletes = AuditLog.objects.filter(
    action='DELETE',
    created_at__date='2026-01-31'
).values('user').annotate(count=Count('id')).filter(count__gt=10)
```

## Production Deployment Checklist

### Pre-Deployment

```bash
☐ Update .env with production values
  ├─ SECRET_KEY (use get_random_secret_key)
  ├─ DEBUG=False
  ├─ ALLOWED_HOSTS=yourdomain.com
  ├─ DB credentials (strong password)
  └─ EMAIL settings

☐ HTTPS certificate obtained (Let's Encrypt)

☐ Database password changed from default

☐ Superuser password set (strong)

☐ Static files collected (python manage.py collectstatic)

☐ Media folder permissions set (755)

☐ Logs folder created and permissions set (755)
```

### Deployment Commands

```bash
# On production server
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# Start with Gunicorn + Nginx
gunicorn church_backend.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120
```

### Post-Deployment

```bash
☐ Verify HTTPS working (https://yourdomain.com)

☐ Check security headers (securityheaders.com)

☐ Test login/admin access

☐ Verify audit logging working

☐ Set up log monitoring/rotation

☐ Configure backups (daily)

☐ Set up monitoring alerts (downtime, errors)

☐ Document emergency contacts

☐ Test disaster recovery (restore from backup)
```

### Security Monitoring

```python
# Weekly - Check for suspicious activity
from api.models import AuditLog
from django.utils import timezone
from datetime import timedelta

week_ago = timezone.now() - timedelta(days=7)

# Suspicious deletions
print("Deletions this week:")
print(AuditLog.objects.filter(
    action='DELETE',
    created_at__gte=week_ago
).values('user', 'model_name').annotate(count=models.Count('id')))

# Failed auth attempts
print("Failed logins this week:")
print(AuditLog.objects.filter(
    action='PERMISSION_DENIED',
    created_at__gte=week_ago
).count())
```

## Common Vulnerabilities Fixed

| Vulnerability | Fixed By |
|---|---|
| Hardcoded SECRET_KEY | .env + python-decouple |
| Weak passwords | Django password validators |
| Session hijacking | HttpOnly + Secure + SameSite cookies |
| CSRF attacks | Django CSRF middleware + token |
| Clickjacking | X-Frame-Options: DENY |
| XSS attacks | CSP headers + template escaping |
| SQL injection | Django ORM (parameterized queries) |
| File upload abuse | Extension/MIME/size validation |
| Unencrypted HTTPS | HSTS enforcement |
| Missing audit trail | AuditLog + signal handlers |

## Security Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/5.2/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Security Headers](https://securityheaders.com/)
- [Mozilla SSL Configuration](https://ssl-config.mozilla.org/)

---

**Last Updated:** January 2026
**Next Review:** Quarterly (every 3 months)
