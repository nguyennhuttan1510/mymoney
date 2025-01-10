from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

from core.models.datetime import Datetime


# Create your models here.
class Saving(Datetime):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saving')
    name = models.CharField(max_length=150)
    target_amount = models.DecimalField(max_digits=2, max_length=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=2, max_length=10, decimal_places=2)
    deadline = models.DateTimeField(null=False, default=timezone.now)