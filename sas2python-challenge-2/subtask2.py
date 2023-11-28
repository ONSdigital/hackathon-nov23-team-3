import pandas as pd
import numpy as np
from scipy import stats
import math

def round_sig(x, sig=10):
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)

def analyze_distribution(filename, column):
    # Read the CSV file
    df = pd.read_csv(filename)

    # Extract the specified column
    data = df[column]

    # List of distributions to check
    distributions = ['norm', 'expon', 'lognorm', 'gamma', 'beta', 'chi2']

    # Initialize variables to store the best distribution and highest KS statistic
    best_distribution = ''
    highest_ks_statistic = -1

    # Perform the Kolmogorov-Smirnov test for each distribution
    for distribution in distributions:
        dist = getattr(stats, distribution)
        param = dist.fit(data)
        ks_statistic, p_value = stats.kstest(data, distribution, args=param)

        # If the KS statistic for this distribution is higher than the current highest, update the best distribution and highest KS statistic
        if ks_statistic > highest_ks_statistic:
            best_distribution = distribution
            highest_ks_statistic = ks_statistic

    # Return the best distribution
    return best_distribution


def generate_synthetic_data(input_file, output_file, num_rows, distribution='norm'):
    # Read the input CSV file
    df = pd.read_csv(input_file)

    # Create a DataFrame for the synthetic data
    df_synthetic = pd.DataFrame()

    # For each column in the original DataFrame
    for column in df.columns:
        if column == 'TS_PERIOD':
            # If the column is 'TS_PERIOD', generate unique quarterly periods
            start_year = df['TS_PERIOD'].str[:4].astype(int).min()
            end_year = start_year + (num_rows // 4) + 1
            quarters = ['Q1', 'Q2', 'Q3', 'Q4']
            ts_periods = [f'{year}{quarter}' for year in range(start_year, end_year) for quarter in quarters]
            df_synthetic['TS_PERIOD'] = ts_periods[:num_rows]
        elif df[column].dtype == np.float64 or df[column].dtype == np.int64:
            # If the column is numerical, generate synthetic data with a similar distribution
            mean = df[column].mean()
            std = df[column].std()
            if distribution == 'norm':
                synthetic_data = np.random.normal(loc=mean, scale=std, size=num_rows)
            elif distribution == 'expon':
                synthetic_data = np.random.exponential(scale=mean, size=num_rows)
            elif distribution == 'lognorm':
                synthetic_data = np.random.lognormal(mean=mean, sigma=std, size=num_rows)
            elif distribution == 'gamma':
                synthetic_data = np.random.gamma(shape=mean, scale=std, size=num_rows)
            elif distribution == 'beta':
                synthetic_data = np.random.beta(a=mean, b=std, size=num_rows)
            elif distribution == 'chi2':
                synthetic_data = np.random.chisquare(df=mean, size=num_rows)
            else:
                raise ValueError(f"Invalid distribution: {distribution}")
            df_synthetic[column] = synthetic_data
        else:
            # If the column is non-numerical, randomly sample from the original data
            synthetic_data = np.random.choice(df[column], size=num_rows)
            df_synthetic[column] = synthetic_data
    
    # Change'TS_VALUE' column to 10 significant figures
    df_synthetic['TS_VALUE'] = df_synthetic['TS_VALUE'].apply(round_sig)

    # Write the synthetic data to a CSV file
    df_synthetic.to_csv(output_file, index=False)

# Define the input and output file paths
input_file = 'D:\\Repos\\hackathon-nov23-team-3\\sas2python-challenge-1\\aggregate-input.csv'
output_file ='D:\\Repos\\hackathon-nov23-team-3\\sas2python-challenge-2\\synthetic.csv'

distribution = analyze_distribution(input_file, 'TS_VALUE')

print(f'Best distribution: {distribution}')

# Call the function to generate synthetic data
generate_synthetic_data(input_file, output_file, 10000, distribution)





