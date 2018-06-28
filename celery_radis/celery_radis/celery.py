from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_radis.settings')

app = Celery('celery_radis')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# celery.py

from celery.schedules import crontab
app.conf.beat_schedule = {
    'add-every-minute-contrab': {
        'task': 'app2.tasks.task_number_two',
        'schedule': crontab(),
        'args': (16, 16),
    },
    'add-every-5-seconds': {
        'task': 'app2.tasks.task_number_two',
        'schedule': 5.0,
        'args': (16, 16)
    },
    'add-every-30-seconds': {
        'task': 'app1.tasks.sub',
        'schedule': 30.0,
        'args': (16, 16)
    },
}
