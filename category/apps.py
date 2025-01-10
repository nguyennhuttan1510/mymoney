from django.apps import AppConfig
from django.conf import settings
from django.db import connection

class CategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'category'

    def ready(self):
        from . import signals


