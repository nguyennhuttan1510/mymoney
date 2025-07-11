from ninja import Schema, ModelSchema
from pydantic import BaseModel

from category.models import Category
from enums.transaction import TransactionType


class CategoryOut(BaseModel):
    id: int
    name: str
    type: TransactionType