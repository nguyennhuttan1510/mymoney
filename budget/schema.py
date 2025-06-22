from datetime import datetime
from typing import Union, List

from ninja import ModelSchema, Schema
from pydantic import Field

from budget.models import Budget
from category.schema import CategorySchema
from enums.budget import BudgetStatus
from wallet.schema import WalletOut, WalletIn


class BudgetOut(ModelSchema):
    categories: list[CategorySchema] = Field(..., alias='category')
    wallets: list[WalletOut] = Field(..., alias='wallet')
    amount: float
    start_date: datetime
    end_date: datetime

    class Meta:
        model = Budget
        fields = ['id', 'amount', 'description', 'start_date', 'end_date']


class BudgetIn(ModelSchema):
    name: str
    amount: float
    wallet: list[int] = Field(..., alias='wallets')
    category: list[int] = Field(..., alias='categories')
    start_date: datetime = Field(default=datetime.now())
    end_date: datetime = Field(default=datetime.now())

    class Meta:
        model = Budget
        fields = ['wallet', 'amount', 'category', 'start_date', 'end_date']


class BudgetUpdate(Schema):
    categories: list[int] = None
    wallets: list[int] = None
    amount: float = None
    description: str = None
    start_date: datetime = None
    end_date: datetime = None


class BudgetParam(Schema):
    wallets: list[int] = None
    categories: list[int] = None
    amount: float = None
    user_id: int = None


class BudgetOutWithCategory(BudgetOut):
    total_spent: float | None = None
    limit: float | None = None# the same amount
    usage_percent: int | None = None
    status: BudgetStatus | None = None
