import pandas as pd
import importlib.util

# File paths
schedule_file_path = "employee_schedule_clean.csv"
employeedata_file_path = "employeedata.py"
staffingdata_file_path = "staffingdata.py"
# Load the employee schedule data
schedule_df = pd.read_csv(schedule_file_path)

# Load employeedata.py dynamically
spec_emp = importlib.util.spec_from_file_location("employeedata", employeedata_file_path)
employeedata = importlib.util.module_from_spec(spec_emp)
spec_emp.loader.exec_module(employeedata)

# Load stuffingdata.py dynamically
spec_emp = importlib.util.spec_from_file_location("staffingdata", staffingdata_file_path)
staffingdata = importlib.util.module_from_spec(spec_emp)
spec_emp.loader.exec_module(staffingdata)

# Extract the employee hours data from employeedata.py
empl_hours = employeedata.empl_hours
employees = range(len(empl_hours))

# Initialize a dictionary to store the scheduled hours for each employee
scheduled_hours = {e: 0 for e in employees}

# Calculate the total scheduled hours for each employee across the entire week
for e in employees:
    # Count the total number of hours scheduled for this employee in the schedule data
    scheduled_hours[e] = schedule_df[schedule_df["Employee"].astype(str) == str(e)].shape[0]

# Update the deviation calculation to include both over_schedule and under_schedule values in the table
def deviation():
    # Initialize a list to store the updated data
    deviation_data = []

    # Calculate the deviation for each employee, including over-schedule and under-schedule
    for e in employees:
        min_hours, max_hours = empl_hours[e]
        total_scheduled = scheduled_hours[e]

        # Calculate over-schedule and under-schedule
        over_schedule = max(0, total_scheduled - max_hours)
        #over_schedule = total_scheduled - max_hours
        under_schedule = max(0, min_hours - total_scheduled)
        #under_schedule = min_hours - total_scheduled
        deviation = max(over_schedule, under_schedule)

        # Store the results in the list
        deviation_data.append([e, min_hours, max_hours, total_scheduled, over_schedule, under_schedule, deviation])

    # Create a DataFrame to display the results
    deviation_df = pd.DataFrame(deviation_data, columns=["Employee", "Min Hours", "Max Hours", "Scheduled Hours", "Over Schedule", "Under Schedule", "Deviation"])

    # Display the DataFrame using print() and save it as a CSV file
    return deviation_df

# Calculate the total required and scheduled hours for each role across the entire week
def role():
    # Initialize dictionaries to store the total required and scheduled hours for each role
    role_labels = {'C': 'Cook', 'E': 'Expo', 'F': 'Front Counter', 'R': 'Runner', 'D': 'Dishwasher'}
    roles = role_labels.keys()
    total_required_hours = {role: 0 for role in roles}
    total_scheduled_hours = {role: 0 for role in roles}

    # Calculate the total required hours for each role based on staffingdata.py
    for role in roles:
        for day in range(5):  # 0: Monday, ..., 4: Friday
            total_required_hours[role] += sum(staffingdata.role_reqs[role][day])

    # Calculate the total scheduled hours for each role based on the employee schedule
    for role in roles:
        total_scheduled_hours[role] = schedule_df[schedule_df["Role"] == role].shape[0]

    # Create a DataFrame to display the total required and scheduled hours for each role
    role_data = []
    for role in roles:
        role_data.append([role_labels[role], total_required_hours[role], total_scheduled_hours[role]])

    # Create the DataFrame
    role_summary_df = pd.DataFrame(role_data, columns=["Role", "Total Required Hours", "Total Scheduled Hours"])

    # Display the DataFrame to the user
    return role_summary_df


deviation_df = deviation()
role_summary_df = role()
# Save the DataFrame to a CSV file
deviation_df.to_csv("employee_deviation_table.csv", index=False)
role_summary_df.to_csv("role_summary_table.csv", index=False)