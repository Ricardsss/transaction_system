import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "transaction_system.settings")
app = Celery("transaction_system")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
