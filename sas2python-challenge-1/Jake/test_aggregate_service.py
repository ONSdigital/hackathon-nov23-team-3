import unittest
import pandas as pd
from aggregate_service import AggregateService

class TestAggregateService(unittest.TestCase):
    """
    Test class for the aggregate service.
    """

    def test_remove_incomplete_periods_empty_dataframe(self):
        """
        Test case for removing incomplete periods from an empty dataframe.
        """
        # Arrange
        aggregate_service = AggregateService()
        df_empty = pd.DataFrame(columns=['TS_PERIOD', 'DIMENSION1', 'TS_VALUE'])
        expected_output_empty = pd.DataFrame(columns=['TS_PERIOD', 'DIMENSION1', 'TS_VALUE'])

        # Act
        result = aggregate_service._remove_incomplete_periods(df_empty)

        # Assert
        pd.testing.assert_frame_equal(result, expected_output_empty)

    def test_remove_incomplete_periods_incomplete_years(self):
        """
        Test case for removing incomplete periods from a dataframe with incomplete years.
        """
        # Arrange
        aggregate_service = AggregateService()
        df_incomplete = pd.DataFrame(columns=['TS_PERIOD', 'DIMENSION1', 'TS_VALUE'],
                                        data ={
                                            'TS_PERIOD': ['2020Q1', '2020Q2', '2020Q3', '2020Q4', '2021Q1', '2021Q2'],
                                            'DIMENSION1': ['CVM', 'CVM', 'CVM', 'CVM', 'CVM', 'CVM'],
                                            'TS_VALUE': [208450.967, 21916.63761, 71873.30554, 19919.71519, 4535.913698, 1283.936637]
                                        })
        expected_output_incomplete = pd.DataFrame(columns=['TS_PERIOD', 'DIMENSION1', 'TS_VALUE'], 
                                                data = {
                                                    'TS_PERIOD': [pd.Period('2020'),pd.Period('2020'),pd.Period('2020'),pd.Period('2020')],
                                                    'DIMENSION1': ['CVM', 'CVM', 'CVM', 'CVM'],            
                                                    'TS_VALUE': [208450.967, 21916.63761, 71873.30554, 19919.71519]

                                                })

        # Act
        result = aggregate_service._remove_incomplete_periods(df_incomplete)

        print(result)
        print(expected_output_incomplete)

        # Assert
        pd.testing.assert_frame_equal(result, expected_output_incomplete)

    def test_remove_incomplete_periods_complete_years(self):
        """
        Test case for removing incomplete periods from a dataframe with complete years.
        """
        # Arrange
        aggregate_service = AggregateService()
        df_complete = pd.DataFrame({
            'TS_PERIOD': ['2020Q1', '2020Q2', '2020Q3', '2020Q4', '2021Q1', '2021Q2', '2021Q3', '2021Q4'],
            'DIMENSION1': ['CVM', 'CVM', 'CVM', 'CVM', 'CVM', 'CVM', 'CVM', 'CVM'],
            'TS_VALUE': [208450.967, 21916.63761, 71873.30554, 19919.71519, 4535.913698, 1283.936637, 2626.719872, 6056.245573]
        })
        expected_output_complete = pd.DataFrame({
            'TS_PERIOD': [pd.Period('2020'),pd.Period('2020'),pd.Period('2020'),pd.Period('2020'),pd.Period('2021'),pd.Period('2021'),pd.Period('2021'),pd.Period('2021')],
            'DIMENSION1': ['CVM', 'CVM', 'CVM', 'CVM', 'CVM', 'CVM', 'CVM', 'CVM'],
            'TS_VALUE': [208450.967, 21916.63761, 71873.30554, 19919.71519, 4535.913698, 1283.936637, 2626.719872, 6056.245573]
        })

        # Act
        result = aggregate_service._remove_incomplete_periods(df_complete)

        # Assert
        pd.testing.assert_frame_equal(result, expected_output_complete)

