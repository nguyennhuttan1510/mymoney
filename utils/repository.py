from typing import List, Optional, Type
from django.db.models import Model
from django.contrib.auth.models import User
from typing import List, Optional, Generic, TypeVar
from transaction.models import Transaction


T = TypeVar('T')

class Repository(Generic[T]):
    def __init__(self, model: Type[Model]):
        self.model = model


    def create(self, data: dict) -> T:
        return self.model.objects.create(**data)

    def get_all(self) -> List[T]:
        return self.model.objects.all()

    def filter(self, *args, **kwargs):
        return self.model.objects.filter(*args, **kwargs)

    def get_by_id(self, pk: int, *args, **kwargs) -> Optional[T]:
        return self.model.objects.get(pk=pk, *args, **kwargs)

    def update(self, instance: T, data: dict) -> Optional[T]:
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, instances: T):
        return instances.delete()





