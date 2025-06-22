from django.db import models

from category.models import Category
from core.models.datetime import Datetime
from wallet.models import Wallet


# Create your models here.
class Budget(Datetime):
    name = models.CharField(max_length=50, default=None, null=True, blank=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    wallet = models.ManyToManyField(Wallet)
    category = models.ManyToManyField(Category)
