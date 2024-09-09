from modules.person_pb2 import Person, People
from serializers.base import Serializable, Serializer
from typing import Iterator, List, Type


class ProtobufSerializer(Serializer):
    def serialize(self, data: List[Serializable]) -> bytes:
        if not data:
            raise ValueError("Data list cannot be empty")

        try:
            people = People()
            for person in data:
                person_proto = Person()

                person_proto.first_name = person.first_name
                person_proto.last_name = person.last_name
                person_proto.age = person.age
                people.person.append(person_proto)

            return people.SerializeToString()
        except TypeError:
            raise ValueError("Invalid data type")

    def deserialize(self, data: bytes, cls: Type[Serializable]) -> Iterator[Serializable]:
        if not data:
            raise ValueError("Data list cannot be empty")

        try:
            people_proto = People()
            people_proto.ParseFromString(data)
            for i in people_proto.person:
                yield cls(first_name=i.first_name, last_name=i.last_name, age=i.age)

        except TypeError:
            raise ValueError("Invalid data type")
        except Exception as e:
            raise ValueError(f"Deserialization error: {e}")
        
    def to_file(self, data: List[Serializable], file_path: str):
        if not data:
            raise ValueError("Data list cannot be empty")

        try:
            with open(file_path, 'wb') as file:
                file.write(self.serialize(data))
        except TypeError:
            raise ValueError("Invalid data type")

    def from_file(self, file_path: str, cls: Type[Serializable]) -> Iterator[Serializable]:
        if not file_path:
            raise ValueError("File path cannot be empty")

        try:
            with open(file_path, 'rb') as file:
                return self.deserialize(file.read(), cls)
        except FileNotFoundError:
            raise ValueError("File not found")
