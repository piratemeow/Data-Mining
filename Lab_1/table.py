import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table

# Data for the table
data = {
    'Min sup': [2.0, 3.0, 5.0, 8.0, 10.0, 20.0],
    'Apriori_Runtime (s)': [15.03, 6.18, 1.67, 1.35, 0.87, 0.14],
    'Apriori_Memory (MB)': [0.02, 0.53, 0.67, 0.02, 0.43, 0.65],
    'Apriori_Frequent Items': [55, 32, 16, 13, 9, 3],
    'FP-Growth_Runtime (s)': [0.36, 0.31, 0.28, 0.29, 0.28, 0.22],
    'FP-Growth_Memory (MB)': [0.94, 1.36, 0.96, 0.25, 0.16, 0.26],
    'FP-Growth_Frequent Items': [55, 32, 16, 13, 9, 3]
}

# Create a Pandas DataFrame
df = pd.DataFrame(data)

# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 4))  # Adjust figure width as needed
ax.axis('off')

# Create the table
table_obj = table(ax, df, loc='center', cellLoc='center')

# Set font size
table_obj.auto_set_font_size(False)
table_obj.set_fontsize(10)

# Adjust column widths manually
col_widths = [0.1, 0.15, 0.15, 0.2, 0.15, 0.15, 0.2]  # Adjust these values
for k, col in enumerate(df.columns):
    cells = [cell for cell in table_obj._cells if cell[0] == 0 and cell[1] == k]  # Header cells
    for cell in cells:
        table_obj._cells[cell].set_width(col_widths[k])
    for i in range(len(df)):
        cell = (i + 1, k)  # Data cells
        if cell in table_obj._cells:
            table_obj._cells[cell].set_width(col_widths[k])

# Add a title
ax.set_title('(c) Comparison Table', y=-0.2)

# Save the figure
plt.savefig('comparison_table_v3.png', bbox_inches='tight')

# Optionally display the table
plt.show()