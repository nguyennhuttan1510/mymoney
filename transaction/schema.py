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
    wallet_id: int
    note: str | None = None
    category_id: int
    transaction_date: datetime
    balance: float


class TransactionReport(Schema):
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
    total: float = 0

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


class TransactionQuery(BaseModel):
    categories: list[int] = None
    wallets: list[int] = None
    start_date: datetime = None
    end_date: datetime = None
    budget_id: int | None = Field(exclude=True, default=None, description='Get transaction by budget')

