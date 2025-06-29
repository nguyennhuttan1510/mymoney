from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from django.db.models import Q

T = TypeVar('T')

class Specification(Generic[T], ABC):
    @abstractmethod
    def is_satisfied(self) -> Q:
        pass


class QueryBuilder:
    def __init__(self):
        self._query = Q()

    def add_condition(self, key, value) -> 'QueryBuilder':
        self._query &= Q(**{key:value})
        return self

    def add_or_condition(self, key, value) -> 'QueryBuilder':
        self._query |= Q(**{key:value})
        return self

    def add_relation_condition(self, key, value) -> 'QueryBuilder':
        self._query &= Q(**{key+'__in':value})
        return self

    def build(self) -> Q:
        return self._query


    # def add_where(self, key, value):
    #     self.query += 'WHERE {} = "{}" '.format(key, value)
    #     return self
    # def add_order_by(self, key, order='ASC'):
    #     self.query += 'ORDER BY {} {}'.format(key, order)
    #     return self
    # def add_limit(self, limit):
    #     pass