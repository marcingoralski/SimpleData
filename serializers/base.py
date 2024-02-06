from abc import ABC, abstractmethod
from typing import Iterator, Type, TypeVar, Generic, Dict

T = TypeVar('T', bound='Serializable')


class Serializable(ABC, Generic[T]):
    @abstractmethod
    def to_serializable(self) -> Dict:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_serializable(cls, data: Dict) -> T:
        raise NotImplementedError


class Serializer(ABC):
    @abstractmethod
    def serialize(self, data: T) -> Iterator[str]:
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, data: str, cls: Type[T]) -> Iterator[T]:
        raise NotImplementedError

    @abstractmethod
    def to_file(self, data: T, file_path: str):
        raise NotImplementedError

    @abstractmethod
    def from_file(self, file_path: str, cls: Type[T]) -> Iterator[T]:
        raise NotImplementedError
