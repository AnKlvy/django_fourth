import os
import logging
from celery import Celery, shared_task
from kombu import Connection, Consumer, Queue
from kombu.exceptions import OperationalError

# Устанавливаем настройки для Celery, включая настройку брокера RabbitMQ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_fourth.settings')

app = Celery('django_fourth')

# Используем RabbitMQ в качестве брокера
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True

# Загружаем задачи из всех зарегистрированных приложений Django
app.autodiscover_tasks()




