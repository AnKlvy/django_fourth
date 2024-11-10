# my_project/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_fourth.settings')

app = Celery('django_fourth')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()