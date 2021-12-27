from __future__ import absolute_import, unicode_literals

from celery import Celery
from datetime import datetime, timedelta

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paywok.settings')

app = Celery('paywok')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.timezone = 'Europe/Madrid'

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
