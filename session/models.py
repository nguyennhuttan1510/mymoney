import uuid
from datetime import timedelta
from django.utils import timezone

from django.conf import settings
from django.db import models

# Create your models here.
class Session(models.Model):
    session_id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sessions')
    is_active = models.BooleanField(default=True)
    ipaddress = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True, max_length=50)
    expires_at = models.DateTimeField(blank=True, null=True)
    revoked_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=["user", "is_active"]),
        ]

    def __str__(self):
        return self.session_id

    def save(self, **kwargs):
        self.expires_at = timezone.now() + timedelta(seconds=settings.SESSION_EXPIRE_MINUTES)
        print('expires_at', self.expires_at)
        super().save(**kwargs)
