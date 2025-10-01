# mcqmaster/settings.py

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url  # ডেটাবেস URL পার্স করার জন্য এটি ইম্পোর্ট করুন

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# .env ফাইল থেকে এনভায়রনমেন্ট ভেরিয়েবল লোড করুন (শুধুমাত্র লোকাল ডেভেলপমেন্টের জন্য)
load_dotenv()

# --- প্রোডাকশনের জন্য গুরুত্বপূর্ণ পরিবর্তন ---

# 1. SECRET_KEY: এটি এখন সরাসরি কোডে লেখা থাকবে না।
# Vercel-এর Environment Variable থেকে এটি আসবে।
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-for-local-dev')

# 2. DEBUG: Vercel-এ এটি স্বয়ংক্রিয়ভাবে 'False' থাকবে।
# লোকাল ডেভেলপমেন্টের জন্য 'True' থাকবে।
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# 3. ALLOWED_HOSTS: আপনার Vercel ডোমেইন এবং লোকাল হোস্ট এখানে থাকবে।
# Vercel নিজে থেকেই তার ডোমেইন যোগ করে, তবে এটি যোগ করা ভালো অভ্যাস।
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')


# --- Application definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # WhiteNoise-এর জন্য এটি যোগ করুন
    'django.contrib.staticfiles',
    'quiz',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # SecurityMiddleware-এর ঠিক পরেই এটি যোগ করুন
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mcqmaster.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mcqmaster.wsgi.application'


# --- Database ---
# 4. ডেটাবেস কনফিগারেশন: Vercel-এর জন্য একটিমাত্র URL ব্যবহার করা হবে।
import dj_database_url
import os

if os.environ.get("DATABASE_URL"):
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
    }
else:
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


# --- Static files (CSS, JavaScript, Images) ---
# 5. স্ট্যাটিক ফাইল কনফিগারেশন
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# আপনার `static` ফোল্ডারটি এখানে উল্লেখ করা আছে, যা ঠিক আছে।
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files (যদি ব্যবহার করেন)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# --- অন্যান্য সেটিংস ---
AUTH_USER_MODEL = 'quiz.CustomUser'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'quiz.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Password validation (অপরিবর্তিত)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization (অপরিবর্তিত)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

