from budget.models import Budget
from utils.repository import Repository


class BudgetRepository(Repository):
    def __init__(self):
        super().__init__(model=Budget)

    def get_all_for_user(self, user_id, *args, **kwargs):
        return self.filter(wallet__user__pk=user_id, *args, **kwargs)
