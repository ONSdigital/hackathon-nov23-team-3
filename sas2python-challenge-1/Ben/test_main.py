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

    def test_remove_incomplete_periods_with_no_complete_years(self):
        df = pd.DataFrame({
            'TS_PERIOD': ['2021Q1', '2021Q2', '2021Q3', '2021Q4', '2023Q1', '2023Q2'],
            'DIMENSION1': ['value1', 'value1', 'value1', 'value1', 'value1', 'value1']
        })
        result = remove_incomplete_periods(df)
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
    Given a DataFrame with TS_PERIOD and DIMENSION1 columns
    When remove_incomplete_periods function is called
    Then the resulting DataFrame should only contain complete years with 4 quarters
    And the length of the resulting DataFrame should be 4

  Scenario: Remove incomplete periods from DataFrame with no complete years
    Given a DataFrame with TS_PERIOD and DIMENSION1 columns
    And the DataFrame does not contain any complete years with 4 quarters
    When remove_incomplete_periods function is called
    Then the resulting DataFrame should be empty
    And the length of the resulting DataFrame should be 0