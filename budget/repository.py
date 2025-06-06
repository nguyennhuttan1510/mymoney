from typing import List, Optional

from budget.models import Budget


def create(data: dict) -> Budget:
    return Budget.objects.create(**data)

def get_all() -> List[Budget]:
    return Budget.objects.filter()

def get_by_id(budget_id: int, *args, **kwargs) -> Optional[Budget]:
    return Budget.objects.get(pk=budget_id, *args, **kwargs)

def update(budget: Budget, data: dict) -> Optional[Budget]:
    for field, value in data.items():
        setattr(budget, field, value)
    budget.save()
    return budget

def delete(budget: Budget):
    budget.delete()
