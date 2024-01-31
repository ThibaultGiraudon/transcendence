import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, 'static'),
]


# HTTPS redirect for 42 API
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False


# Default profile picture
DEFAULT_IMAGE_PATH = '/usr/src/app/static/users/img/default.jpg'


# Date and Languages
TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGE_CODE = 'fr'


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Django secret key
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')


# Debug modes
DEBUG = bool(os.getenv('DEBUG', True))


# CRSF verification
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
	'http://localhost:8000',
	'https://localhost:8443',
]


# Application definition
INSTALLED_APPS = [
	'daphne',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'mainApp',
	'mainApp.templatetags.poll_extras',
	'channels',
]

AUTH_USER_MODEL = 'mainApp.CustomUser'

APPEND_SLASH=False


# Logging gestion
LOGGING = {
	"version": 1,
	"disable_existing_loggers": False,
	"handlers": {
		"console": {
			"class": "logging.StreamHandler",
		},
	},
	"root": {
		"handlers": ["console"],
		"level": "INFO",
	},
}

DJANGO_IGNORE_APP_READY_WARNINGS = True


# ASGI
ASGI_APPLICATION = 'mainProject.asgi.application'

CHANNEL_LAYERS = {
	"default": {
		"BACKEND": "channels.layers.InMemoryChannelLayer"
	},
}


# Middleware and Templates
MIDDLEWARE = [
	'django.middleware.common.CommonMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mainProject.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


# Database gestion
WSGI_APPLICATION = 'mainProject.wsgi.application'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.getenv('POSTGRES_DB', 'default_db_name'),
		'USER': os.getenv('POSTGRES_USER', 'default_db_user'),
		'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'default_db_password'),
		'HOST': os.getenv('DB_FOLDER', 'default_db_host'),
		'PORT': os.getenv('POSTGRES_PORT', '5432'),
	}
}

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
