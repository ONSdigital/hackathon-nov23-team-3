import pandas as pd

import math

def round_sig(x, sig=10):
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)

def remove_incomplete_periods(df):
    # Convert TS_PERIOD to datetime and extract the year
    df['Year'] = pd.to_datetime(df['TS_PERIOD']).dt.to_period('Y')
    df['Quarter'] = pd.to_datetime(df['TS_PERIOD']).dt.to_period('Q')

    # Count the number of quarters for each year
    quarter_counts = df.groupby(['DIMENSION1', 'Year'])['Quarter'].nunique()

    # Only keep the years with 4 quarters
    complete_years = quarter_counts[quarter_counts == 4].reset_index()['Year']

    # Filter the dataframe to only include complete years
    return df[df['Year'].isin(complete_years)]

def aggregate(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    df = remove_incomplete_periods(df)

    # Group by DIMENSION1 and Year, and sum TS_VALUE
    df_agg = df.groupby(['DIMENSION1', 'Year'])['TS_VALUE'].sum().reset_index()

    # Round the aggregated values to 9 significant figures
    df_agg['TS_VALUE'] = df_agg['TS_VALUE'].apply(round_sig)

    # Print the aggregated data
    print(df_agg)

    # Save the aggregated data to a CSV file
    df_agg.to_csv(output_file, index=False)

input_file = 'D:\\Repos\\hackathon-nov23-team-3\\sas2python-challenge-1\\Jake\\aggregate-input.csv'
output_file = 'D:\\Repos\\hackathon-nov23-team-3\\sas2python-challenge-1\\Jake\\aggregate-output-test.csv'

aggregate(input_file, output_file)
