from simplecsv import serialize_c
from serializers.base import Serializable, Serializer
from typing import Iterator, List, Type


class CSVSerializer(Serializer):
    def serialize(self, data: List[Serializable]) -> Iterator[str]:
        if not data:
            raise ValueError("Data list cannot be empty")

        try:
            for item in data:
                yield serialize_c(item.to_serializable())
        except TypeError:
            raise ValueError("Invalid data type")

    def deserialize(self, csv_string: str, cls: Type[Serializable]) -> Iterator[Serializable]:
        if not csv_string.strip():
            raise ValueError("CSV string cannot be empty")

        try:
            for line in csv_string.splitlines():
                yield cls.from_serializable(dict(zip(cls.model_fields, line.split(","))))
        except TypeError:
            raise ValueError("Invalid CSV string")

    def to_file(self, data: List[Serializable], file_path: str):
        if not data:
            raise ValueError("Data list cannot be empty")

        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                [file.writelines(self.serialize(item)) for item in data]
        except TypeError:
            raise ValueError("Invalid data type")

    def from_file(self, file_path: str, cls: Type[Serializable]) -> Iterator[Serializable]:
        if not file_path:
            raise ValueError("File path cannot be empty")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                yield self.deserialize(file.read(), cls)
        except FileNotFoundError:
            raise ValueError("File not found")
