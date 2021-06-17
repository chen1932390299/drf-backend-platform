"""
Django settings for rookie project.

Generated by 'django-admin startproject' using Django 2.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^c8&g-i8npx3yzrq0$=srzfkacdo9t!$-sov$caui&ry@a9&39'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','192.168.96.55']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'drf_yasg', # swagger doc
    'django_filters',
    "django_redis",  # redis
    'mysite',
    'django_apscheduler', #  cron
    'django_mysql'



]

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # FIX CSRF
    'django.middleware.common.CommonMiddleware', #
    'django.middleware.csrf.CsrfViewMiddleware',  # 跨域
    # 'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rookie.urls'

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

WSGI_APPLICATION = 'rookie.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "mall",
        'USER': 'root',
        'PASSWORD': 'App@123456',
        'HOST': '192.168.110.151',
        'PORT': '3306',
        'OPTIONS': {
            # Tell MySQLdb to connect with 'utf8mb4' character set
            'charset': 'utf8mb4',
            # 'isolation_level': None
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'zh-hans' # 语言
TIME_ZONE = 'Asia/Shanghai'  # 时区
USE_I18N = True  # 国际化
USE_L10N = True   # 本地化
USE_TZ = False   #
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
REST_FRAMEWORK={

    # "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    # "DEFAULT_VERSION": 'v1',  # 默认为1
    # "ALLOWED_VERSIONS": ['v1', 'v2'],  # 仅允许v1或者v2访问
    # "VERSION_PARAM": 'version',
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",   # application/json
        "rest_framework.parsers.FormParser",  # application/x-www-form-urlencoded
        'rest_framework.parsers.MultiPartParser', # multipart/form-data
        "rest_framework.parsers.FileUploadParser" # with a single key 'file' containing the uploaded file.
        ],
    # 自定义分页器
    'DEFAULT_PAGINATION_CLASS':  'utils.pagenation.ListPagination',
    #'rest_framework.pagination.PageNumberPagination',
    #'PAGE_SIZE': 10,

    # 过滤器
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'EXCEPTION_HANDLER': 'utils.custom_exception_handler.exception_handler',
    # output format of datetime
    'DATETIME_FORMAT':'%Y-%m-%d %H:%M:%S',
    # input datetime format
    "DATETIME_INPUT_FORMATS":'%Y-%m-%d %H:%M:%S',

}


# 内置加密make_password
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)


# django-redis
CACHES = {
    "default": {
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": "redis://192.168.110.151:6379/0",
    "OPTIONS": {
    "CLIENT_CLASS": "django_redis.client.DefaultClient",
    "CONNECTION_POOL_KWARGS": {"max_connections": 100},
    "SOCKET_CONNECT_TIMEOUT": 10,  # connect in seconds
    "SOCKET_TIMEOUT": 10,  # r+w timeout seconds
    # "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
    }
            }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CORS_ORIGIN_ALLOW_ALL = True

# chrome slash switch 
# APPEND_SLASH=True
