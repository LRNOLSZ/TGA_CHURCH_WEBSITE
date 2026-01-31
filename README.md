# TGA Church Management System

A comprehensive Django-based church management system with REST API, admin dashboard, and integrated audit logging.

## Quick Links

- **[Setup & Installation](docs/SETUP.md)** - Get the project running locally
- **[API Documentation](docs/API.md)** - REST API endpoints and usage
- **[Architecture & Code](docs/ARCHITECTURE.md)** - System design, models, and components
- **[Security Guide](docs/SECURITY.md)** - Security measures and configuration

## Overview

**Technology Stack:**
- Django 5.2.8 with PostgreSQL
- Django REST Framework for API
- django-unfold for admin UI
- Rotating file logging with audit trails

**Key Features:**
- ✅ Comprehensive audit logging for all admin actions
- ✅ File upload validation (images, documents)
- ✅ Image tracking across 10 models with orphaned cleanup
- ✅ User profiles with optional profile pictures
- ✅ Security hardening (HSTS, CSP, secure cookies, environment-based config)
- ✅ Organized admin interface with custom widgets

## Project Structure

```
TGA website/
├── api/                          # Main Django app
│   ├── models.py                # Models (Event, Sermon, User, etc.)
│   ├── views.py                 # API views
│   ├── admin.py                 # Admin customization
│   ├── signals.py               # Auto-logging, cleanup signals
│   ├── audit_middleware.py      # Request context capture
│   ├── validators.py            # File upload validation
│   └── migrations/              # Database migrations
├── church_backend/              # Django settings & config
│   ├── settings.py             # Security, logging, env config
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # Production entry point
├── media/                       # Uploaded files (gitignored)
├── static/                      # Static assets
├── logs/                        # Application logs (gitignored)
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
├── manage.py                    # Django CLI
└── docs/                        # Documentation
```

## Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/LRNOLSZ/TGA_CHURCH_WEBSITE.git
cd "TGA website"
python -m venv venv

# 2. Activate venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your database credentials

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create admin user
python manage.py createsuperuser

# 7. Start server
python manage.py runserver
```

Access admin at: `http://127.0.0.1:8000/admin/`

## Environment Configuration

Create a `.env` file in the project root. See [Security Guide](docs/SECURITY.md) for details.

Key variables:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=church_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

## Documentation

- **[Complete Setup Guide](docs/SETUP.md)** - Detailed installation, database setup, production deployment
- **[API Reference](docs/API.md)** - All endpoints, authentication, examples
- **[System Architecture](docs/ARCHITECTURE.md)** - Models, signals, middleware, validators explained
- **[Security Hardening](docs/SECURITY.md)** - Security measures, secrets management, HTTPS configuration

## Development

### Creating Users
Users can be created in the admin panel at `/admin/auth/user/add/`. Profile pictures are optional and can be added during user creation or edited later.

### Adding Content
Navigate to the admin dashboard to manage:
- Banners, Gallery, Church Info
- Pastors, Leadership, Sermons, Events
- Branches, Service Times, Giving Info, Messages

### Viewing Audit Logs
Admin actions are automatically logged. View at `/admin/api/auditlog/`

## Logging

Logs are stored in the `logs/` directory (not git-tracked):
- `django.log` - General application logs
- `security.log` - Security-related warnings
- `audit.log` - All admin actions (CREATE/UPDATE/DELETE/LOGIN/LOGOUT)

## Database

Uses PostgreSQL. Migrations are version-controlled. Run:
```bash
python manage.py migrate
```

## Contributing

1. Create a feature branch
2. Make changes
3. Test locally
4. Commit with clear messages
5. Push and create a pull request

## License

Proprietary - TGA Church

## Support

For issues or questions, refer to the documentation or contact the development team.

---

**Last Updated:** January 2026
