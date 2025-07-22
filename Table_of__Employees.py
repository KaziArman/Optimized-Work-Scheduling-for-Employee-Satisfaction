import pandas as pd
import matplotlib.pyplot as plt
import employeedata as ed

# Load employee availability and desired work hours data
empl_avail = ed.empl_avail
empl_hours = ed.empl_hours
employee_ids = list(range(len(empl_avail)))
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Prepare the data for each employee
table_data = {
    "Employee ID": [f"Emp {emp_id}" for emp_id in employee_ids],
    "Min Desired Work Hour": [empl_hours[emp_id][0] for emp_id in employee_ids],
    "Max Desired Work Hour": [empl_hours[emp_id][1] for emp_id in employee_ids],
    "Total Availability (Hours/Week)": [
        sum([empl_avail[emp_id][day].count(1) for day in range(5)]) for emp_id in employee_ids
    ]
}

# Create a DataFrame for the table
df_table = pd.DataFrame(table_data)

# Display the table using matplotlib
plt.figure(figsize=(12, 8))
plt.axis('off')
tbl = plt.table(cellText=df_table.values, colLabels=df_table.columns, cellLoc='center', loc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1.2, 1.5)

# Set the title
plt.title("Employee Availability and Desired Work Hours Summary", fontsize=14, fontweight='bold')
plt.show()
