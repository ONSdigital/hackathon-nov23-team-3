import pandas as pd

# Read the input CSV file
df = pd.read_csv('D:\\Repos\\hackathon-nov23-team-3\\sas2python-challenge-2\conround-input.csv')

# Round the 'TS_VALUE' column to 2 decimal places
df['TS_VALUE'] = round(df['TS_VALUE'], 2)

# Write the DataFrame to an output CSV file
df.to_csv('D:\\Repos\\hackathon-nov23-team-3\\sas2python-challenge-2\conround-output-test.csv', index=False)