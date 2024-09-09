import unittest
from unittest.mock import mock_open, patch
from factory.serializer_factory import SimpleDataSerializer
from factory.format_enum import Format
from models.person import Person
from modules.person_pb2 import Person as PersonProto, People as PeopleProto

class TestProtobufSerializer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.serializer = SimpleDataSerializer.create_serializer(Format.PROTOBUF)
        cls.sample_person = Person(first_name="John", last_name="Doe", age=30)
        cls.sample_bytes = cls.serializer.serialize([cls.sample_person])

    def test_serialize(self):
        serialized_data = self.serializer.serialize([self.sample_person])
        deserialized_people = PeopleProto()
        deserialized_people.ParseFromString(serialized_data)

        deserialized_person = deserialized_people.person[0]
        self.assertEqual(deserialized_person.first_name, self.sample_person.first_name)
        self.assertEqual(deserialized_person.last_name, self.sample_person.last_name)
        self.assertEqual(deserialized_person.age, self.sample_person.age)

    def test_deserialize(self):
        deserialized_data = next(self.serializer.deserialize(self.sample_bytes, Person))
        self.assertEqual(deserialized_data.first_name, "John")
        self.assertEqual(deserialized_data.last_name, "Doe")
        self.assertEqual(deserialized_data.age, 30)

    @patch("builtins.open", new_callable=mock_open)
    def test_to_file(self, mock_file):
        serialized_bytes = self.serializer.serialize([self.sample_person])
        self.serializer.to_file([self.sample_person], 'test_person.bin')
        mock_file.assert_called_once_with('test_person.bin', 'wb')
        mock_file().write.assert_called_once_with(serialized_bytes)

    @patch("builtins.open", new_callable=mock_open)
    def test_from_file(self, mock_file):
        mock_file.return_value.read.return_value = self.sample_bytes
        deserialized_data = next(self.serializer.from_file('test_person.bin', Person))
        self.assertEqual(deserialized_data.first_name, "John")
        self.assertEqual(deserialized_data.last_name, "Doe")
        self.assertEqual(deserialized_data.age, 30)

if __name__ == '__main__':
    unittest.main()
