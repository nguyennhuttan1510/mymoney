
from transaction.models import Transaction
from utils.repository import Repository


class TransactionRepository(Repository):
    def __init__(self):
        super().__init__(model=Transaction)

    def get_all_for_user(self, user_id: int):
        return self.filter(user_id=user_id)