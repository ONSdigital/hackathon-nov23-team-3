import pandas as pd

def aggregate(ts_value, periodicity, basis):
    periodicity = periodicity.upper()
    basis = basis.upper()

    print(f'ts_value= {ts_value}')
    print(f'periodicity= {periodicity}')
    print(f'basis= {basis}')

    # Open the input dataset
    try:
        df = pd.read_csv(ts_value)  # Assuming the input is a CSV file
    except Exception as e:
        print(f"ERROR in 'aggregate' function - Cannot open {ts_value} file")
        return

    # Check if the column '___pdicity' exists
    if '___pdicity' in df.columns:
        pdicity_exists = True
    else:
        pdicity_exists = False

    print(f'pdicity_exists= {pdicity_exists}')