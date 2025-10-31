from enum import Enum

from django.db import models

from core.models.datetime import Datetime

class StatusAsset(str, Enum):
    USING = 'USING'
    USED = 'USED'
    LOSS = 'LOSS'
    BROKEN = 'BROKEN'
    NOT_USE = 'NOT_USE'
    GIVE = 'GIVE'

# Create your models here.
class Asset(Datetime):
    name = models.CharField(max_length=50)
    status = models.CharField(choices=[(c.value, c.name) for c in StatusAsset], default=StatusAsset.USING.value, max_length=20)
    expired_date = models.DateField(null=True, blank=True)
    buy_price = models.DecimalField(max_digits=12, decimal_places=2)
    sell_price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    buy_date = models.DateTimeField()
    sell_date = models.DateTimeField(null=True, blank=True)
    note = models.CharField(null=True, max_length=100)


