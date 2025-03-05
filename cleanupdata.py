# Very simple program to clean up csv files using the pandas package
import pandas as pd

initial_file = pd.read_csv('your_csv_file.csv')

# Remove rows that are missing all entries
file_with_empty_rows_removed = initial_file.dropna(how='all')

# Replace missing entries with "None"
cleaned_file = file_with_empty_rows_removed.fillna("None")

# Convert the cleaned up file into a csv file
cleaned_file.to_csv('your_output_file.csv', index=False)