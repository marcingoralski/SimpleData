from serializers.csv_serializer import CSVSerializer
from serializers.json_serializer import JSONSerializer
from serializers.protobuf_serializer import ProtobufSerializer


class SimpleDataSerializer:
    @staticmethod
    def create_serializer(format: str):
        match (format):
            case "csv":
                return CSVSerializer()
            case "json":
                return JSONSerializer()
            case "protobuf":
                return ProtobufSerializer()
            case _:
                raise ValueError(f"Unknown format {format}")
