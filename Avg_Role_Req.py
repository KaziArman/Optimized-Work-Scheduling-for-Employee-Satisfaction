import matplotlib.pyplot as plt
import staffingdata as sd
import numpy as np

# Role requirements data from staffingdata.py
role_reqs = sd.role_reqs  # Dictionary with keys as role codes ('C', 'E', 'F', 'R', 'D')
roles = ['C', 'E', 'F', 'R', 'D']
role_labels = {'C': 'Cook', 'E': 'Expo', 'F': 'Front Counter', 'R': 'Runner', 'D': 'Dishwasher'}
role_colors = {'C': 'skyblue', 'E': 'orange', 'F': 'green', 'R': 'purple', 'D': 'yellow'}

# Initialize arrays for each role's requirement per hour (averaged over all days)
hours = list(range(12))  # From hour 0 to hour 11
time_labels = ['9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM']
role_counts_avg = {role: np.zeros(len(hours)) for role in roles}

# Calculate average role requirements for each hour of the day across all weekdays
for role in roles:
    for hour in hours:
        # Calculate the average by dividing the sum by the number of days (5 weekdays)
        role_counts_avg[role][hour] = sum(role_reqs[role][day][hour] for day in range(5)) / 5

# Create the stacked bar chart
fig, ax = plt.subplots(figsize=(14, 8))
bottom = np.zeros(len(hours))  # Initialize the bottom array for stacking

# Plot each role's requirements as a stacked bar
for role in roles:
    ax.bar(hours, role_counts_avg[role], bottom=bottom, color=role_colors[role], label=role_labels[role], edgecolor='black')
    bottom += role_counts_avg[role]  # Update the bottom for the next stack

# Set labels and title
ax.set_xlabel("Time of the Day", fontsize=14)
ax.set_ylabel("Average Number of Employees Required", fontsize=14)
ax.set_title("Average Role Requirements by Hour (Across the Week)", fontsize=16, fontweight='bold')
ax.set_xticks(hours)
ax.set_xticklabels(time_labels, rotation=45, ha='right', fontsize=12)
ax.legend(title="Roles", loc="upper right")

# Display the grid and the plot
ax.grid(visible=True, color='grey', linestyle='--', linewidth=0.7)
plt.tight_layout()
plt.show()
