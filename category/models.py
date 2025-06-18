from django.contrib.auth.models import User
from django.db import models

from core.models.datetime import Datetime
from enums.transaction import TransactionType
from utils.common import get_choices


# Create your models here.
class Category(Datetime):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(choices=get_choices(TransactionType), default=TransactionType.INCOME, max_length=20)
    icon = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=True)
    user = models.ManyToManyField(User)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="children", null=True, blank=True)
