from datetime import datetime
from typing import Union, List

from ninja import ModelSchema, Schema
from pydantic import Field, BaseModel

from budget.models import Budget
from category.schema import CategoryOut
from enums.budget import BudgetStatus
from wallet.schema import WalletOut, WalletIn


class BudgetOut(ModelSchema):
    categories: list[CategoryOut] = Field(..., alias='category')
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


class BudgetQueryParam(Schema):
    wallets: list[int] = None
    categories: list[int] = None
    amount: float = None
    user_id: int = None


class CalculatorBudget(BaseModel):
    total_spent: float
    limit: float  # the same amount
    usage_percent: int
    status: BudgetStatus


class BudgetParam(BaseModel):
    is_calc: bool = Field(default=False, description='if true return Schema BudgetOutWithCalculate else BudgetOut')


class BudgetDeleteIn(BaseModel):
    ids: list[int]


class BudgetOutWithCalculate(BudgetOut, CalculatorBudget):
    pass
