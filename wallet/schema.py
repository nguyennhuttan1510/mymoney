from ninja import ModelSchema, Field, Schema
from pydantic import BaseModel, field_validator
from pydantic.v1 import validator

from enums.transaction import TransactionType
from enums.wallet import WalletType
from wallet.models import Wallet


class WalletOut(ModelSchema):
    balance:int

    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'type', 'name']


class WalletIn(ModelSchema):
    name: str
    balance: int
    type: WalletType

    class Meta:
        model = Wallet
        fields = ['balance', 'type']

    @field_validator("balance")
    def validate_balance_positive(cls, v):
        print('v', v)
        if v < 0:
            raise ValueError("Balance must be positive")
        return v


class WalletParam(Schema):
    balance: float = None
    type: WalletType = None
    name: str = None