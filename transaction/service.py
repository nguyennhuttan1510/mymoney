from django.contrib.auth.models import User
from django.db import transaction as transaction_db

from category.models import Category
from core.models.transactions import SpendingTransaction
from transaction.schema import TransactionCreateSchema, TransactionUpdateSchema
from transaction import repository as repository_transaction
from transaction.models import Transaction
from utils.query import query_or_not
from wallet.models import Wallet


class TransactionService:
    user: User = None
    transaction_id: int = None

    def __init__(self, user, transaction_id=None):
        self.user = user
        self.transaction_id = transaction_id

    def create_transaction(self, data: TransactionCreateSchema):
        transaction_data = {"amount": data.amount, "category_id": data.category, "wallet_id": data.wallet, "budget_id": data.budget, 'user_id': self.user.pk}
        transaction = SpendingTransaction(Transaction(**transaction_data))

        return transaction.process()


    def get_all_transaction(self, *args, **kwarg):
        return repository_transaction.get_all(self.user, *args, **kwarg)


    def update_transaction(self, data: TransactionUpdateSchema):
        transaction_updated = repository_transaction.get_by_id(self.transaction_id)
        for field, value in data.dict().items():
            if value is not None:
                setattr(transaction_updated, field, value)

        transaction = SpendingTransaction(transaction_updated)
        return transaction.process()

    def delete_transaction(self, transaction_id: int):
        transaction = repository_transaction.get_by_id(transaction_id)
        return repository_transaction.delete(transaction)
