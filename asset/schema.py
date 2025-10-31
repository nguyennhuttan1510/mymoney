from datetime import datetime, timedelta
from typing import Any, Optional

from ninja import Schema
from openpyxl.styles.builtins import total
from pydantic import BaseModel, computed_field, create_model, Field

from asset.models import StatusAsset


class AssetIn(Schema):
    name: str
    status: StatusAsset
    expired_date: datetime | None = None
    buy_price: float
    sell_price: float | None = None
    buy_date: datetime
    sell_date: datetime | None = None
    note: str | None = None


class AssetOut(AssetIn):
    @computed_field
    @property
    def delta_days(self) -> int:
        return (self.sell_date - self.buy_date).days if self.sell_date and self.buy_date else None

    @computed_field
    @property
    def delta_price(self) -> float:
        return self.buy_price - self.sell_price if self.sell_price and self.buy_price else None

    @computed_field
    @property
    def price_per_day(self) -> float:
        return round(self.delta_price / self.delta_days, 2) if self.delta_price and self.delta_days else None


class AssetSearchParams(Schema):
    status: StatusAsset | None = None
