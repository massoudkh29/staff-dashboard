import pandas as pd

# Show all columns and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Load file
file_path = 'data/reception_hours2.xlsx'

# Days covered in this sheet
days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']

rows = []

for i, day in enumerate(days):
    start_row = i * 3
    # Read shift and lunch rows (2 rows per block)
    df = pd.read_excel(file_path, skiprows=start_row, nrows=2, header=None)

    if df.shape[0] < 2:
        continue  # skip incomplete blocks

    names = df.iloc[0, 1:].tolist()     # R6, R7, R8, R9
    shifts = df.iloc[1, 1:].tolist()    # Shift times

    # Try to read lunch row (third row)
    try:
        lunch_row = pd.read_excel(file_path, skiprows=start_row + 2, nrows=1, header=None).iloc[0, 1:].tolist()
    except:
        lunch_row = [''] * len(names)

    for name, shift_time, lunch_time in zip(names, shifts, lunch_row):
        rows.append({
            'Day': day.capitalize(),
            'Name': name,
            'Shift': shift_time if pd.notna(shift_time) else '',
            'Lunch': lunch_time if pd.notna(lunch_time) else ''
        })

# Create DataFrame
reception_df2 = pd.DataFrame(rows)

# Print cleaned data
print("\n📋 Cleaned Reception Hours Table (R6–R9):")
print(reception_df2)
