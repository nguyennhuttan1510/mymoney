from ninja import Schema, ModelSchema
from pydantic import BaseModel

from category.models import Category
from enums.transaction import TransactionType


class CategoryOut(Schema):
    id: int
    name: str
    type: TransactionType