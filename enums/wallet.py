from enum import Enum
from django.db import models

class WalletType (models.TextChoices):
    CASH = 'CASH', 'cash'
    BANK = 'BANK', 'bank'
    SAVINGS = 'SAVINGS', 'savings'