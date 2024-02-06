import unittest
from unittest.mock import mock_open, patch
from factory.serializer_factory import SimpleDataSerializer
from models.person import Person


class TestJSONSerializer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.serializer = SimpleDataSerializer.create_serializer('json')
        cls.sample_data = [Person(first_name="John", last_name="Doe", age=30),
                           Person(first_name="Jane", last_name="Doe", age=25)]

    def test_serialize(self):
        it = self.serializer.serialize(self.sample_data)
        first_line = next(it)
        self.assertIn('[', first_line)

    def test_deserialize(self):
        json_data = '[{"first_name": "John", "last_name": "Doe", "age": 30}, {"first_name": "Jane", "last_name": "Doe", "age": 25}]'
        it = self.serializer.deserialize(json_data, Person)
        john = next(it)
        self.assertEqual(john.first_name, "John")
        jane = next(it)
        self.assertEqual(jane.first_name, "Jane")

    def test_serialize_empty_list(self):
        with self.assertRaises(ValueError):
            next(self.serializer.serialize([]))

    def test_deserialize_empty_string(self):
        with self.assertRaises(ValueError):
            next(self.serializer.deserialize('', Person))

    @patch("builtins.open", new_callable=mock_open, read_data='[{"first_name": "John", "last_name": "Doe", "age": 30}, {"first_name": "Jane", "last_name": "Doe", "age": 25}]')
    def test_from_file(self, mock_file):
        deserialized = next(self.serializer.from_file('test.json', Person))
        self.assertEqual(deserialized.first_name, "John")
        mock_file.assert_called_once_with('test.json', 'r', encoding='utf-8')

    @patch("builtins.open", new_callable=mock_open)
    def test_to_file(self, mock_file):
        self.serializer.to_file(self.sample_data, 'test.json')
        mock_file.assert_called_once_with('test.json', 'w', encoding='utf-8')

    def test_json_roundtrip(self):
        serialized_data = list(self.serializer.serialize(self.sample_data))
        deserialized_data = list(self.serializer.deserialize(
            ''.join(serialized_data), Person))

        for original, deserialized in zip(self.sample_data, deserialized_data):
            self.assertEqual(original, deserialized)
            self.assertEqual(original.first_name, deserialized.first_name)


if __name__ == '__main__':
    unittest.main()
