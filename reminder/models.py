from django.contrib.auth.models import User
from django.db import models

from core.models.datetime import Datetime


# Create your models here.
class Reminder(Datetime):
    user = models.ForeignKey(User, related_name='reminders', on_delete=models.CASCADE)
    message = models.CharField(max_length=250)
    remain_at = models.DateTimeField()
    is_completed = models.BooleanField(default=False)