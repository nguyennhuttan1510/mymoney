from typing import Dict

from asset.repository import AssetRepository, AssetSpecification
from asset.schema import AssetIn
from core.schema.service_abstract import ServiceAbstract


class AssetService(ServiceAbstract):
    repository = AssetRepository()

    def create(self, data: AssetIn):
        return self.repository.create(data.dict())

    def search(self, query):
        specification = AssetSpecification(query)
        return self.repository.filter(specification)

    def update(self, asset_id:int, payload:dict):
        instance = self.repository.get_by_id(pk=asset_id)
        return self.repository.update(instance, data=payload)

    def delete(self, asset_id:int):
        return self.repository.delete(asset_id)
