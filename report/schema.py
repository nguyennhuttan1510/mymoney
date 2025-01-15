from typing import Optional, List

from ninja import Schema

from transaction.schema import TransactionSchema
from wallet.models import Wallet
from wallet.schema import WalletSchema


class ReportWalletTransaction(Schema):
    wallet: WalletSchema
    transactions: List[TransactionSchema]