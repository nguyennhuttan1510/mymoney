from typing import Optional, List

from ninja import Schema

from budget.schema import BudgetOut
from transaction.schema import TransactionOut
from wallet.models import Wallet
from wallet.schema import WalletOut


class ReportWalletTransaction(Schema):
    wallet: WalletOut
    transactions: List[TransactionOut]

class ResponseBudgetTransaction(Schema):
    budget: BudgetOut
    transactions: List[TransactionOut]
    spent: int
    remaining: int
    percentage_spent: int
    percentage_remaining: int