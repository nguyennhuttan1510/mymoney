from django.contrib.auth.models import User
from django.db import models

from category.models import Category
from core.models.datetime import Datetime


# Create your models here.
class Budget(Datetime):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='budgets', null=True, blank=True)
    category = models.ForeignKey(Category, ondeletemodel=models.SET_NULL, related_name='budgets', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)