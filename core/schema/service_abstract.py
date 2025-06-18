from abc import ABC
from typing_extensions import TypeVar, Generic

T = TypeVar('T')

class ServiceAbstract(ABC):
    repository = None
    service = None