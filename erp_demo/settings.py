 
from pathlib import Path
import pymysql
pymysql.install_as_MySQLdb()

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ERP_NEXT_URL = os.getenv("ERP_URL")
ERP_API_KEY = os.getenv("ERP_API_KEY")
ERP_API_SECRET = os.getenv("ERP_API_SECRET")

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-7+ug312elp@(*oa#*x$0e+x-&9*13-2$*46@r6w)nh%*j&khtj'
DEBUG = True
ALLOWED_HOSTS = []


INSTALLED_APPS = [ 
    'dal',
    'dal_select2',            
    'erp',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    'auditlog', 
    "crispy_forms",
    "crispy_bootstrap4", 
    
]

AUTH_USER_MODEL = 'erp.Employee' 
# ERPNEXT API LOGIN
AUTHENTICATION_BACKENDS = ['sales_app.auth.ERPNextAuthBackend']
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Optional settings
IMPORT_EXPORT_USE_TRANSACTIONS = True  
IMPORT_EXPORT_SKIP_ADMIN_LOG = True    

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
        'NAME': 'autopros_erp',
        'USER': 'root', 
        'PASSWORD': 'autopro2025?', 
        'HOST': 'localhost', 
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
# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
FILE_UPLOAD_PERMISSIONS = 0o644
 
JAZZMIN_SETTINGS = { 
    # ============ Branding ============
    "site_title": "AutoZone Admin",  
    "site_header": "AutoZone ERP",  
    "site_brand": "AutoZone Pro", 
    "site_logo": "img/Logo.png",  
    "login_logo": "img/Logo.png", 
    "site_logo_classes": "img-fluid",  
    "copyright": "AutoZone Ltd",
    "user_avatar": None,
    
    # UI Customization
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    
     
    "topmenu_links": [
 
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
 
        {"name": "Support", "url": "#", "new_window": True},
 
        {"model": "auth.User"},
 
        {"app": "books"},
    ],
 
    "usermenu_links": [
        {"name": "Support", "url": "#", "new_window": True},
        {"model": "auth.user"}
    ],
 
    "show_sidebar": True, 
    "navigation_expanded": True, 
    "hide_apps": [], 
    "hide_models": [], 
    "order_with_respect_to": ["auth", "books", "books.author", "books.book"], 
    "custom_links": {
        "books": [{
            "name": "Make Messages", 
            "url": "make_messages", 
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },
 
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    }, 
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
 
    "related_modal_active": False,
 
    "custom_css": None,
    "custom_js": None, 
    "use_google_fonts_cdn": True, 
    "show_ui_builder": False, 
    "changeform_format": "horizontal_tabs", 
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"}, 
    "language_chooser": True,

    "notifications": {
        "pending_estimates": {
            "model": "erp.Estimate",
            "filters": {"status": "pending"},
            "icon": "fas fa-file-invoice",
            "text": "You have {} pending estimates",
        }
    },
  
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

LOGIN_URL = '/erpnext/login/'  # URL for your login view
LOGIN_REDIRECT_URL = '/sales/dashboard/'  # Redirect after successful login
LOGOUT_REDIRECT_URL = '/erpnext/login/'
 