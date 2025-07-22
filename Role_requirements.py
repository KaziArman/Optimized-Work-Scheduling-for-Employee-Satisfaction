import matplotlib.pyplot as plt
import staffingdata as sd

# Define the function to create the horizontal bar chart for role requirements
def role_requirements_horizontal_chart(day="all"):
    role_reqs = sd.role_reqs  # Role requirements from staffingdata
    day_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    role_labels = {'C': 'Cook', 'E': 'Expo', 'F': 'Front Counter', 'R': 'Runner', 'D': 'Dishwasher'}
    role_colors = {'C': 'skyblue', 'E': 'orange', 'F': 'green', 'R': 'purple', 'D': 'yellow'}

    # Case 1: "all" - Show the role requirements for all days in the week
    if day.lower() == "all":
        y_labels = []
        counts = []
        colors = []
        day_dividers = []  # To store the positions for segmenting the chart

        # Iterate over each day and role
        y_pos = 0
        for day_idx, day_name in enumerate(day_labels):
            # Add a divider position before starting a new day
            if y_pos > 0:
                day_dividers.append(y_pos - 0.5)

            # Add the day label (bold text)
            y_labels.append(f"{day_name}")
            counts.append(0)  # Placeholder for the day label (no bar)
            colors.append('white')  # Invisible bar for the day label

            # Add role-specific bars for the current day
            for role, label in role_labels.items():
                total_count = sum(role_reqs[role][day_idx])  # Sum of the requirements across all hours
                y_labels.append(f"  {label}")  # Indent the role labels
                counts.append(total_count)
                colors.append(role_colors[role])
                y_pos += 1

            y_pos += 1  # Increment for the day label

        # Create the horizontal bar chart
        fig, ax = plt.subplots(figsize=(14, 10))
        y_positions = range(len(y_labels))

        # Plot the horizontal bars
        bars = ax.barh(y_positions, counts, color=colors, edgecolor='black')

        # Set labels and title
        ax.set_yticks(y_positions)
        ax.set_yticklabels(y_labels, fontweight='bold')
        ax.invert_yaxis()  # Ensure Monday is at the top and Friday is at the bottom
        ax.set_xlabel("Count of Role Requirements", fontsize=14)
        ax.set_title("Role Requirements for the Restaurant (Monday to Friday)", fontsize=16, fontweight='bold')

        # Add the count values on the bars
        for bar, count in zip(bars, counts):
            if count > 0:  # Only display text for non-placeholder bars
                ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                        f"{count}", va='center', ha='left', fontweight='bold', fontsize=12)

        # Add segment dividers for each day
        for divider in day_dividers:
            ax.axhline(y=divider, color='black', linewidth=1.5)

        # Add a legend for the roles
        handles = [plt.Line2D([0], [0], color=color, linewidth=3) for color in role_colors.values()]
        labels = [role_labels[role] for role in role_colors.keys()]
        ax.legend(handles, labels, title="Role", loc="upper right")

        # Adjust layout and show the plot
        plt.tight_layout()
        plt.show()

    # Case 2: Single Day - Show the role requirements for the specified day
    elif day.capitalize() in day_labels:
        day_idx = day_labels.index(day.capitalize())

        # Prepare the data for the single day chart
        y_labels = list(role_labels.values())  # Role names for the Y-axis
        counts = []
        colors = []

        # Accumulate the count of required roles for the selected day
        for role, label in role_labels.items():
            total_count = sum(role_reqs[role][day_idx])  # Sum of the requirements across all hours
            counts.append(total_count)
            colors.append(role_colors[role])

        # Create the horizontal bar chart
        fig, ax = plt.subplots(figsize=(12, 8))
        y_positions = range(len(y_labels))

        # Plot the horizontal bars
        bars = ax.barh(y_positions, counts, color=colors, edgecolor='black')

        # Set labels and title
        ax.set_yticks(y_positions)
        ax.set_yticklabels(y_labels, fontweight='bold')
        ax.invert_yaxis()  # Ensure the first role (Cook) is at the top
        ax.set_xlabel("Count of Role Requirements", fontsize=14)
        ax.set_title(f"Role Requirements for the Restaurant on {day.capitalize()}", fontsize=16, fontweight='bold')

        # Add the count values on the bars
        for bar, count in zip(bars, counts):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                    f"{count}", va='center', ha='left', fontweight='bold', fontsize=12)

        # Add a legend for the roles
        handles = [plt.Line2D([0], [0], color=color, linewidth=3) for color in role_colors.values()]
        labels = [role_labels[role] for role in role_colors.keys()]
        ax.legend(handles, labels, title="Role", loc="upper right")

        # Adjust layout and show the plot
        plt.tight_layout()
        plt.show()

    # Invalid input case
    else:
        print("Invalid day input. Please choose 'all', or one of: Monday, Tuesday, Wednesday, Thursday, Friday.")

# Example usage:
#role_requirements_horizontal_chart("all")  # Shows the entire week
role_requirements_horizontal_chart("Monday")  # Shows role requirements for Monday
