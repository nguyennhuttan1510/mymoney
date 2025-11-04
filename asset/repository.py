from django.db.models import Q
from ninja import Query

from asset.models import Asset
from asset.schema import AssetSearchParams
from utils.query_builder import Specification, QueryBuilder
from core.dao.repository import Repository


class AssetRepository(Repository[Asset]):
    def __init__(self):
        super().__init__(model=Asset)



class AssetSpecification(Specification[Asset]):
    def __init__(self, params: Query[AssetSearchParams]):
        self.params = params
        self.builder = QueryBuilder()

    def is_satisfied(self) -> Q:
        params_dict = self.params.model_dump(exclude_none=True)
        self.base_query(params_dict, self.builder)
        return self.builder.build()

