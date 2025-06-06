from typing import List, Optional

from category.models import Category


def create(data: dict) -> Category:
    return Category.objects.create(**data)

def get_all() -> List[Category]:
    return Category.objects.filter()

def get_by_id(category_id: int, *args, **kwargs) -> Optional[Category]:
    return Category.objects.get(pk=category_id, *args, **kwargs)

def update(category: Category, data: dict) -> Optional[Category]:
    for field, value in data.items():
        setattr(category, field, value)
    category.save()
    return category

def delete(category: Category):
    category.delete()
