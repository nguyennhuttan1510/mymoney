from typing import Optional

from django.db.models import Q, QuerySet
from ninja import Query

from budget.models import Budget
from budget.schema import BudgetQueryParam, BudgetDeleteIn
from utils.query_builder import Specification, QueryBuilder
from core.dao.repository import Repository, T

class BudgetSpecification(Specification[Budget]):
    def __init__(self, params: Query[BudgetQueryParam]):
        self.params = params
        self.builder = QueryBuilder()

    def is_satisfied(self) -> Q:
        params_dict = self.params.model_dump(exclude_unset=True, exclude={'wallets', 'categories'})
        # build base query
        self.base_query(params_dict, builder=self.builder)
        # build a relationship query
        if self.params.wallets:
            self.builder.add_relation_condition('wallet', self.params.wallets)
        if self.params.categories:
            self.builder.add_relation_condition('category', self.params.categories)
        return self.builder.build()


class BudgetDeleteSpecification(Specification[Budget]):
    def __init__(self, params: BudgetDeleteIn):
        self.params = params
        self.builder = QueryBuilder()

    def is_satisfied(self) -> Q:
        if self.params.ids:
            self.builder.add_relation_condition('pk', self.params.ids)
        return self.builder.build()


class BudgetRepository(Repository[Budget]):
    def __init__(self):
        super().__init__(model=Budget)

    def create(self, data: dict):
        categories = data.pop('categories', None)
        wallets = data.pop('wallets', None)
        instance = super().create(data)
        if categories:
            instance.category.set(categories)
        if wallets:
            instance.wallet.set(wallets)
        return instance

    def search(self, params: Query[BudgetQueryParam]):
        specification = BudgetSpecification(params)
        return self.filter(specification)

    def update(self, instance: T, data: dict) -> Optional[T]:
        categories = data.pop("categories", None)
        wallets = data.pop("wallets", None)
        if categories:
            instance.category.set(categories)
        if wallets:
            instance.wallet.set(wallets)
        super().update(instance, data)
        return instance

    def delete(self, instance: QuerySet[T]):
        instance.delete()

