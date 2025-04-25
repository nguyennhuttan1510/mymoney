from django.contrib.auth.models import User
from django.db import models

from core.models.datetime import Datetime
from enums.wallet import WalletType


# Create your models here.
class Wallet(Datetime):
    name = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    user = models.ForeignKey(User, related_name='wallets', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=WalletType.choices)