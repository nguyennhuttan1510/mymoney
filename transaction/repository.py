from typing import List, Literal

from django.db.models import Q, Model, QuerySet, Sum, Count
from ninja import Query

from transaction.models import Transaction
from transaction.schema import TransactionQueryParams, GroupByTransaction
from utils.repository import Repository


class TransactionRepository(Repository):
    def __init__(self):
        super().__init__(model=Transaction)

    def get_all_for_user(self, params: TransactionQueryParams):
        q_o2m = Q()
        if params.categories:
            q_o2m &= Q(category__in=params.categories)
        if params.wallets:
            q_o2m &= Q(wallet__in=params.wallets)
        if params.start_date and params.end_date:
            q_o2m &= Q(transaction_date__range=(params.start_date, params.end_date))
        # must be use model_dump to auto exclude param handle logic
        scalar_filters = params.model_dump(exclude={'wallets', 'categories', 'start_date', 'end_date'}, exclude_none=True)
        return self.filter(q_o2m, **scalar_filters)

    @staticmethod
    def group_by(query:QuerySet[Transaction], group_by: Literal['category', 'wallet']= 'category') -> list[
        GroupByTransaction]:
        calc = query.values(group_by, 'category__name', 'wallet__name').annotate(
            total=Sum('amount'),
            count=Count('id')
        )
        result: list[GroupByTransaction] = list(calc)
        return result

    @staticmethod
    def sum_amount(query: QuerySet[Transaction]):
        return query.aggregate(total=Sum('amount'))['total'] or 0



