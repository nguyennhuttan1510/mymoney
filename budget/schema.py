from datetime import datetime
from typing import Union, List

from ninja import ModelSchema, Schema
from pydantic import Field, BaseModel, computed_field

from budget.models import Budget
from category.schema import CategoryOut
from enums.budget import BudgetStatus
from wallet.schema import WalletOut, WalletIn


class BudgetOut(Schema):
    id: int
    categories: list[CategoryOut] = Field(..., alias='category')
    wallets: list[WalletOut] = Field(..., alias='wallet')
    amount: float
    description: str | None = None
    start_date: datetime
    end_date: datetime


class BudgetIn(BaseModel):
    name: str
    amount: float
    wallet: list[int] | None = Field(default=None, alias='wallets')
    category: list[int] | None = Field(default=None, alias='categories')
    start_date: datetime = Field(default=datetime.now())
    end_date: datetime = Field(default=datetime.now())


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


class BudgetOutCalculate(BudgetOut):
    total_spent: float
    limit: float  # the same amount

    @computed_field
    @property
    def remaining(self) -> float:
        return self.limit - self.total_spent

    @computed_field
    @property
    def usage_percent(self) -> float:
        return round(float((self.total_spent/self.limit) * 100), 2)

    @computed_field
    @property
    def remaining_percent(self) -> float:
        return round(float((self.remaining/self.limit) * 100), 2)

    @computed_field
    @property
    def status(self) -> BudgetStatus:
        if self.usage_percent > 100:
            return BudgetStatus.OVER
        elif self.usage_percent >= 80:
            return BudgetStatus.WARNING
        else:
            return BudgetStatus.OK


class BudgetParam(BaseModel):
    is_calc: bool = Field(default=False, description='if true return Schema BudgetOutWithCalculate else BudgetOut')


class BudgetDeleteIn(BaseModel):
    ids: list[int]

