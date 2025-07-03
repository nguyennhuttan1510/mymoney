from django.contrib.auth.models import User
from django.db import models
from django.db.models import Manager

from budget.models import Budget
from category.models import Category
from core.models.datetime import Datetime
from wallet.models import Wallet


# Create your models here.
class Transaction(Datetime):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(null=True, default=None)
    transaction_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name='transactions')
    user = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, related_name='transactions', on_delete=models.CASCADE, null=True, default=None)
