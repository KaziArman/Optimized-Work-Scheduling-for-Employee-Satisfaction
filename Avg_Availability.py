import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import employeedata as ed

# Load employee availability data
empl_avail = ed.empl_avail
employee_ids = list(range(len(empl_avail)))  # Employee IDs (0 to 13)
time_labels = ['9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM']

def plot_avg_availability_heatmap():
    # Compute the average availability across the week for each employee at each hour
    avg_availability_matrix = np.mean(empl_avail, axis=1)

    # Create the heatmap
    plt.figure(figsize=(14, 8))
    sns.heatmap(avg_availability_matrix, cmap='Blues', cbar=True, linewidths=0.5, linecolor='black', annot=True, fmt='.2f')

    # Set labels and title
    plt.xlabel("Time of the Day", fontsize=14)
    plt.ylabel("Employee ID", fontsize=14)
    plt.title("Average Employee Availability by Hour (Monday to Friday)", fontsize=16, fontweight='bold')
    plt.xticks(ticks=range(12), labels=time_labels, rotation=45, ha='right')
    plt.yticks(ticks=range(len(employee_ids)), labels=employee_ids)

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.show()

# Example usage:
plot_avg_availability_heatmap()
