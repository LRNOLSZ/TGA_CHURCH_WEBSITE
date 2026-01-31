import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ SECRET_KEY must be set in environment variables
SECRET_KEY = config('SECRET_KEY', default='')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set. Please set it in your .env file.")

# DEBUG should NEVER be True in production
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS should be specific - not wildcards
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])
if DEBUG:
    # Allow development servers when DEBUG is True
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])
if not DEBUG:
    # In production, ensure proper domain is set
    if 'localhost' in ALLOWED_HOSTS or '127.0.0.1' in ALLOWED_HOSTS:
        raise ValueError("localhost/127.0.0.1 should not be in ALLOWED_HOSTS in production")


# Application definition
INSTALLED_APPS = [
    'unfold',  # Must be at the top
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'embed_video',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'church_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'church_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# SESSION SECURITY
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Logout when browser closes
SESSION_COOKIE_AGE = 900  # 15 minutes in seconds
SESSION_COOKIE_SECURE = not DEBUG  # Enforce HTTPS in production
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
SESSION_COOKIE_SAMESITE = 'Strict'  # Strict CSRF protection
CSRF_COOKIE_SECURE = not DEBUG  # Enforce HTTPS for CSRF cookie
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access to CSRF cookie
CSRF_COOKIE_SAMESITE = 'Strict'  # Strict CSRF protection

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SECURITY HEADERS
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int) if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG  # Redirect HTTP to HTTPS in production
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": ("'self'", "'unsafe-inline'"),  # Adjust based on your needs
    "style-src": ("'self'", "'unsafe-inline'"),
    "img-src": ("'self'", "data:", "https:"),
    "font-src": ("'self'",),
    "connect-src": ("'self'",),
    "frame-ancestors": ("'none'",),
}

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://localhost:5173' if DEBUG else '',
    cast=lambda v: [s.strip() for s in v.split(',')] if v else []
)

# Additional security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# --- UNFOLD BRANDING (Blue, White, Yellow) ---
UNFOLD = {
    "SITE_TITLE": "TGA Admin",
    "SITE_HEADER": "TGA Church Management",
    "SITE_SYMBOL": "church",
    "COLORS": {
        "primary": {
            "50": "239 246 255",
            "100": "219 234 254",
            "200": "191 219 254",
            "300": "147 197 253",
            "400": "96 165 250",
            "500": "37 99 235",    # Royal Blue
            "600": "29 78 216",
            "700": "30 64 175",
            "800": "30 58 138",
            "900": "30 50 110",
        },
        "accent": {
            "500": "251 191 36",   # Golden Yellow
        }
    },
    "SIDEBAR": {
        "show_search": True,
        "navigation": [
            {
                "title": "Website Content",
                "items": [
                    {"title": "Banners", "icon": "view_carousel", "link": "/admin/api/homebanner/"},
                    {"title": "Church Info", "icon": "info", "link": "/admin/api/churchinfo/"},
                    {"title": "Gallery", "icon": "photo_library", "link": "/admin/api/photogallery/"},
                ],
            },
            {
                "title": "Ministry",
                "items": [
                    {"title": "Head Pastor", "icon": "person_pin", "link": "/admin/api/headpastor/"},
                    {"title": "Leadership", "icon": "groups", "link": "/admin/api/leader/"},
                    {"title": "Sermons", "icon": "menu_book", "link": "/admin/api/sermon/"},
                    {"title": "Events", "icon": "event", "link": "/admin/api/event/"},
                ],
            },
            {
                "title": "Administration",
                "items": [
                    {"title": "Branches", "icon": "account_balance", "link": "/admin/api/branch/"},
                    {"title": "Service Times", "icon": "schedule", "link": "/admin/api/servicetime/"},
                    {"title": "Giving", "icon": "volunteer_activism", "link": "/admin/api/givinginfo/"},
                    {"title": "Messages", "icon": "mail", "link": "/admin/api/contactmessage/"},
                ],
            },
        ],
    },
}