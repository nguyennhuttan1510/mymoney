from enum import Enum

from django.db import models

from category.models import Category
from core.models.datetime import Datetime
from utils.common import TransactionType


# Create your models here.
class Transaction(Datetime):
    transaction_type = models.CharField(choices=TransactionType.get_choices(), default=TransactionType.EXPENSE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(null=True, default=None)
    transaction_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name='transactions')