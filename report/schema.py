from typing import Optional, List

from ninja import Schema

from budget.schema import BudgetSchema
from transaction.schema import TransactionSchema
from wallet.models import Wallet
from wallet.schema import WalletResponse


class ReportWalletTransaction(Schema):
    wallet: WalletResponse
    transactions: List[TransactionSchema]

class ResponseBudgetTransaction(Schema):
    budget: BudgetSchema
    transactions: List[TransactionSchema]
    spent: int
    remaining: int
    percentage_spent: int
    percentage_remaining: int