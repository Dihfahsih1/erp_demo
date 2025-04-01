 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-7+ug312elp@(*oa#*x$0e+x-&9*13-2$*46@r6w)nh%*j&khtj'
DEBUG = True
ALLOWED_HOSTS = []


INSTALLED_APPS = [ 
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'erp',
    'auditlog', 
    'import_export'
] 

# Optional settings
IMPORT_EXPORT_USE_TRANSACTIONS = True  # Enable DB transactions
IMPORT_EXPORT_SKIP_ADMIN_LOG = True    # Reduce log clutter

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'erp_demo.urls'

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

WSGI_APPLICATION = 'erp_demo.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'erp_demo',
        'USER': 'root', 
        'PASSWORD': '', 
        'HOST': '127.0.0.1', 
        'PORT': '3306',
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


JAZZMIN_SETTINGS = {
    # General settings
    "site_title": "AutoZone ERP",
    "site_header": "AutoZone",
    "site_brand": "AutoZone Admin",
    "welcome_sign": "Welcome to AutoZone ERP Admin",
    "copyright": "AutoZone Ltd",
    
    # UI Customization
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    
    # Menu customization
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "erp.Customer"},
    ],

    "notifications": {
        "pending_estimates": {
            "model": "erp.Estimate",
            "filters": {"status": "pending"},
            "icon": "fas fa-file-invoice",
            "text": "You have {} pending estimates",
        }
    }
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "sidebar": "sidebar-dark-primary",
}

JAZZMIN_SETTINGS = {
    "custom_links": {
        "dashboard": [{
            "name": "Sales Analytics",
            "url": "/admin/sales-analytics/",
            "icon": "fas fa-chart-line",
        }]
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
 


STATIC_URL = '/static/' 
STATICFILES_DIRS = [
    BASE_DIR / 'static',   
]
STATIC_ROOT = BASE_DIR / 'staticfiles'   
MEDIA_URL = '/media/' 
MEDIA_ROOT = BASE_DIR / 'media'  
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
