import matplotlib.pyplot as plt
import numpy as np

# Data arrays
x_labels = ['70', '75', '80', '85', '90']
apriori = [9.99, 7.16 , 5.66 , 4.31, 2.94]
fp_growth = [14.15, 8.45, 6.11, 4.23, 3.33]

x = np.arange(len(x_labels))     # label locations
width = 0.35                     # width of the bars

fig, ax = plt.subplots(figsize=(8,5))
bars1 = ax.bar(x - width/2, apriori, width, label='Apriori')
bars2 = ax.bar(x + width/2, fp_growth, width, label='FP-Growth', color='orange')

# Add values on the bars
for bar in bars1:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.2, f'{yval:.2f}', ha='center', va='bottom', fontsize=8)
for bar in bars2:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.2, f'{yval:.2f}', ha='center', va='bottom', fontsize=8)

# Chart formatting
ax.set_ylabel('Memory Usage (MB)')
ax.set_xlabel('Min Support (%)')
ax.set_title('Memory Usage Comparison')
ax.set_xticks(x)
ax.set_xticklabels(x_labels)
ax.legend()

plt.tight_layout()

# Save the figure
plt.savefig('chess_memory.png', dpi=300)  # You can change filename/format/dpi as needed

plt.show()