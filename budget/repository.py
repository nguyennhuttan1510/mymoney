from typing import Optional

from django.db.models import Q
from ninja import Query

from budget.models import Budget
from budget.schema import BudgetParam
from utils.query_builder import Specification, QueryBuilder
from utils.repository import Repository, T

class BudgetSpecification(Specification[Budget]):
    def __init__(self, params: Query[BudgetParam]):
        self.params = params
        self.builder = QueryBuilder()
    def is_satisfied(self) -> Q:
        params_dict = self.params.model_dump(exclude_unset=True, exclude={'wallets', 'categories'})
        # build base query
        for k, v in params_dict.items():
            if isinstance(v, list): pass
            self.builder.add_condition(k, v)
        # build a relationship query
        if self.params.wallets:
            self.builder.add_relation_condition('wallet', self.params.wallets)
        if self.params.categories:
            self.builder.add_relation_condition('category', self.params.categories)
        return self.builder.build()


class BudgetRepository(Repository[Budget]):
    def __init__(self):
        super().__init__(model=Budget)

    def create(self, data: dict) -> T:
        categories = data.pop('category', None)
        wallets = data.pop('wallet', None)
        instance = super().create(data)
        instance.category.set(categories)
        instance.wallet.set(wallets)
        return instance

    def get_all_for_user(self, user_id, params: Query[BudgetParam]):
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
