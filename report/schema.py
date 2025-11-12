from datetime import datetime
from typing import Optional, List

from ninja import Schema
from pydantic import BaseModel, Field

from budget.schema import BudgetOut
from enums.transaction import TransactionType
from transaction.schema import TransactionReport, TransactionQuery
from wallet.models import Wallet
from wallet.schema import WalletOut


class CategoryReport(BaseModel):
    id: int | None = None
    name: str | None = None
    type: TransactionType | None = None
    percent: float | None = None
    total: float | None = None
    count: int | None = None


class WalletReport(CategoryReport):
    type: TransactionType | None = Field(exclude=True, default=None)


class ReportQuery(BaseModel):
    start_date: datetime
    end_date: datetime
    wallets: list[int] = None
    categories: list[int] = None


class ReportOut(BaseModel):
    start_date: datetime = Field(default_factory=datetime.now)
    end_date: datetime = Field(default_factory=datetime.now)
    categories: list[CategoryReport] = Field(default_factory=list)
    wallets: list[WalletReport] = Field(default_factory=list)
    transactions: list[TransactionReport] = Field(default_factory=list)
    total: float = 0.0
    count_transaction: int = 0

