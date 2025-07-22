import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the Excel data
file_path = "employee_schedule_clean.csv"  # Update with the correct file path if needed
schedule_df = pd.read_csv(file_path)
employee_schedule = schedule_df

# Define the mapping dictionary
day_mapping = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}

# Replace the Day column values based on the mapping
employee_schedule["Day"] = employee_schedule["Day"].map(day_mapping)

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
    # Step 3: Plot the Gantt chart for single employees
    fig, ax = plt.subplots(figsize=(14, 8));  
    for i, (label, start, end, role) in enumerate(gantt_data):
        ax.barh(label, (end - start), left=start, color=role_colors[role], edgecolor='black', label=role_labels[role])
    # Set labels and title
    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Day")
    ax.set_title(f"Gantt Chart for Employee {employee_id}'s Schedules")
    ax.set_xticks(range(0, 14))
    ax.set_xticklabels(range(0, 14))
    # Remove duplicate legend entries
    handles, labels = ax.get_legend_handles_labels()
    unique_legend = dict(zip(labels, handles))
    ax.legend(unique_legend.values(), unique_legend.keys(), title="Role", loc="upper right")
    # Display the grid and the Gantt chart
    plt.grid(visible=True, color='black', linestyle='--', linewidth=0.7);
    return plt.show()

# Prepare Gantt chart data for the selected employee
# Define the function to create a side-by-side Gantt chart for three selected employees
def gantt_sel_empls(x, y, z):
    employee_ids = [x, y, z]  # List of the three employee IDs

    # Create a figure with three subplots (side-by-side for each employee)
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 8), sharex=True, sharey=True)

    # Iterate over the three employee IDs and their respective subplots
    for idx, (employee_id, ax) in enumerate(zip(employee_ids, axes)):
        gantt_data = []
        # Filter the schedule data for the current employee
        employee_schedule = schedule_df[schedule_df["Employee"] == employee_id]

        # Prepare the Gantt chart data for the current employee
        for day in [4, 3, 2, 1, 0]:  # From Day 4 (Friday) to Day 0 (Monday)
            day_name = day_labels[day]
            day_data = employee_schedule[employee_schedule["Day"] == day]
            for role in day_data["Role"].unique():
                role_data = day_data[day_data["Role"] == role]
                for hour in role_data["Hour"].unique():
                    start_hour = hour - 1  # Shift by 1 to align with the Gantt chart interpretation
                    end_hour = hour
                    gantt_data.append((day_name, start_hour, end_hour, role))

        # Plot the Gantt chart for the current employee
        for (label, start, end, role) in gantt_data:
            ax.barh(label, (end - start), left=start, color=role_colors[role], edgecolor='black', label=role_labels[role])

        # Set labels and title for each subplot
        ax.set_xlabel("Hour of the Day")
        ax.set_title(f"Employee {employee_id}'s Schedule")
        ax.set_xticks(range(0, 14))
        ax.set_xticklabels(range(0, 14))

    # Set the shared y-axis labels (days of the week)
    axes[0].set_ylabel("Day of the Week")
    axes[0].set_yticks(list(day_labels.values()))
    axes[0].set_yticklabels(list(day_labels.values()))

    # Remove duplicate legend entries and add a single legend
    handles, labels = axes[0].get_legend_handles_labels()
    unique_legend = dict(zip(labels, handles))
    #fig.legend(unique_legend.values(), unique_legend.keys(), title="Role", loc="upper right")

    # Display the grid for each subplot
    for ax in axes:
        ax.grid(visible=True, color='black', linestyle='--', linewidth=0.7)

    # Adjust layout for better spacing
    plt.tight_layout()
    return plt.show()



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
    # Step 3: Plot the Gantt chart for all employees
    fig, ax = plt.subplots(figsize=(14, 8));  
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
    plt.grid(visible=True, color='black', linestyle='--', linewidth=0.7);
    return plt.show()  

# A Gantt chart for all employees for a specific day
def gantt_day(day_name):
    # Map the day name to the corresponding index
    day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}
    if day_name not in day_map:
        print("Invalid day name. Please choose from: Monday, Tuesday, Wednesday, Thursday, Friday.")
        return

    # Get the corresponding day index
    day_index = day_map[day_name]

    # Prepare Gantt chart data for the specified day
    gantt_data = []
    day_data = schedule_df[schedule_df["Day"] == day_index]
    for employee_id in sorted(schedule_df["Employee"].unique()):
        emp_data = day_data[day_data["Employee"] == employee_id]
        for role in emp_data["Role"].unique():
            role_data = emp_data[emp_data["Role"] == role]
            for hour in role_data["Hour"].unique():
                start_hour = hour - 1  # Shift by 1 to align with the Gantt chart interpretation
                end_hour = hour
                gantt_data.append((f"Emp {employee_id}", start_hour, end_hour, role))
    # Step 3: Plot the Gantt chart for all employees on the specified day
    fig, ax = plt.subplots(figsize=(14, 8))
    for i, (label, start, end, role) in enumerate(gantt_data):
        ax.barh(label, (end - start), left=start, color=role_colors[role], edgecolor='black', label=role_labels[role])
    # Set labels and title
    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Employee")
    ax.set_title(f"Gantt Chart for All Employees' Schedules on {day_name}")
    ax.set_xticks(range(0, 14))
    ax.set_xticklabels(range(0, 14))
    # Remove duplicate legend entries
    handles, labels = ax.get_legend_handles_labels()
    unique_legend = dict(zip(labels, handles))
    ax.legend(unique_legend.values(), unique_legend.keys(), title="Role", loc="upper right")
    # Display the grid and the Gantt chart
    plt.grid(visible=True, color='black', linestyle='--', linewidth=0.7)
    return plt.show()

#gantt_all() # For all the employees
#gantt_empl(3) # For single employees
#gantt_day("Monday") # For all employees in a single day
gantt_sel_empls(1, 4, 9)
