from datetime import datetime
from typing import Union, List

from ninja import ModelSchema, Schema
from pydantic import Field

from budget.models import Budget
from category.schema import CategorySchema
from wallet.schema import WalletOut, WalletIn


class BudgetOut(ModelSchema):
    category: CategorySchema
    wallet: WalletOut
    amount: float

    class Meta:
        model = Budget
        fields = ['id', 'wallet', 'amount', 'category', 'description', 'start_date', 'end_date']


class BudgetIn(ModelSchema):
    name: str
    amount: float
    wallet: list[int] = Field(..., alias='wallets')
    category: list[int] = Field(..., alias='categories')

    class Meta:
        model = Budget
        fields = ['wallet', 'amount', 'category', 'start_date', 'end_date']

class BudgetUpdate(Schema):
    category_id: int = None
    amount: float = None
    description: str = None
    start_date: datetime = None
    end_date: datetime = None


class BudgetParam(Schema):
    wallet_id: int = None
    category_id: int = None
    amount: float = None
    user_id: int = None
