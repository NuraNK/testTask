import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testTask.settings')

app = Celery('grafen')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.enable_utc = False
app.conf.timezone = "Asia/Almaty"