# report/tasks.py
from celery import shared_task
from django.db.models import Avg, F
from .models import Mark
import time

@shared_task
def celery_test():
    print("background task running...")
    for i in range(1, 101):
        print(i)
        time.sleep(5)