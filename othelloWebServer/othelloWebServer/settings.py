"""
Django settings for othelloWebServer project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hzgck8(^u5il2_)8m#v35ypo@(&myh!d*dsbto(_30%$iba0dl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','localhost','group02.dhcp.nd.edu','10.173.222.96']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.corsheaders'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'corsheaders.middleware.CorsMiddleware',
    #'django.middleware.common.CommonMiddleware'
)

TEMPLATES = [{
	'BACKEND' : 'django.template.backends.django.DjangoTemplates',
	'DIRS' : [os.path.join(BASE_DIR, 'othello/templates')],
	'APP_DIRS' : False,
	'OPTIONS' : {
		'context_processors': [
			'django.template.context_processors.debug',
			'django.template.context_processors.request',
			'django.contrib.auth.context_processors.auth',
			'django.contrib.messages.context_processors.messages',
		],
		'loaders': [
			'django.template.loaders.filesystem.Loader',
			'django.template.loaders.app_directories.Loader',
		],
                #'debug': DEBUG
	},
}]

ROOT_URLCONF = 'othelloWebServer.urls'

WSGI_APPLICATION = 'othelloWebServer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.postgresql_psycopg2',
	#'OPTIONS' : {
#		'options' : '-c search_path=fuzzytoads'
#	},
	'NAME'     : 'othello',
	'USER'     : 'othellouser',
	'PASSWORD' : 'password',
	'HOST'     : 'localhost',
	'PORT'     : '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

#STATIC_URL = 'http://group02.dhcp.nd.edu/static/'

STATIC_ROOT = '/home/djasek/othelloAI/othelloWebServer/othello/static'
STATIC_URL = '/static/'
#STATICFILES_DIRS = ( os.path.join('static'), )

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

#CORS_ORIGIN_ALLOW_ALL = True   
