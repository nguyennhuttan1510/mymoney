from datetime import datetime
from typing import Optional, Literal
from ninja import ModelSchema, Schema
from pydantic import Field, BaseModel, computed_field

from category.schema import CategoryOut
from transaction.models import Transaction
from wallet.schema import WalletOut


class TransactionOut(Schema):
    id: int
    amount: float
    wallet: int = Field(..., alias='wallet.id')
    note: str | None = None
    category: int = Field(..., alias='category.id')
    transaction_date: datetime

    # class Config:
    #     from_attributes = True

class TransactionReportGenerate(Schema):
    amount: float
    wallet: str = Field(..., alias='wallet.name')
    category: CategoryOut
    transaction_date: datetime

class GroupByTransaction(BaseModel):
    id: int = None
    name: str = None
    count: int = None
    total: float = None


class TransactionListOut(BaseModel):
    transactions: list[TransactionOut]
    group_by: list[GroupByTransaction] | None = None
    total: float | None = None

    @computed_field
    @property
    def count(self) -> int:
        return len(self.transactions)


class TransactionIn(ModelSchema):
    wallet: int = Field(..., alias='wallet_id')
    category: int = Field(..., alias='category_id')
    amount: int = Field(default=0, ge=0)
    transaction_date: datetime = datetime.now()
    note: str = None

    class Meta:
        model = Transaction
        fields = ['wallet', 'budget', 'amount', 'note', 'category', 'transaction_date']


class TransactionUpdateSchema(Schema):
    wallet_id: Optional[int] = None
    amount: Optional[int] = None
    category_id: Optional[int] = None
    note: Optional[str] = None
    budget_id: Optional[int] = None


class TransactionQueryParams(BaseModel):
    categories: list[int] = None
    wallets: list[int] = None
    start_date: datetime = None
    end_date: datetime = None
    budget: int | None = Field(default=None, description='Get transaction by budget')
    by_budget_id: int | None = Field(default=None,
                                  exclude=True, description='Only get transaction in budget')  # must be set Field(...,exclude=True) with field that is use handle logic ex: budget_id
    group_by: Literal['category', 'wallet'] | None = Field(default=None, exclude=True)


# class TransactionStatistical(BaseModel):


class TransactionOutCalculate(BaseModel):
    transactions: list[TransactionOut]
    count: int
