from pathlib import Path
import os




BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-w-h!btx5q0^7oziy7-*s5(owe%pemqw4ph8w%5k006l1qu8xcx'

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'essentialthreads.netlify.app',   
    'essentialthreads-backend.onrender.com',
]





INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'corsheaders',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'store',
]

STRIPE_PUBLISHABLE_KEY = 'pk_test_51RTSVv4ERU9xOMUAKNWyazOz2R6y09usbqHtYWdz7x5x6aKMuzoCppHUVrPfhOs8TAPrKeLVzzGJ2aslS6zzoFOd00xfhSUT2V'  
STRIPE_SECRET_KEY = 'sk_test_51RTSVv4ERU9xOMUAp8yi8jKFLs54koDCzJEfOSK6TswyVebsleSjHskmSuinqqp9U20Lz2IuwG8g0U1A19JEXIv500AX59KjfI'      
STRIPE_WEBHOOK_SECRET ='whsec_IQ1Zi0GkM5OKzBRlpU0bq15ddGT9CztT' 

PAYPAL_CLIENT_ID='AQGPxvo3Xf0SQcxSSdBiEBLn7N_dKXOWW7JTwVZR-Fz1FMr1yv2i57LmF8YlxWTzGUq55rwORX0g7-vJ'
PAYPAL_CLIENT_SECRET='EGIvbiQQRMbtqrsLViGQ-YmLk02dXZMyadgBZN-RWtkzyVZgihRL_pfmxI37S2WyyFK2JsSOl-NGyR-N'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'essentialThreads',
        'USER': 'postgres',
        'PASSWORD': 'newpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://essentialthreads.netlify.app",
]



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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

