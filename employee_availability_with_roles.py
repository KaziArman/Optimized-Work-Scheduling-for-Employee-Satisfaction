import pandas as pd
import matplotlib.pyplot as plt
import employeedata as ed
import staffingdata as sd

# Define the function to create a side-by-side Gantt chart for multiple employees
def gantt_employee_availability_with_roles(*employee_ids):
    empl_avail = ed.empl_avail
    empl_roles = ed.empl_roles  # Employee role eligibility from employeedata
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    hours = list(range(12))
    gantt_color = 'skyblue'  # Consistent color for all employees in the Gantt chart
    role_labels = {'C': 'Cook', 'E': 'Expo', 'F': 'Front Counter', 'R': 'Runner', 'D': 'Dishwasher'}
    role_colors = {'C': 'skyblue', 'E': 'orange', 'F': 'green', 'R': 'purple', 'D': 'yellow'}
    roles = list(role_labels.keys())

    # Check if the provided employee IDs are valid
    if len(employee_ids) != 3:
        print("Please provide exactly three employee IDs for the side-by-side Gantt chart.")
        return

    for employee_id in employee_ids:
        if employee_id >= len(empl_avail):
            print(f"Invalid employee ID: {employee_id}. Please choose IDs between 0 and {len(empl_avail) - 1}.")
            return

    # Create a figure with three subplots for availability and three for role eligibility
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 10), sharey='row', gridspec_kw={'height_ratios': [3, 0.5]})

    for idx, (gantt_ax, role_ax, employee_id) in enumerate(zip(axes[0], axes[1], employee_ids)):
        availability = empl_avail[employee_id]
        role_eligibility = empl_roles[employee_id]
        gantt_data = []

        # Prepare the data for the Gantt chart for the current employee
        for day_idx, day in enumerate(days):
            for hour in hours:
                if availability[day_idx][hour] == 1:  # Employee is available
                    start_hour = hour
                    end_hour = hour + 1
                    gantt_data.append((day, start_hour, end_hour))

        # Plot the Gantt chart for the current employee
        for day, start, end in gantt_data:
            gantt_ax.barh(day, (end - start), left=start, color=gantt_color, edgecolor='black')

        # Set labels and title for the Gantt chart
        gantt_ax.set_xlabel("Hour of the Day")
        gantt_ax.set_xticks(range(0, 13))
        gantt_ax.set_xticklabels(range(0, 13))
        gantt_ax.set_title(f"Employee {employee_id} Availability and Role Eligibility")
        gantt_ax.invert_yaxis()  # Ensure Monday is at the top and Friday is at the bottom

        # Plot the role eligibility chart for the current employee
        role_x = list(range(len(roles)))
        role_y = [role_eligibility.get(role, 0) for role in roles]
        role_colors_list = [role_colors[role] for role in roles]

        # Adjust bar width and height for role eligibility chart
        bar_width = 0.2  # Reduced bar width
        bar_height = 0.3  # Reduced bar height
        role_ax.bar(role_x, role_y, color=role_colors_list, edgecolor='black', width=bar_width)

        # Customize the X-axis and Y-axis for the role eligibility chart
        role_ax.set_xticks(role_x)
        role_ax.set_xticklabels([role_labels[role] for role in roles], rotation=45, fontweight='bold')
        role_ax.set_ylim(-0.5, 1.5)
        role_ax.set_yticks([0, 1])
        role_ax.set_yticklabels(['Not Eligible', 'Eligible'], fontweight='bold')

        # Only add legend for the last role eligibility chart (rightmost subplot)
        if idx == 2:
            handles = [plt.Line2D([0], [0], color=role_colors[role], linewidth=3) for role in roles]
            labels = [role_labels[role] for role in roles]
            role_ax.legend(handles, labels, title="Roles", loc="upper right")

    # Display the grid for each subplot
    for ax in axes[0]:
        ax.grid(visible=True, color='black', linestyle='--', linewidth=0.7)
    for ax in axes[1]:
        ax.grid(visible=True, color='black', linestyle='--', linewidth=0.7)

    # Adjust layout for better spacing
    plt.tight_layout()
    plt.show()

# Example usage:
gantt_employee_availability_with_roles(1, 4, 9)
