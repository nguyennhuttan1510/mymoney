from abc import ABC, abstractmethod
from transaction.models import Transaction as TransactionModel
from utils.common import TransactionType
from django.db import transaction as transaction_db

from wallet.models import Wallet


class Transaction(ABC):

    def change_balance(self, transaction: TransactionModel):
        wallet = Wallet.objects.get(pk=transaction.wallet.pk)
        if transaction.category.type == TransactionType.INCOME.value:
            wallet.balance += transaction.amount
        else:
            wallet.balance -= transaction.amount
        wallet.save()

    @abstractmethod
    def pay(self) -> TransactionModel:
        pass

    def destroy(self):
        pass


class SpendingTransaction(Transaction):
    transaction: TransactionModel = None

    def __init__(self, transaction):
        self.transaction = transaction

    def pay(self):
        try:
            with transaction_db.atomic():
                is_new = self.transaction.pk is None
                if is_new:
                    self.change_balance(self.transaction)

                else:
                    old_transaction = TransactionModel.objects.get(pk=self.transaction.pk)
                    if old_transaction.amount != self.transaction.amount or old_transaction.category_id.type != self.transaction.category.type or old_transaction.wallet != self.transaction.wallet:
                        self.transaction.reset_transactions(old_transaction)
                        self.change_balance(self.transaction)

                self.transaction.save()
                return self.transaction

        except Exception as e:
            raise e

    def destroy(self):
        self.transaction.reset_transactions(self.transaction)
        self.transaction.delete()



class SpendingTransactionFactory(ABC):
    @abstractmethod
    def create_transaction_method(self) -> Transaction:
        return SpendingTransaction()





