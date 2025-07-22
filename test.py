import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Manually input the data from the heatmap
data = {
    "Role": ["Cook", "Expo", "Front Counter", "Runner", "Dishwasher"],
    "9 AM": [1, 1, 0, 0, 0],
    "10 AM": [1, 1, 1, 1, 1],
    "11 AM": [1, 1, 1, 1, 1],
    "12 PM": [1, 1, 1, 1, 1],
    "1 PM": [1, 1, 1, 1, 1],
    "2 PM": [1, 1, 1, 0, 0],
    "3 PM": [2, 1, 1, 0, 0],
    "4 PM": [2, 1, 1, 1, 1],
    "5 PM": [2, 1, 1, 1, 1],
    "6 PM": [2, 1, 1, 1, 1],
    "7 PM": [2, 1, 1, 1, 1],
    "8 PM": [2, 1, 1, 1, 1],
}

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(data)
df.set_index("Role", inplace=True)

# Define a custom colormap to match the colors in the image
colors = ["white", "orange", "skyblue"]
n_bins = 3  # Number of unique levels in the data (0, 1, 2)
cmap = LinearSegmentedColormap.from_list("custom_cmap", colors, N=n_bins)

# Plot the heatmap
plt.figure(figsize=(10, 6))
ax = sns.heatmap(
    df, 
    annot=True, 
    fmt="d", 
    cmap=cmap, 
    cbar=True, 
    linewidths=0.5, 
    linecolor='black'
)

# Add border lines around the x and y axis
ax.spines['top'].set_visible(True)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.spines['top'].set_color('black')
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['right'].set_color('black')
ax.spines['top'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.spines['left'].set_linewidth(1.5)
ax.spines['right'].set_linewidth(1.5)

# Set title and labels
plt.title("Monday Role Requirements Heatmap")
plt.xlabel("Time")
plt.ylabel("Role")
plt.tight_layout()
plt.show()
