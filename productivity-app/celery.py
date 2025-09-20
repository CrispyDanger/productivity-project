import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'productivity-app.settings')

app = Celery('productivity-app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'make-post': {
            'task': 'social.tasks.make_post',
            'schedule': 60.0},
                        }
