import pandas as pd
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Join the directory with the filename
file_path = os.path.join(script_dir, 'provider_summary.sas7bdat')

# Load the SAS dataset
provider_summary = pd.read_sas(file_path)

# Join the directory with the output filename
output_file_path = os.path.join(script_dir, 'provider_summary.csv')

# Write the DataFrame to a CSV file
provider_summary.to_csv(output_file_path, index=False)
