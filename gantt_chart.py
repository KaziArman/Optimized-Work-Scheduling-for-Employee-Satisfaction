import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the Excel data
file_path = "employee_schedule_clean.csv"  # Update with the correct file path if needed
schedule_df = pd.read_csv(file_path)
employee_schedule = schedule_df

# Define the mapping dictionaries
day_mapping = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}
day_labels = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday"}
role_labels = {'C': 'Cook', 'E': 'Expo', 'F': 'Front Counter', 'R': 'Runner', 'D': 'Dishwasher'}
role_colors = {'C': '#D46F1A', 'E': '#ECA61D', 'F': '#D6841F', 'R': '#F2D200', 'D': '#C1C1C1'}

# Map Day column values and convert data types
schedule_df["Day"] = schedule_df["Day"].map(day_mapping)
schedule_df["Hour"] = schedule_df["Hour"].astype(int)

# Generate Gantt chart for all employees
def gantt_all():
    gantt_data = []
    for day in range(5):  # From Monday (0) to Friday (4)
        day_name = day_labels[day]
        day_data = schedule_df[schedule_df["Day"] == day]
        for employee_id in sorted(schedule_df["Employee"].unique()):
            emp_data = day_data[day_data["Employee"] == employee_id]
            for role in emp_data["Role"].unique():
                role_data = emp_data[emp_data["Role"] == role]
                for hour in role_data["Hour"].unique():
                    start_hour = hour # Shift by 1 to align with the Gantt chart interpretation
                    end_hour = hour
                    gantt_data.append((f"Emp {employee_id} - {day_name}", start_hour, end_hour, role))
    
    # Plot the Gantt chart for all employees
    fig, ax = plt.subplots(figsize=(14, 8))
    for label, start, end, role in gantt_data:
        ax.barh(label, (end - start), left=start, color=role_colors.get(role[0], '#C1C1C1'), 
                label=role_labels.get(role[0], 'Unknown Role'))

    # Set labels and title
    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Employee and Day")
    ax.set_title("Gantt Chart for All Employees' Schedules")
    # Map 1-12 to "9 AM", "10 AM", ..., "8 PM"
    hour_labels = {
        1: "9 AM", 2: "10 AM", 3: "11 AM", 4: "12 PM",
        5: "1 PM", 6: "2 PM", 7: "3 PM", 8: "4 PM",
        9: "5 PM", 10: "6 PM", 11: "7 PM", 12: "8 PM"
    }
    ax.set_xticks(list(hour_labels.keys()))
    ax.set_xticklabels([hour_labels[hour] for hour in hour_labels])

    # Remove duplicate legend entries
    handles, labels = ax.get_legend_handles_labels()
    unique_legend = dict(zip(labels, handles))
    ax.legend(unique_legend.values(), unique_legend.keys(), title="Role", loc="upper right")

    # Display the grid and the Gantt chart
    #plt.grid(visible=False, color='black', linestyle='--', linewidth=0.7)
    plt.tight_layout()
    plt.show()
# Gantt chart for all employees for a specific day
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
                start_hour = hour  # Shift by 1 to align with the Gantt chart interpretation
                end_hour = hour
                gantt_data.append((f"Emp {employee_id}", start_hour, end_hour, role))

    # Plot the Gantt chart for the specified day
    fig, ax = plt.subplots(figsize=(14, 8))
    for label, start, end, role in gantt_data:
        ax.barh(label, (end - start+1), left=start, color=role_colors.get(role[0], '#C1C1C1'),
                label=role_labels.get(role[0], 'Unknown Role'))

    # Set labels and title
    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Employee")
    ax.set_title(f"Gantt Chart for All Employees' Schedules on {day_name}")
    # Map 1-12 to "9 AM", "10 AM", ..., "8 PM"
    hour_labels = {
        1: "9 AM", 2: "10 AM", 3: "11 AM", 4: "12 PM",
        5: "1 PM", 6: "2 PM", 7: "3 PM", 8: "4 PM",
        9: "5 PM", 10: "6 PM", 11: "7 PM", 12: "8 PM"
    }
    ax.set_xticks(list(hour_labels.keys()))
    ax.set_xticklabels([hour_labels[hour] for hour in hour_labels])

    # Remove duplicate legend entries
    handles, labels = ax.get_legend_handles_labels()
    unique_legend = dict(zip(labels, handles))
    ax.legend(unique_legend.values(), unique_legend.keys(), title="Role", loc="upper right")

    # Display the grid and the Gantt chart
    #plt.grid(visible=False, color='black', linestyle='--', linewidth=0.7)
    plt.tight_layout()
    plt.show()
# Define the function to create a side-by-side Gantt chart for three selected employees
def gantt_sel_empls(emp1, emp2, emp3):
    employee_ids = [emp1, emp2, emp3]  # List of the three employee IDs

    # Create a figure with three subplots (side-by-side for each employee)
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 8), sharex=True, sharey=True)

    # Iterate over the three employee IDs and their respective subplots
    for idx, (employee_id, ax) in enumerate(zip(employee_ids, axes)):
        gantt_data = []
        # Filter the schedule data for the current employee
        employee_schedule = schedule_df[schedule_df["Employee"] == employee_id]

        # Prepare the Gantt chart data for the current employee
        for day in [4, 3, 2, 1, 0]:  # From Friday (4) to Monday (0)
            day_name = day_labels[day]
            day_data = employee_schedule[employee_schedule["Day"] == day]
            for role in day_data["Role"].unique():
                role_data = day_data[day_data["Role"] == role]
                for hour in role_data["Hour"].unique():
                    start_hour = hour - 1  # Shift by 1 to align with the Gantt chart interpretation
                    end_hour = hour
                    gantt_data.append((day_name, start_hour, end_hour, role))

        # Plot the Gantt chart for the current employee
        for label, start, end, role in gantt_data:
            ax.barh(label, (end - start), left=start, color=role_colors.get(role[0], '#C1C1C1'),
                    label=role_labels.get(role[0], 'Unknown Role'))

        # Set labels and title for each subplot
        ax.set_xlabel("Hour of the Day")
        ax.set_title(f"Employee {employee_id}'s Schedule")
        hour_labels = {
            1: "9 AM", 2: "10 AM", 3: "11 AM", 4: "12 PM",
            5: "1 PM", 6: "2 PM", 7: "3 PM", 8: "4 PM",
            9: "5 PM", 10: "6 PM", 11: "7 PM", 12: "8 PM"}
        ax.set_xticks(list(hour_labels.keys()))
        ax.set_xticklabels([hour_labels[hour] for hour in hour_labels])

    # Set the shared y-axis labels (days of the week)
    axes[0].set_ylabel("Day of the Week")
    axes[0].set_yticks([4, 3, 2, 1, 0])  # Correct order: Friday to Monday
    axes[0].set_yticklabels(["Friday", "Thursday", "Wednesday", "Tuesday", "Monday"])

    # Remove duplicate legend entries and add a single legend
    handles, labels = axes[0].get_legend_handles_labels()
    unique_legend = dict(zip(labels, handles))
    fig.legend(unique_legend.values(), unique_legend.keys(), title="Role", loc="upper center", bbox_to_anchor=(0.5, 1.1), ncol=5)

    # Display the grid for each subplot
    '''for ax in axes:
        ax.grid(visible=False, color='black', linestyle='--', linewidth=0.7)'''

    # Adjust layout for better spacing
    plt.tight_layout()
    plt.show()

# Call the function to generate the Gantt chart for three selected employees
#gantt_sel_empls(11, 12, 13)

# Call the function with a specific day, e.g., "Monday" or "Tuesday"
gantt_day("Monday")

# Call the function to generate the Gantt chart
#gantt_all()
