import matplotlib.pyplot as plt
import numpy as np

# Create figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define coordinates for apple and peach images
# Apple positioned in XZ plane (y=0), Peach positioned in YZ plane (x=0)
apple_x = np.linspace(-5, 5, 100)
apple_z = np.linspace(-5, 5, 100)
peach_y = np.linspace(-5, 5, 100)
peach_z = np.linspace(-5, 5, 100)

# Plot apple in XZ plane
ax.scatter(apple_x, np.zeros_like(apple_x), apple_z, c='r', label='Apple')

# Plot peach in YZ plane
ax.scatter(np.zeros_like(peach_y), peach_y, peach_z, c='orange', label='Peach')

# Set labels and legend
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()

# Show plot
plt.show()