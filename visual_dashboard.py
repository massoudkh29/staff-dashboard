import pandas as pd
import matplotlib.pyplot as plt

# Display settings
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# ------------------------
# Load Staff Skills Matrix
# ------------------------
skills_df = pd.read_excel("data/Staff Skills.xlsx")

# Clean skills: convert X/x → 1, blanks → 0
for col in skills_df.columns[2:]:
    skills_df[col] = skills_df[col].apply(lambda x: 1 if str(x).strip().lower() == 'x' else 0)

# ------------------------
# Function: Load staff working on a specific day
# ------------------------
def load_staff_for_day(file_path, day_index):
    start_row = day_index * 3
    df = pd.read_excel(file_path, skiprows=start_row, nrows=2, header=None)

    if df.shape[0] < 2:
        return []

    names = df.iloc[0, 1:].tolist()
    shifts = df.iloc[1, 1:].tolist()

    return [name for name, shift in zip(names, shifts) if isinstance(shift, str) and shift.strip().upper() != 'OFF']

# ------------------------
# Loop through each weekday
# ------------------------
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

for i, day in enumerate(days):
    # Load working staff from all three sources
    admin_staff = load_staff_for_day("data/admin_hours.xlsx", i)
    reception1 = load_staff_for_day("data/reception_hours1.xlsx", i)
    reception2 = load_staff_for_day("data/reception_hours2.xlsx", i)

    working_staff = admin_staff + reception1 + reception2

    if not working_staff:
        print(f"No working staff found for {day}.")
        continue

    # Filter skills by working staff
    available_df = skills_df[skills_df['Name'].isin(working_staff)]

    # ------------------------
    # Chart 1: Task vs Staff Count
    # ------------------------
    task_coverage = available_df.iloc[:, 2:].sum().sort_values(ascending=True)

    plt.figure(figsize=(10, 12))
    task_coverage.plot(kind='barh', color='skyblue')
    plt.title(f"🗓️ {day} - Task Coverage by Available Staff")
    plt.xlabel("Number of Available Staff")
    plt.ylabel("Task")
    plt.tight_layout()
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.show()

    # ------------------------
    # Chart 2: Staff vs Task Count
    # ------------------------
    staff_task_counts = available_df.set_index('Name').iloc[:, 1:].sum(axis=1).sort_values(ascending=True)

    plt.figure(figsize=(10, 6))
    staff_task_counts.plot(kind='barh', color='mediumseagreen')
    plt.title(f"🧑‍💼 {day} - Staff vs Number of Tasks They Can Cover")
    plt.xlabel("Number of Tasks")
    plt.ylabel("Staff")
    plt.tight_layout()
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.show()
