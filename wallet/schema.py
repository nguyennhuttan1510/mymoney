from ninja import ModelSchema

from wallet.models import Wallet


class WalletSchema(ModelSchema):
    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'type']