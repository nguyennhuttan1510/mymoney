from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class UserProvider(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='provider_accounts')
    provider = models.CharField(max_length=50)
    provider_account_id = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    profile_data = models.JSONField(null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    expires_in = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    scopes = models.TextField(null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('provider', 'provider_account_id',)
        indexes = [
            models.Index(fields=['provider', 'provider_account_id']),
            models.Index(fields=['user']),
        ]
