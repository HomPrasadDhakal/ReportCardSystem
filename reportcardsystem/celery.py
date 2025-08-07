import os
import django
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reportcardsystem.settings')
django.setup()

app = Celery('reportcardsystem')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'daily-term-summary-update': {
        'task': 'students.tasks.calculate_student_term_summaries', 
        'schedule': crontab(hour=1, minute=0),
    },
}
