from django.contrib.auth.models import User
from django.db import models

from core.models.datetime import Datetime
from utils.common import TransactionType


# Create your models here.
class Category(Datetime):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(choices=TransactionType.get_choices(), default=TransactionType.INCOME, max_length=20)
    icon = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, related_name="category", on_delete=models.SET_NULL, null=True, blank=True)