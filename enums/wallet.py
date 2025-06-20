from enum import Enum

class WalletType(str, Enum):
    CASH = 'CASH'
    BANK = 'BANK'
    SAVING = 'SAVING'
    BUDGET = 'BUDGET'
