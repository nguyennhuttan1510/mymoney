from typing import List, Optional, Type
from django.db.models import Model, QuerySet
from django.contrib.auth.models import User
from typing import List, Optional, Generic, TypeVar
from transaction.models import Transaction
from utils import query_strategy
from utils.query_builder import Specification
from utils.query_strategy import QueryStrategy, DefaultQueryStrategy

T = TypeVar('T')

class Repository(Generic[T]):
    def __init__(self, model, query_strategy: QueryStrategy = None):
        self.model = model
        self.query_strategy = query_strategy or DefaultQueryStrategy()

    def create(self, data: dict) -> T:
        return self.model.objects.create(**data)

    def get_all(self) -> List[T]:
        return self.model.objects.all()

    def filter(self, specification: Specification[T]) -> QuerySet[T]:
        query = self.query_strategy.execute(specification)
        return self.model.objects.filter(query)

    def get_by_id(self, pk: int, *args, **kwargs) -> Optional[T]:
        return self.model.objects.get(pk=pk, *args, **kwargs)

    def update(self, instance: T, data: dict) -> Optional[T]:
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, pk:int):
        instance = self.get_by_id(pk=pk)
        return instance.delete()





