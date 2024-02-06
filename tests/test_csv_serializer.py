import unittest
from unittest.mock import mock_open, patch
from factory.serializer_factory import SimpleDataSerializer
from models.person import Person


class TestCSVSerializer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.serializer = SimpleDataSerializer.create_serializer('csv')
        cls.sample_data = [Person(first_name='John', last_name='Doe', age=30),
                           Person(first_name='Jane', last_name='Doe', age=25)]

    def test_serialize_empty_data(self):
        with self.assertRaises(ValueError):
            next(self.serializer.serialize([]))

    def test_deserialize_empty_string(self):
        with self.assertRaises(ValueError):
            next(self.serializer.deserialize('', Person))

    def test_round_trip(self):
        serialized_data = list(self.serializer.serialize(self.sample_data))
        deserialized_data = list(self.serializer.deserialize(
            '\n'.join(serialized_data), Person))

        for original, deserialized in zip(self.sample_data, deserialized_data):
            self.assertEqual(original, deserialized)

    def test_to_file_empty_data(self):
        with self.assertRaises(ValueError):
            self.serializer.to_file([], 'dummy_path')

    @patch("builtins.open", new_callable=mock_open)
    def test_to_file(self, mock_file):
        self.serializer.to_file(self.sample_data, 'dummy_path')
        mock_file.assert_called_once_with(
            'dummy_path', 'w', newline='', encoding='utf-8')
        self.assertEqual(mock_file().writelines.call_count, 2)

    @patch("builtins.open", new_callable=mock_open, read_data="John,Doe,30\nJane,Doe,25")
    def test_from_file(self, mock_file):
        it = next(self.serializer.from_file('dummy_path', Person))

        first_result = next(it)
        self.assertEqual(first_result.first_name, 'John')
        self.assertEqual(first_result.last_name, 'Doe')
        self.assertEqual(first_result.age, 30)

        second_result = next(it)
        self.assertEqual(second_result.first_name, 'Jane')
        self.assertEqual(second_result.last_name, 'Doe')
        self.assertEqual(second_result.age, 25)

    # Additional tests for edge cases and error conditions can be added here


if __name__ == '__main__':
    unittest.main()
