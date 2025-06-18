from utils.repository import Repository
from wallet.models import Wallet


class WalletRepository(Repository):
    def __init__(self):
        super().__init__(model=Wallet)

    def get_all_for_user(self, user_id, *args, **kwargs):
        return self.filter(user_id=user_id, *args, **kwargs)
