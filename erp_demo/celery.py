# erp_demo/celery.py

import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_demo.settings')

# Create Celery app
app = Celery('erp_demo')

# Load custom config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in all registered Django app configs
app.autodiscover_tasks()
