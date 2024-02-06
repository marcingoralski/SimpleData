import unittest
from unittest.mock import mock_open, patch
from factory.serializer_factory import SimpleDataSerializer
from models.person import Person


class TestProtobufSerializer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.serializer = SimpleDataSerializer.create_serializer('protobuf')
        cls.sample_person = Person(first_name="John", last_name="Doe", age=30)
        cls.sample_bytes = b'\n\r\n\x04John\x12\x03Doe\x18\x1e'

    def test_serialize(self):
        serialized_data = next(self.serializer.serialize([self.sample_person]))
        self.assertIsInstance(serialized_data, bytes)
        self.assertEqual(serialized_data, self.sample_bytes)

    def test_deserialize(self):
        deserialized_data = next(
            self.serializer.deserialize(self.sample_bytes, Person))
        self.assertEqual(deserialized_data.first_name, "John")
        self.assertEqual(deserialized_data.last_name, "Doe")
        self.assertEqual(deserialized_data.age, 30)

    @patch("builtins.open", new_callable=mock_open)
    def test_to_file(self, mock_file):
        self.serializer.to_file([self.sample_person], 'test_person.bin')
        mock_file.assert_called_once_with(
            'test_person.bin', 'w', encoding='utf-8')

    @patch("builtins.open", new_callable=mock_open)
    def test_from_file(self, mock_file):
        mock_file.return_value.read.return_value = self.sample_bytes

        deserialized_data = next(
            self.serializer.from_file('test_person.bin', Person))
        self.assertEqual(deserialized_data.first_name, "John")
        self.assertEqual(deserialized_data.last_name, "Doe")
        self.assertEqual(deserialized_data.age, 30)


if __name__ == '__main__':
    unittest.main()
