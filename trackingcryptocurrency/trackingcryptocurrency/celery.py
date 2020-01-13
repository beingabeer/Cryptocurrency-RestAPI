import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trackingcryptocurrency.settings")

app = Celery("trackingcryptocurrency")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
