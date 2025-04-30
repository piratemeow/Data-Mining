import matplotlib.pyplot as plt
import numpy as np

# Data arrays
x_labels = [70, 75, 80, 85, 90]
apriori = [134.10, 47.86, 15.33, 3.42, 0.61]
fp_growth = [32.15, 14.68,  6.03, 1.81, 0.47]

fig, ax = plt.subplots(figsize=(9, 6))

# Plot lines with markers
line1, = ax.plot(x_labels, apriori, '-o', label='Apriori')
line2, = ax.plot(x_labels, fp_growth, '-o', label='FP-Growth', color='orange')

# Annotate points
for i, val in enumerate(apriori):
    ax.annotate(f'{val:.2f}', (x_labels[i], apriori[i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8)
for i, val in enumerate(fp_growth):
    ax.annotate(f'{val:.2f}', (x_labels[i], fp_growth[i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8)

# Chart formatting
ax.set_ylabel('Execution Time (seconds)')
ax.set_xlabel('Min Support (%)')
ax.set_title('Execution Time vs Min Support')
ax.legend()

plt.tight_layout()
plt.savefig('execution_time_chess.png', dpi=300)  # Save image
plt.show()