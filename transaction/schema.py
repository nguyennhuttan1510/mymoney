from typing import Optional

from ninja import Schema, ModelSchema

from category.schema import CategorySchema
from transaction.models import Transaction
from utils.common import TransactionType


class TransactionSchema(ModelSchema):
    category: Optional[CategorySchema] = None
    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'wallet',  'budget', 'amount', 'note', 'category', 'transaction_date']

class TransactionCreateSchema(ModelSchema):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'wallet',  'budget', 'amount', 'note', 'category', 'transaction_date']
        optional_fields = ['budget']

