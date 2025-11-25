from django.contrib.auth.models import User

from wallet.repository import WalletRepository
from wallet.schema import WalletParam


class UserService:
    repository = WalletRepository()

    @classmethod
    def get_wallets_user(cls, user_id:int):
        return cls.repository.search(params=WalletParam(user=user_id))
