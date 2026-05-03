import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from . import utils
from scipy.optimize import curve_fit

# Create some dummy data
x = np.linspace(0, 10, 100)
y1 = 2 * x + 1      # First line
y2 = 5 * x - 20     # Second line

# Create a figure with 1 row and 2 columns
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Plot on the first axis (left)
ax1.plot(x, y1, color='blue')
ax1.set_title('First Segment Slope')
ax1.grid(True)

# Plot on the second axis (right)
ax2.plot(x, y2, color='red')
ax2.set_title('Second Segment Slope')
ax2.grid(True)

plt.tight_layout() # Adjusts spacing so labels don't overlap
plt.show()