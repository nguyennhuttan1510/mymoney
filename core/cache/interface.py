from abc import abstractmethod, ABC
from typing import Any, Callable


class CacheStrategy(ABC):
    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key:str, value:Any, ttl:int):
        pass

    @abstractmethod
    def delete(self, key:str):
        pass

    @abstractmethod
    def scan(self, pattern:str):
        pass

    @abstractmethod
    def existed(self, key:str):
        pass

    @abstractmethod
    def clear(self, pattern:str):
        pass



class KeyGenerator(ABC):
    @abstractmethod
    def generate(self, **kwargs):
        pass


class Serializer(ABC):
    @abstractmethod
    def serialize(self, data: Any):
        pass

    @abstractmethod
    def deserialize(self, data: Any):
        pass


class CacheConnect(ABC):
    @abstractmethod
    def get_client(self):
        pass