from serializers.csv_serializer import CSVSerializer
from serializers.json_serializer import JSONSerializer
from serializers.protobuf_serializer import ProtobufSerializer
from factory.format_enum import Format


class SimpleDataSerializer:
    @staticmethod
    def create_serializer(format: Format):
        match (format):
            case format.CSV:
                return CSVSerializer()
            case format.JSON:
                return JSONSerializer()
            case format.PROTOBUF:
                return ProtobufSerializer()
            case _:
                raise ValueError(f"Unknown format: {format}")