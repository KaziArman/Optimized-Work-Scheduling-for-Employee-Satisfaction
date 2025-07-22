import pandas as pd
import matplotlib.pyplot as plt
import importlib.util

# Load the employee schedule and required staffing data
schedule_file_path = "employee_schedule_clean.csv"
employeedata_file_path = "employeedata.py"
staffingdata_file_path = "staffingdata.py"

# Load the schedule data
schedule_df = pd.read_csv(schedule_file_path)

# Load employeedata.py and staffingdata.py
spec_emp = importlib.util.spec_from_file_location("employeedata", employeedata_file_path)
employeedata = importlib.util.module_from_spec(spec_emp)
spec_emp.loader.exec_module(employeedata)

spec_staff = importlib.util.spec_from_file_location("staffingdata", staffingdata_file_path)
staffingdata = importlib.util.module_from_spec(spec_staff)
spec_staff.loader.exec_module(staffingdata)

# Role mappings and required employee data
role_labels = {'C': 'Cook', 'E': 'Expo', 'F': 'Front Counter', 'R': 'Runner', 'D': 'Dishwasher'}
role_reqs = staffingdata.role_reqs
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Function to generate the comparison chart for a given day
def svr_day(day="Monday"):
    if day.capitalize() not in days and day.lower() != "all":
        print("Invalid input. Please choose a day (Monday to Friday) or 'all' for all days.")
        return

    if day.lower() == "all":
        # Generate charts for all days from Monday to Friday
        for single_day in days:
            create_chart(single_day)
    else:
        # Generate chart for the specific day
        create_chart(day.capitalize())

# Helper function to create the chart for a single day
def create_chart(day):
    # Get the day index for staffing requirements (0: Monday, 1: Tuesday, ..., 4: Friday)
    day_idx = days.index(day)

    # Filter the data for the selected day
    day_data = schedule_df[schedule_df["Day"] == day]

    # Count occurrences of employees for each role
    scheduled_counts = day_data.groupby("Role")["Employee"].count().reindex(role_labels.keys(), fill_value=0)

    # Calculate required employee counts for each role
    required_counts = [
        sum(role_reqs['C'][day_idx]),  # Cook
        sum(role_reqs['E'][day_idx]),  # Expo
        sum(role_reqs['F'][day_idx]),  # Front Counter
        sum(role_reqs['R'][day_idx]),  # Runner
        sum(role_reqs['D'][day_idx])   # Dishwasher
    ]

    # Role labels and scheduled values for plotting
    roles = list(role_labels.values())
    scheduled_values = scheduled_counts.values

    # Create the dual-axis comparison plot
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Define the positions and bar width
    y_pos = range(len(roles))
    bar_width = 0.4

    # Plot scheduled employees (primary axis)
    ax1.barh(y_pos, scheduled_values, height=bar_width, color='green', edgecolor='black', label='Scheduled Employees')
    ax1.set_xlabel("Scheduled Employees", color='green', fontweight='bold')
    ax1.tick_params(axis='x', colors='green')

    # Create secondary axis for required employees
    ax2 = ax1.twiny()
    ax2.barh([p + bar_width for p in y_pos], required_counts, height=bar_width, color='red', edgecolor='black', label='Required Employees', hatch='//')
    ax2.set_xlabel("Required Employees", color='red', fontweight='bold')
    ax2.tick_params(axis='x', colors='red')

    # Set labels, title, and legend
    ax1.set_yticks([p + bar_width / 2 for p in y_pos])
    ax1.set_yticklabels(roles, fontweight='bold')
    plt.title(f"Comparison of Scheduled vs. Required Employees for {day}", fontsize=16, fontweight='bold')

    # Display legends
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    # Display grid lines for clarity
    ax1.axvline(x=0, color='black', linewidth=1)
    plt.grid(visible=True, linestyle='--', color='grey', linewidth=0.5)

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.show()

# Example usage:
svr_day("Monday")  # For a specific day
#svr_day("all")     # For all days (Monday to Friday)


