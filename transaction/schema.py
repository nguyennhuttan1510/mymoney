from datetime import datetime
from typing import Optional, Union, Literal, Any
from ninja import ModelSchema, Schema
from pydantic import Field, BaseModel, field_serializer, computed_field

from transaction.models import Transaction


class TransactionOut(ModelSchema):
    amount: int

    class Meta:
        model = Transaction
        fields = ['id', 'budget', 'wallet', 'amount', 'note', 'category', 'transaction_date']


class GroupByTransaction(BaseModel):
    count: int = None
    total: float = None
    name: str = None


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
    budget_id: int | None = Field(default=None,
                                  exclude=True)  # must be set Field(...,exclude=True) with field that is use handle logic ex: budget_id
    group_by: Literal['category', 'wallet'] | None = Field(default=None, exclude=True)


# class TransactionStatistical(BaseModel):


class TransactionOutCalculate(BaseModel):
    transactions: list[TransactionOut]
    count: int
