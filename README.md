# SimpleData

Extendable serializer adapter for common formats (csv, json, protobuf), which also benchmarks how bloated today's environments are.

```
SimpleData/
│
├── setup.py                        # Setup for simplecsv module
├── benchmark.py                    # Benchmark methods
│
├── serializers/
│   ├── base.py                     # Serializer ABC
│   ├── csv_serializer.py           # CSVSerializer class
│   ├── json_serializer.py          # JSONSerializer class
│   └── protobuf_serializer.py      # ProtobufSerializer class
│
├── models/
│   ├── person.py                   # Person class
│   └── person.proto                # Protobuf Person class 
│
├── modules/
│   └── simplecsv.c                 # CSV serializer extension
│
├── factory/
│   └── serializer_factory.py       # SimpleDataSerializer factory class
│
└── tests/
    ├── test_csv_serializer.py      # CSVSerializer tests
    ├── test_json_serializer.py     # JSONSerializer tests
    └── test_protobuf_serializer.py # ProtobufSerializer tests
```

## Install dependencies
`pip install -r requirements.txt`

## Setup the CSV module
`python setup.py install`

## Build Protobuf module
 - Using [Chocolatey](https://chocolatey.org/):
    `choco install protoc && protoc --python_out= . 'models/person.proto'`

## Run tests
`python -m unittest discover`
