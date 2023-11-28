import unittest
import pandas as pd
from main import remove_incomplete_periods

class TestRemoveIncompletePeriods(unittest.TestCase):
    def test_remove_incomplete_periods(self):
        df = pd.DataFrame({
            'TS_PERIOD': ['2021Q1', '2021Q2', '2021Q3', '2021Q4', '2022Q1', '2022Q2'],
            'DIMENSION1': ['value1', 'value1', 'value1', 'value1', 'value1', 'value1']
        })
        result = remove_incomplete_periods(df)
        self.assertEqual(len(result), 4)

        df = pd.DataFrame({
            'TS_PERIOD': ['2021Q1', '2021Q2', '2021Q3', '2022Q1', '2022Q2'],
            'DIMENSION1': ['value1', 'value1', 'value1', 'value1', 'value1']
        })
        result = remove_incomplete_periods(df)
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()

