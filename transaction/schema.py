from typing import Optional
from ninja import ModelSchema, Schema
from pydantic import Field

from transaction.models import Transaction


class TransactionOut(ModelSchema):
    amount: int
    class Meta:
        model = Transaction
        fields = ['id', 'budget', 'wallet', 'amount', 'note', 'category', 'transaction_date']


class TransactionIn(ModelSchema):
    wallet: int = Field(..., alias='wallet_id')
    category: int = Field(..., alias='category_id')
    amount: int
    transaction_date: Optional[str] = None

    class Meta:
        model = Transaction
        fields = ['wallet', 'budget', 'amount', 'note', 'category', 'transaction_date']


class TransactionUpdateSchema(Schema):
    wallet_id: Optional[int] = None
    amount: Optional[int] = None
    category_id: Optional[int] = None
    note: Optional[str] = None
    budget_id: Optional[int] = None
