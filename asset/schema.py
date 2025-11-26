from datetime import datetime
from typing import List

from django.utils import timezone

from ninja import Schema
from openpyxl.styles.builtins import total
from pydantic import BaseModel, computed_field, create_model, Field

from asset.models import StatusAsset
from core.schema.response import EntityListResponse


class AssetIn(Schema):
    name: str
    status: StatusAsset
    expired_date: datetime | None = None
    buy_price: float = 0
    sell_price: float = 0
    buy_date: datetime
    sell_date: datetime | None = None
    note: str | None = None


class AssetOut(AssetIn):
    @computed_field
    @property
    def delta_days(self) -> int:
        end_date = self.sell_date or timezone.now()
        return (end_date - self.buy_date).days if self.buy_date else None

    @computed_field
    @property
    def delta_price(self) -> float:
        return self.buy_price - self.sell_price

    @computed_field
    @property
    def price_per_day(self) -> float:
        return round(self.delta_price / self.delta_days, 2)


class AssetSearchParams(Schema):
    status: StatusAsset | None = None
    user_id: int | None = None


class AssetList(EntityListResponse[AssetOut]):
    pass

