import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the Excel data
file_path = "employee_schedule.xlsx"  # Update with the correct file path if needed
schedule_df = pd.read_excel(file_path)
employee_schedule = schedule_df

# Convert columns to appropriate data types
employee_schedule["Day"] = employee_schedule["Day"].astype(int)
employee_schedule["Hour"] = employee_schedule["Hour"].astype(int)
employee_schedule["Role"] = employee_schedule["Role"].astype(str)

# Define the mapping for day names and roles
day_labels = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday"}
role_labels = {'C': 'Cook', 'E': 'Expo', 'F': 'Front Counter', 'R': 'Runner', 'D': 'Dishwasher'}
role_colors = {'C': 'skyblue', 'E': 'orange', 'F': 'green', 'R': 'purple', 'D': 'yellow'}

# Prepare Gantt chart data for the selected employee
def gantt_empl(x):
    gantt_data = []
    employee_id = x  # Change this to the desired employee ID
    employee_schedule = schedule_df[schedule_df["Employee"] == employee_id]
    for day in [4, 3, 2, 1, 0]:  # From Day 0 (Monday) to Day 4 (Friday)
        day_name = day_labels[day]
        day_data = employee_schedule[employee_schedule["Day"] == day]
        for role in day_data["Role"].unique():
            role_data = day_data[day_data["Role"] == role]
            for hour in role_data["Hour"].unique():
                start_hour = hour - 1  # Shift by 1 to align with the Gantt chart interpretation
                end_hour = hour
                gantt_data.append((day_name, start_hour, end_hour, role))
    return gantt_data

# Prepare Gantt chart data for all employees
def gantt_all():
    gantt_data = []
    for day in [4, 3, 2, 1, 0]:  # From Day 4 (Friday) to Day 0 (Monday)
        day_name = day_labels[day]
        day_data = schedule_df[schedule_df["Day"] == day]
        for employee_id in sorted(schedule_df["Employee"].unique()):
            emp_data = day_data[day_data["Employee"] == employee_id]
            for role in emp_data["Role"].unique():
                role_data = emp_data[emp_data["Role"] == role]
                for hour in role_data["Hour"].unique():
                    start_hour = hour - 1  # Shift by 1 to align with the Gantt chart interpretation
                    end_hour = hour
                    gantt_data.append((f"Emp {employee_id} - {day_name}", start_hour, end_hour, role))
    return gantt_data

# Step 3: Plot the Gantt chart for all employees
fig, ax = plt.subplots(figsize=(14, 8))
gantt_data = gantt_all() # For all the employees
#gantt_data = gantt_empl(3) # For single employees
for i, (label, start, end, role) in enumerate(gantt_data):
    ax.barh(label, (end - start), left=start, color=role_colors[role], edgecolor='black', label=role_labels[role])

# Set labels and title
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("Employee and Day")
ax.set_title("Gantt Chart for All Employees' Schedules")
ax.set_xticks(range(0, 14))
ax.set_xticklabels(range(0, 14))

# Remove duplicate legend entries
handles, labels = ax.get_legend_handles_labels()
unique_legend = dict(zip(labels, handles))
ax.legend(unique_legend.values(), unique_legend.keys(), title="Role", loc="upper right")

# Display the grid and the Gantt chart
plt.grid(visible=True, color='black', linestyle='--', linewidth=0.7)
plt.show()

