from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mooclet_engine.settings.aws')
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mooclet_engine.settings.local')

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(300.0, get_qualtrics_data.s('self', {"qualtrics_survey": 1}), name='add every 10')



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))