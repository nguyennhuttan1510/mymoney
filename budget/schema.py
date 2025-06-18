
from ninja import ModelSchema, Schema
from pydantic import Field

from budget.models import Budget
from category.schema import CategorySchema
from wallet.schema import WalletOut


class BudgetOut(ModelSchema):
    category: CategorySchema
    wallet: WalletOut
    amount: float

    class Meta:
        model = Budget
        fields = ['id', 'wallet', 'amount', 'category', 'start_date', 'end_date']


class BudgetIn(ModelSchema):
    amount: float
    wallet: int = Field(..., alias='wallet_id')
    category: int = Field(..., alias='category_id')

    class Meta:
        model = Budget
        fields = ['wallet', 'amount', 'category', 'start_date', 'end_date']


class BudgetParam(Schema):
    wallet_id: int = None
    category_id: int = None
