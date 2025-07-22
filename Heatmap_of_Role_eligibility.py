# Simplifying and retrying the heatmap generation
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import employeedata as ed

# Load the employee role eligibility data
empl_roles = ed.empl_roles
roles = ['C', 'E', 'F', 'R', 'D']
role_labels = ['Cook', 'Expo', 'Front Counter', 'Runner', 'Dishwasher']
employee_ids = [f"Emp {i}" for i in range(len(empl_roles))]

# Prepare the data for the heatmap
heatmap_data = [[empl_roles[i][role] for role in roles] for i in range(len(empl_roles))]

# Convert the data into a DataFrame
df = pd.DataFrame(heatmap_data, index=employee_ids, columns=role_labels)

# Create a heatmap
plt.figure(figsize=(14, 8))
sns.heatmap(df, cmap="RdYlGn", annot=True, linewidths=0.5, linecolor='black', cbar=True)

# Set labels and title
plt.xlabel("Roles", fontsize=14)
plt.ylabel("Employees", fontsize=14)
plt.title("Employee Role Eligibility Heatmap", fontsize=16, fontweight='bold')

# Display the heatmap
plt.tight_layout()
plt.show()
