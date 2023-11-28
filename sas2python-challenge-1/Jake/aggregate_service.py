import pandas as pd
import math

class AggregateService:
    def __init__(self):
        pass

    def _round_sig(self, x, sig=10):
        return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)

    def _remove_incomplete_periods(self, df):
        # Convert TS_PERIOD to datetime and extract the year
        df['Year'] = pd.to_datetime(df['TS_PERIOD']).dt.to_period('Y')

        df['Quarter'] = pd.to_datetime(df['TS_PERIOD']).dt.to_period('Q')

        df['TS_PERIOD'] = df['Year']

        # Remove the Year column
        df = df.drop('Year', axis=1)

        # Count the number of quarters for each year
        quarter_counts = df.groupby(['DIMENSION1', 'TS_PERIOD'])['Quarter'].nunique()

        # Only keep the years with 4 quarters
        complete_years = quarter_counts[quarter_counts == 4].reset_index()['TS_PERIOD']

        # Filter the dataframe to only include complete years
        df = df[df['TS_PERIOD'].isin(complete_years)]

        # Remove the Quarter column
        df = df.drop('Quarter', axis=1)

        return df

    def aggregate(self, input_file, output_file):
        # Read the CSV file
        df = pd.read_csv(input_file)

        df = self._remove_incomplete_periods(df)

        # Group by DIMENSION1 and Year, and sum TS_VALUE
        df_agg = df.groupby(['DIMENSION1', 'TS_PERIOD'])['TS_VALUE'].sum().reset_index()

        # Round the aggregated values to 9 significant figures
        df_agg['TS_VALUE'] = df_agg['TS_VALUE'].apply(self._round_sig)

        # Save the aggregated data to a CSV file
        df_agg.to_csv(output_file, index=False)
