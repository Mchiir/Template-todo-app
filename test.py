import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd  # Import pandas

# Generate some random data
num_points = 20
x = 5 + np.arange(num_points) + np.random.randn(num_points)
y = 10 + np.arange(num_points) + 5 * np.random.randn(num_points)

# Create a DataFrame
data = pd.DataFrame({'x': x, 'y': y})

# Use regplot with the DataFrame
sns.regplot(data=data, x='x', y='y')
plt.show()