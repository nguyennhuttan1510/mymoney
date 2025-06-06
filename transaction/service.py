from django.contrib.auth.models import User
from django.db import transaction as transaction_db

from core.models.transactions import SpendingTransaction
from transaction.schema import TransactionCreateSchema
from transaction import repository as repository_transaction
from transaction.models import Transaction

class TransactionService:
    user: User = None
    def __init__(self, user):
        self.user = user

    def create_transaction(self, data: TransactionCreateSchema):
        with transaction_db.atomic():

            transaction_data = {"amount": data.amount, "category_id": data.category, "wallet_id": data.wallet, "budget_id": data.budget, 'user_id': self.user.pk}
            transaction = SpendingTransaction(Transaction(**transaction_data))

            return transaction.pay()


    def get_all_transaction(self):
        return repository_transaction.get_all(self.user)