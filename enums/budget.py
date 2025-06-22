from enum import Enum


class BudgetStatus(str, Enum):
    OK = 'OK'
    OVER = 'OVER'
    WARNING = 'WARNING'