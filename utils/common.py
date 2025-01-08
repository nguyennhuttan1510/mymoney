from enum import Enum


class TransactionType(Enum):
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'

    @classmethod
    def get_choices(cls):
        return [(c.value, c.name) for c in cls]
