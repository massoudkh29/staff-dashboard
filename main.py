import pandas as pd

# Show all rows and all columns in the console
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Load Excel file
file_path = 'data/Staff Skills.xlsx'
df = pd.read_excel(file_path)

# Print raw table
print("Raw Data:")
print(df)

# Convert 'X' and 'x' to 1, blanks to 0 — skipping Name and Tasks columns
binary_df = df.copy()
for col in df.columns[2:]:
    binary_df[col] = df[col].apply(lambda x: 1 if str(x).strip().lower() == 'x' else 0)

# Print cleaned binary table
print("\nBinary Skills Table:")
print(binary_df)
