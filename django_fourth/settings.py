"""
Django settings for django_fourth project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from environ import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(env_file=BASE_DIR / '.env.dev')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# Получение SECRET_KEY и DEBUG из окружения
SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS", default="localhost").split(" ")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Добавьте ваше приложение
    'django_fourth',
    'graphene_django',
    'storages',
    'celery',
    'kombu.transport',
]

GRAPHENE = {
    'SCHEMA': 'django_fourth.schema.schema'  # Путь к схеме
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_fourth.urls'

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

WSGI_APPLICATION = 'django_fourth.wsgi.application'

# Database
DATABASES = {
    "default": {
        "ENGINE": env("SQL_ENGINE", default="django.db.backends.postgresql"),
        "NAME": env("SQL_DATABASE", default=os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": env("SQL_USER", default="user"),
        "PASSWORD": env("SQL_PASSWORD", default="password"),
        "HOST": env("SQL_HOST", default="localhost"),
        "PORT": env("SQL_PORT", default="5432"),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = f'{env("MINIO_ACCESS_URL")}/{env("STATICFILES_LOCATION", default="static")}/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MEDIA_URL = f'{env("MINIO_ACCESS_URL")}/media/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = env("AWS_S3_URL")
MINIO_ACCESS_URL = env("MINIO_ACCESS_URL")

AWS_S3_FILE_OVERWRITE = env.bool("AWS_S3_FILE_OVERWRITE", default=False)
AWS_DEFAULT_ACL = None
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_QUERYSTRING_AUTH = env.bool("AWS_QUERYSTRING_AUTH", default=False)

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# class DisableMigrations:
#     def __contains__(self, item):
#         return True
#
#     def __getitem__(self, item):
#         return None
#
# MIGRATION_MODULES = DisableMigrations()

# Конфигурация брокера для Celery и RabbitMQ
RABBITMQ = {
    "PROTOCOL": "amqp", # in prod change with "amqps"
    "HOST": os.getenv("RABBITMQ_HOST", "rabbitmq"),
    "PORT": os.getenv("RABBITMQ_PORT", 5672),
    "USER": os.getenv("RABBITMQ_USER", "guest"),
    "PASSWORD": os.getenv("RABBITMQ_PASSWORD", "guest"),
}
CELERY_BROKER_URL = f"{RABBITMQ['PROTOCOL']}://{RABBITMQ['USER']}:{RABBITMQ['PASSWORD']}@{RABBITMQ['HOST']}:{RABBITMQ['PORT']}"
# CELERY_RESULT_BACKEND = 'rpc://'  # Использование RPC для передачи результатов задач
CELERY_ACCEPT_CONTENT = ['json']  # Поддержка формата JSON

BROKER_URL = os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')

CACHES = {
    'default' : {
        'BACKEND' : 'django_redis.cache.RedisCache' ,
        'LOCATION' : 'redis://127.0.0.1:6379/1' ,   # Используйте соответствующий URL-адрес сервера Redis
        'OPTIONS' : {
            'CLIENT_CLASS' : 'django_redis.client.DefaultClient' ,
        }
    }
}

CELERY_BROKER_URL = "amqp://guest:guest@rabbitmq:5672//"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_TASK_SENT_EVENT = True
