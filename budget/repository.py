from typing import Optional

from django.db.models import Q
from ninja import Query

from budget.models import Budget
from budget.schema import BudgetParam
from utils.repository import Repository, T


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
        query = Q()
        params_dict = params.model_dump(exclude_unset=True, exclude={'wallets', 'categories'})
        for k, v in params_dict.items():
            if isinstance(v, list): pass
            query &= Q(**{k:v})
        if params.wallets:
            query &= Q(wallet__in=params.wallets)
        if params.categories:
            query &= Q(category__in=params.categories)
        return self.filter(query)

    def update(self, instance: T, data: dict) -> Optional[T]:
        categories = data.pop("categories", None)
        wallets = data.pop("wallets", None)
        if categories:
            instance.category.set(categories)
        if wallets:
            instance.wallet.set(wallets)
        super().update(instance, data)
        return instance
