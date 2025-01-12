from typing import ClassVar

from ninja import ModelSchema, Schema
from budget.models import Budget
from category.schema import CategorySchema


class BudgetSchema(ModelSchema):
    category: CategorySchema = None
    class Meta:
        model = Budget
        fields = ['id', 'user', 'amount', 'category', 'start_date', 'end_date']



class BudgetCreateSchema(ModelSchema):
    class Meta:
        model = Budget
        fields = ['amount', 'category', 'start_date', 'end_date']
