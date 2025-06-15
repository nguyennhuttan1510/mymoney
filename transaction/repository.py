from transaction.models import Transaction
from utils.repository import Repository


class TransactionRepository(Repository):
    model = Transaction

    def get_all_for_user(self, user_id: int):
        return self.filter(user_id=user_id)