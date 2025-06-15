from typing import List, Optional
from utils.query import query_or_not
from utils.repository import Repository
from wallet.models import Wallet


class WalletRepository(Repository):
    model = Wallet

    def get_all_for_user(self, user_id):
        return self.filter(user_id=user_id)
