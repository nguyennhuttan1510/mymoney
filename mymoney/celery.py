import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mymoney.settings")

celery_app = Celery("mymoney")

# Lấy cấu hình từ Django settings (prefix CELERY_)
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto discover tasks.py trong các app
celery_app.autodiscover_tasks()