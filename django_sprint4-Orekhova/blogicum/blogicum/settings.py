from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xn5)z4fdefk$^j!_&-!xukk-d@@eprv!nes2l_wp5f2=6_!l(a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Установите False при переходе на продакшн

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

# Media files (for user-uploaded content like images)
MEDIA_URL = '/media/'  # URL для доступа к медиа-файлам
MEDIA_ROOT = BASE_DIR / 'media'  # Директория хранения медиа-файлов

# Static files (CSS, JavaScript, images)
STATIC_URL = '/static/'  # URL для статических файлов
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Папка со статикой для разработки
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Папка для collectstatic при продакшн-использовании

# Login and authentication
LOGIN_REDIRECT_URL = 'blog:index'  # Куда перенаправлять после успешного входа
LOGIN_URL = 'login'  # URL для страницы входа

# CSRF custom error view
CSRF_FAILURE_VIEW = 'pages.views.csrf_failure'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',  # Ваше приложение
    'pages.apps.PagesConfig',  # Ваше приложение
    'django_bootstrap5',  # Библиотека для работы с Bootstrap
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blogicum.urls'

TEMPLATES_DIR = BASE_DIR / 'templates'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'blogicum.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
