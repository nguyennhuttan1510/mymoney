from ninja import ModelSchema

from wallet.models import Wallet


class WalletResponse(ModelSchema):
    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'type']

class WalletRequest(ModelSchema):
    class Meta:
        model = Wallet
        fields = ['balance', 'type']