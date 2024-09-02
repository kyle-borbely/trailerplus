from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trailersplus.settings")

app = Celery("tailersplus")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "footer_date": {
        "task": "home.tasks.footer_date",
        "schedule": crontab(minute=1, hour=0),
    },
    "Geo_up_to_date": {
        "task": "home.tasks.update_geoip2",
        "schedule": crontab(minute=0, hour=3),
    },
}
