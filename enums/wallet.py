from enum import Enum
from django.db import models

class WalletType(str, Enum):
    CASH = 'CASH'
    BANK = 'BANK'
    SAVING = 'SAVING'
