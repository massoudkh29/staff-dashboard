import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit setup
st.set_page_config(layout="wide")
st.title("📊 Staff Task Coverage Dashboard")

# Select day
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
selected_day = st.selectbox("Select a day to view coverage", days)

# Load staff skills
skills_df = pd.read_excel("data/Staff Skills.xlsx")

# Clean skills (convert X/x → 1)
for col in skills_df.columns[2:]:
    skills_df[col] = skills_df[col].apply(lambda x: 1 if str(x).strip().lower() == 'x' else 0)

# Helper: Load staff on a specific day
def load_staff_for_day(file_path, day_index):
    start_row = day_index * 3
    df = pd.read_excel(file_path, skiprows=start_row, nrows=2, header=None)
    if df.shape[0] < 2:
        return []
    names = df.iloc[0, 1:].tolist()
    shifts = df.iloc[1, 1:].tolist()
    return [name for name, shift in zip(names, shifts) if isinstance(shift, str) and shift.strip().upper() != 'OFF']

# Load working staff for selected day
i = days.index(selected_day)
admin_staff = load_staff_for_day("data/admin_hours.xlsx", i)
reception1 = load_staff_for_day("data/reception_hours1.xlsx", i)
reception2 = load_staff_for_day("data/reception_hours2.xlsx", i)
working_staff = admin_staff + reception1 + reception2

# Filter skill matrix
available_df = skills_df[skills_df['Name'].isin(working_staff)]

# Chart 1: Task Coverage
task_coverage = available_df.iloc[:, 2:].sum().sort_values(ascending=True)

st.subheader(f"🗓️ Task Coverage on {selected_day}")
fig1, ax1 = plt.subplots(figsize=(10, 12))
task_coverage.plot(kind='barh', color='skyblue', ax=ax1)
ax1.set_xlabel("Number of Available Staff")
ax1.set_title(f"Task Coverage on {selected_day}")
ax1.grid(axis='x', linestyle='--', alpha=0.5)
st.pyplot(fig1)

# Chart 2: Staff Coverage
staff_task_counts = available_df.set_index('Name').iloc[:, 1:].sum(axis=1).sort_values(ascending=True)

st.subheader(f"🧑‍💼 Staff Capacity on {selected_day}")
fig2, ax2 = plt.subplots(figsize=(10, 6))
staff_task_counts.plot(kind='barh', color='mediumseagreen', ax=ax2)
ax2.set_xlabel("Number of Tasks")
ax2.set_title(f"Staff vs. Tasks on {selected_day}")
ax2.grid(axis='x', linestyle='--', alpha=0.5)
st.pyplot(fig2)
