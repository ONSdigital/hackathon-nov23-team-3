import unittest
import pandas as pd
from main import load_data


class TestDataLoading(unittest.TestCase):
    def test_load_data(self):
        # Arrange
        file_path = "test_data.csv"
        expected_columns = ['col1', 'col2', 'col3']

        # Act
        filtered_data = load_data(file_path)
        actual_columns = filtered_data.columns.tolist()

        # Assert
        self.assertIsInstance(filtered_data, pd.DataFrame)
        self.assertEqual(actual_columns, expected_columns)
    
    def test_load_data_file_exists(self):
        # Arrange
        file_path = "test_data_missing.csv"

        # Act and Assert
        with self.assertRaises(FileNotFoundError):
            load_data(file_path)

    # def test_load_data_empty_file(self):
    #     # Arrange
    #     file_path = "empty_file.csv"

    #     # Act
    #     filtered_data = load_data(file_path)

    #     # Assert
    #     self.assertIsInstance(filtered_data, pd.DataFrame)
    #     self.assertTrue(filtered_data.empty)

    # def test_load_data_missing_columns(self):
    #     # Arrange
    #     file_path = "missing_columns.csv"
    #     expected_columns = ['col1', 'col3']

    #     # Act
    #     filtered_data = load_data(file_path)
    #     actual_columns = filtered_data.columns.tolist()

    #     # Assert
    #     self.assertIsInstance(filtered_data, pd.DataFrame)
    #     self.assertEqual(actual_columns, expected_columns)

if __name__ == '__main__':
    unittest.main()