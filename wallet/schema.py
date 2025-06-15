from ninja import ModelSchema
from pydantic.v1 import validator

from wallet.models import Wallet


class WalletOut(ModelSchema):
    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'type']

class WalletIn(ModelSchema):
    balance: int

    class Meta:
        model = Wallet
        fields = ['balance', 'type']

    @validator("balance")
    def validate_balance_positive(cls, v):
        if v < 0:
            raise ValueError("Balance must be >= 0")
        return v