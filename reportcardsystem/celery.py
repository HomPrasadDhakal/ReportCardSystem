import os
from celery import Celery
import django 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reportcardsystem.settings')
django.setup()

app = Celery('reportcardsystem')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
