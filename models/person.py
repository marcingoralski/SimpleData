from serializers.base import Serializable
from pydantic import BaseModel


class Person(BaseModel, Serializable):
    first_name: str
    last_name: str
    age: int

    def __eq__(self, other):
        if not isinstance(other, Person):
            return False

        return (self.first_name == other.first_name and
                self.last_name == other.last_name and
                self.age == other.age)

    def to_serializable(self) -> dict:
        return self.model_dump()

    @classmethod
    def from_serializable(cls, data):
        return cls(**data)
