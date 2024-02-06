import json
from serializers.base import Serializable, Serializer
from typing import Iterator, List, Type


class JSONSerializer(Serializer):
    def serialize(self, data: List[Serializable]) -> Iterator[str]:
        if not data:
            raise ValueError("Data list cannot be empty")

        try:
            for it in json.dumps([item.to_serializable() for item in data], indent=4):
                yield it
        except TypeError:
            raise ValueError("Invalid data type")

    def deserialize(self, json_string: str, cls: Type[Serializable]) -> Iterator[Serializable]:
        if not json_string.strip():
            raise ValueError("JSON string cannot be empty")

        try:
            data = json.loads(json_string)
            for item in data:
                yield cls.from_serializable(item)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string")

    def to_file(self, data: List[Serializable], file_path: str):
        if not data:
            raise ValueError("Data list cannot be empty")

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.serialize(data))
        except TypeError:
            raise ValueError("Invalid data type")

    def from_file(self, file_path: str, cls: Type[Serializable]) -> Iterator[Serializable]:
        if not file_path:
            raise ValueError("File path cannot be empty")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for it in self.deserialize(file.read(), cls):
                    yield it
        except FileNotFoundError:
            raise ValueError("File not found")
