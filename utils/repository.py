from typing import List, Optional
from django.db.models import Model
from django.contrib.auth.models import User
from typing import List, Optional, Generic, TypeVar
from transaction.models import Transaction


T = TypeVar('T')

class Repository(Generic[T]):
    model: Model = None
    @classmethod
    def create(cls, data: dict) -> T:
        return cls.model.objects.create(**data)
    @classmethod
    def get_all(cls) -> List[T]:
        return cls.model.objects.all()
    @classmethod
    def filter(cls, *args, **kwargs):
        return cls.model.objects.filter(*args, **kwargs)
    @classmethod
    def get_by_id(cls, transaction_id: int) -> Optional[T]:
        return cls.model.objects.get(pk=transaction_id)
    @classmethod
    def update(cls, instance: T, data: dict) -> Optional[T]:
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
    @classmethod
    def delete(cls, instance: T):
        return instance.delete()





