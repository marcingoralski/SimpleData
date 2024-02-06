# SimpleData

Extendable serializer adapter for common formats (csv, json, protobuf), which also shows off how bloated today's environments are.

```
SimpleData/
│
├── setup.py                        # Setup for simplecsv module
├── benchmark.py                    # Benchmark methods
│
├── serializers/                    # Directory for serializer classes
│   ├── base.py                     # Contains the Serializable ABC and other base classes
│   ├── csv_serializer.py           # CSVSerializer class
│   ├── json_serializer.py          # JSONSerializer class
│   ├── xml_serializer.py           # XMLSerializer class
│   └── protobuf_serializer.py      # ProtobufSerializer class
│
├── models/                         # Directory for data models
│   └── person.py                   # Person class 
│
├── modules/                        # Directory for data models
│   ├── simplecsv.c                 # C serializer module
│   ├── person.proto                # Protobuf Person class
│   └── person_pb2.py               # Precompiled Protobuf module
│
├── factory/                        # Directory for the serializer factory
│   └── serializer_factory.py       # SimpleDataSerializer factory class
│
└── tests/                          # Directory for test cases
    ├── test_csv_serializer.py      # Test cases for CSVSerializer
    ├── test_json_serializer.py     # Test cases for JSONSerializer
    ├── test_xml_serializer.py      # Test cases for XMLSerializer
    └── test_protobuf_serializer.py # Test cases for ProtobufSerializer
```

## Install dependencies
`pip install -r requirements.txt`

## Setup the CSV module
`python setup.py install`

## Run tests
`python -m unittest discover`

## (Optional) Build your own Protobuf module
 - Using [Chocolatey](https://chocolatey.org/):
    `choco install protoc && protoc --python_out= . 'models/person.proto'`
