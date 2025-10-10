# mcqmaster/settings.py

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# -------------------------------------------------------------------
# 🔧 Base setup
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env variables (only for local/dev)
load_dotenv()

# -------------------------------------------------------------------
# 🔒 Security Settings
# -------------------------------------------------------------------
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-for-local-dev')

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# -------------------------------------------------------------------
# 🧩 Installed Apps
# -------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # Static handling for local + prod
    'django.contrib.staticfiles',

    # Your custom app
    'quiz',
]

# -------------------------------------------------------------------
# ⚙️ Middleware
# -------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ⚡ Must be right after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------------------------------------------------
# 🌐 URL & Templates
# -------------------------------------------------------------------
ROOT_URLCONF = 'mcqmaster.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'mcqmaster.wsgi.application'

# -------------------------------------------------------------------
# 🗄️ Database Configuration
# -------------------------------------------------------------------
if os.environ.get("DATABASE_URL"):
    # Production: Use full database URL (e.g. from Vercel or Render)
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
    }
else:
    # Local development database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }

# -------------------------------------------------------------------
# 🎨 Static & Media Files
# -------------------------------------------------------------------
STATIC_URL = '/static/'

# Where your own static files are stored (CSS, JS)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Where collectstatic will output to (for deployment)
STATIC_ROOT = BASE_DIR / 'staticfiles_build' / 'static'

# WhiteNoise compressed static storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media (uploads, profile images, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -------------------------------------------------------------------
# 👥 Authentication
# -------------------------------------------------------------------
AUTH_USER_MODEL = 'quiz.CustomUser'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

AUTHENTICATION_BACKENDS = [
    'quiz.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# -------------------------------------------------------------------
# 🔐 Password Validation
# -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------------------------
# 🌍 Internationalization
# -------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# 🧱 Default Primary Key
# -------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------------------
# ✅ End of File
# -------------------------------------------------------------------
