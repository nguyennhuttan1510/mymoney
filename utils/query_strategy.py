from abc import ABC, abstractmethod

from django.db.models import Q

from utils.query_builder import Specification


class QueryStrategy(ABC):
    @abstractmethod
    def execute(self, specification: Specification) -> Q:
        pass


class DefaultQueryStrategy(QueryStrategy):
    def execute(self, specification: Specification) -> Q:
        return specification.is_satisfied()