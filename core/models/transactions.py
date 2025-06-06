from abc import ABC, abstractmethod
from transaction.models import Transaction as TransactionModel
from utils.common import TransactionType
from django.db import transaction as transaction_db
from transaction import repository

from wallet.models import Wallet


class Transaction(ABC):
    transaction: TransactionModel


    def reset_balance(self, old_transaction: TransactionModel):
        transaction = self.transaction
        if old_transaction.category.type == TransactionType.INCOME.value:
            transaction.wallet.balance -= old_transaction.amount
        else:
            transaction.wallet.balance += old_transaction.amount
        transaction.wallet.save()


    def change_balance(self):
        transaction = self.transaction
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
    transaction = None

    def __init__(self, transaction: TransactionModel):
        self.transaction = transaction

    def pay(self):
        try:
            with transaction_db.atomic():
                is_new = self.transaction.pk is None
                if is_new:
                    self.change_balance()

                else:
                    old_transaction = repository.get_by_id(self.transaction.pk)
                    if old_transaction.amount != self.transaction.amount or old_transaction.category.type != self.transaction.category.type or old_transaction.wallet != self.transaction.wallet:
                        self.reset_balance(old_transaction)
                        self.change_balance()

                self.transaction.save()
                return self.transaction

        except Exception as e:
            raise e

    def destroy(self):
        repository.delete(self.transaction)
        self.reset_balance(self.transaction)



class SpendingTransactionFactory(ABC):
    @abstractmethod
    def create_transaction_method(self) -> Transaction:
        return SpendingTransaction()





