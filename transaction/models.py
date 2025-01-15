from django.contrib.auth.models import User
from django.db import models

from category.models import Category
from core.models.datetime import Datetime
from utils.common import TransactionType
from wallet.models import Wallet


# Create your models here.
class Transaction(Datetime):
    transaction_type = models.CharField(choices=TransactionType.get_choices(), default=TransactionType.EXPENSE.value, max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(null=True, default=None)
    transaction_date = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name='transactions')
    user = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE)

    @staticmethod
    def reset_transactions(transaction):
        if transaction.transaction_type == TransactionType.INCOME.value:
            transaction.wallet.balance -= transaction.amount
        else:
            transaction.wallet.balance += transaction.amount

        transaction.wallet.save()


    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not is_new:
            old_transaction = Transaction.objects.get(pk=self.pk)
            if old_transaction.amount != self.amount or old_transaction.transaction_type != self.transaction_type or old_transaction.wallet != self.wallet:
                self.reset_transactions(old_transaction)

        if self.transaction_type == TransactionType.INCOME.value:
            self.wallet.balance += self.amount
        else:
            self.wallet.balance -= self.amount

        self.wallet.save()
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.reset_transactions(self)

        self.wallet.save()
        super().delete(*args, **kwargs)
