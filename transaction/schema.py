from datetime import datetime
from typing import Optional
from ninja import ModelSchema, Schema
from pydantic import Field, BaseModel

from transaction.models import Transaction


class TransactionOut(ModelSchema):
    amount: int
    class Meta:
        model = Transaction
        fields = ['id', 'budget', 'wallet', 'amount', 'note', 'category', 'transaction_date']


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
    budget_id: int = None
