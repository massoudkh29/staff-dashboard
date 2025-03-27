import pandas as pd

# Show full output
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Load Excel file
file_path = 'data/admin_hours.xlsx'

# Days of the week in order
days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']

rows = []

for i, day in enumerate(days):
    start_row = i * 3
    df = pd.read_excel(file_path, skiprows=start_row, nrows=2, header=None)

    if df.shape[0] < 2:
        continue  # Skip empty/malformed blocks

    names = df.iloc[0, 1:].tolist()
    shifts = df.iloc[1, 1:].tolist()

    # Try to read the third row (lunch) if it exists
    lunch_row = None
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

# Build final DataFrame
admin_schedule_df = pd.DataFrame(rows)

# Show full output
print("\n🗓️ Cleaned Admin Hours Table (with Lunch):")
print(admin_schedule_df)
