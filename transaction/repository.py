from typing import List, Literal

from django.db.models import Q, Model, QuerySet, Sum, Count, F
from ninja import Query

from transaction.models import Transaction
from transaction.schema import TransactionQueryParams, GroupByTransaction
from utils.query_builder import Specification, QueryBuilder
from utils.repository import Repository

class TransactionSpecification(Specification[Transaction]):
    def __init__(self, params: Query[TransactionQueryParams]):
        self.params = params
        self.builder = QueryBuilder()

    def is_satisfied(self) -> Q:
        params_dict = self.params.model_dump(exclude_unset=True, exclude={'wallets', 'categories', 'start_date', 'end_date'})
        for k, v in params_dict.items():
            if isinstance(v, list): pass
            self.builder.add_condition(k, v)

        if self.params.wallets:
            self.builder.add_relation_condition('wallet', self.params.wallets)
        if self.params.categories:
            self.builder.add_relation_condition('category', self.params.categories)
        if self.params.start_date and self.params.end_date:
            self.builder.range('transaction_date', (self.params.start_date, self.params.end_date))
        return self.builder.build()

class TransactionRepository(Repository):
    def __init__(self):
        super().__init__(model=Transaction)

    def get_all_for_user(self, params: Query[TransactionQueryParams]):
        specification = TransactionSpecification(params)
        return self.filter(specification)

    @staticmethod
    def group_by(query:QuerySet[Transaction], group_by: Literal['category', 'wallet'] | None = 'category') -> list[
        GroupByTransaction]:
        calc = query.values(group_by).annotate(
            id=F(group_by),
            name=F(group_by+'__name'),
            total=Sum('amount'),
            count=Count('id')
        )
        return list(calc)
        # result = [GroupByTransaction(total=obj['total'], count=obj['count'], name=obj['name'], id=obj[group_by]) for obj in list(calc)]
        # return result

    @staticmethod
    def sum_amount(query: QuerySet[Transaction]):
        return query.aggregate(total=Sum('amount'))['total'] or 0



