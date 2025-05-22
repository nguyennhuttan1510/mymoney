from abc import ABC, abstractmethod
from transaction.models import Transaction as TransactionModel
from utils.common import TransactionType
from django.db import transaction as transaction_db

class Transaction(ABC):

    def change_balance(self, transaction: TransactionModel):
        if transaction.category.type == TransactionType.INCOME.value:
            transaction.wallet.balance += transaction.amount
        else:
            transaction.wallet.balance -= transaction.amount
        transaction.wallet.save()

    @abstractmethod
    def pay(self, amount: float) -> TransactionModel:
        pass

    def destroy(self):
        pass


class SpendingTransaction(Transaction):
    def pay(self, transaction_instance: TransactionModel) -> TransactionModel:
        try:
            with transaction_db.atomic():
                is_new = transaction_instance.pk is None
                if is_new:
                    self.change_balance(transaction_instance)

                else:
                    old_transaction = TransactionModel.objects.get(pk=transaction_instance.pk)
                    if old_transaction.amount != transaction_instance.amount or old_transaction.category.type != transaction_instance.category.type or old_transaction.wallet != transaction_instance.wallet:
                        transaction_instance.reset_transactions(old_transaction)
                        self.change_balance(transaction_instance)

                transaction_instance.save()
                return transaction_instance

        except Exception as e:
            raise e


class SpendingTransactionFactory(ABC):
    @abstractmethod
    def create_transaction_method(self) -> Transaction:
        return SpendingTransaction()





