"""
Django settings for video_microservice project.
"""

import os
from pathlib import Path
import boto3

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
DEBUG = True
#DEBUG = False

ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1', '52.207.108.185']

# SECURITY WARNING: keep the secret key used in production secret!


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_extensions',
    'videos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'video_microservice.urls'

# Updated template configuration to include 'video-frontend' for direct HTML serving
SECRET_KEY = 'django-insecure-6q_2a=en*6xk7)a@k&ujc2t42@-wqa#(yck$rqj-*lqcc^f-)b'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
#            BASE_DIR / 'video-frontend',  # Include video-frontend for serving HTML files
#            os.path.join(BASE_DIR, 'video-frontend')
        ],
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

WSGI_APPLICATION = 'video_microservice.wsgi.application'

# Database configuration (set to dummy since you're using DynamoDB)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
#STATICFILES_DIRS = [BASE_DIR / 'video-frontend' / 'static']

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AWS Configuration
AWS_STORAGE_BUCKET_NAME = 'webpage-uploads-2'
AWS_S3_REGION_NAME = 'us-east-1'

# boto3 S3 client for fetching posters and videos
s3 = boto3.client(
    's3',
    region_name=AWS_S3_REGION_NAME
)

# boto3 DynamoDB resource for tracking video metadata
dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_S3_REGION_NAME
)

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://52.207.108.185:5000",
    "http://localhost:8001",
    "http://127.0.0.1:8001",
    "http://localhost:5000",
    "http://52.207.108.185:8001"
]
CORS_ALLOW_ALL_ORIGINS = True

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
