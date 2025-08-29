from datetime import datetime
from typing import Optional, List

from ninja import Schema
from pydantic import BaseModel, Field

from budget.schema import BudgetOut
from enums.transaction import TransactionType
from transaction.schema import TransactionReportGenerate
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


class ReportIn(BaseModel):
    start_date: datetime
    end_date: datetime


class ReportOut(BaseModel):
    start_date: datetime | None = None
    end_date: datetime | None = None
    categories: list[CategoryReport] | None = None
    wallets: list[WalletReport] | None = None
    transactions: list[TransactionReportGenerate] | None = None
    total: float | None = None
    count_transaction: int | None = None


class ResponseBudgetTransaction(Schema):
    budget: BudgetOut
    transactions: list[TransactionReportGenerate]
    spent: int
    remaining: int
    percentage_spent: float
    percentage_remaining: float
