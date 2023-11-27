import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPRegressor
from sklearn.metrics.pairwise import euclidean_distances
import matplotlib.pyplot as plt
import numpy as np

# Define the necessary variables
git_repo_dir = "D:\src-code\Hackthon\hackathon-nov23-team-3\sas2python-challenge-4\Tom\enlighten-deep-master\SAS_Neural_Autoencoder"  # Set your directory path
num_cores = 1  # Set the number of cores
num_outliers = 5  # Set the number of outliers to find


# Load the data from a .sas7bdat file
provider_summary = pd.read_sas(git_repo_dir + '\provider_summary.sas7bdat')

# Get the column names
column_names = provider_summary.columns.tolist()

# Filter out 'provider_id' and 'name'
name = [name for name in column_names if name not in ['provider_id', 'name']]
print(name)
# Now filtered_names contains the names of the columns in provider_summary, excluding 'provider_id' and 'name'


# # Load the data
# provider_summary = pd.read_sas(git_repo_dir + "/provider_summary.sas7bdat")

# # Filter the data to get the numeric inputs
numeric_inputs = provider_summary.select_dtypes(include=['float64', 'int64']).drop(columns=['provider_id', 'name'])

# Standardize the numeric inputs for K-means clustering
scaler = StandardScaler()
numeric_inputs_scaled = scaler.fit_transform(numeric_inputs)

# K-means clustering
kmeans = KMeans(n_clusters=16, random_state=0, n_jobs=num_cores).fit(numeric_inputs_scaled)

# Train simple stacked autoencoder with 5 hidden layers
mlp = MLPRegressor(hidden_layer_sizes=(numeric_inputs.shape[1], numeric_inputs.shape[1]//2, 2, numeric_inputs.shape[1]//2, numeric_inputs.shape[1]), random_state=0)
mlp.fit(numeric_inputs_scaled, numeric_inputs_scaled)

# Score training data with trained neural network
score2D = mlp.predict(numeric_inputs_scaled)

# Keep output of 2-dimensional middle layer as new feature space
middle_layer_output = mlp.hidden_layer_sizes[2]

# Set the median point as the origin of the new 2-D feature space
origin = np.median(middle_layer_output, axis=0)

# Calculate the distance of each point in new feature space from this origin
distances = euclidean_distances(middle_layer_output, origin.reshape(1, -1))

# Detect outliers as first 5 points farthest from the origin
outliers = distances.argsort()[-num_outliers:]

# Display the data in 2-D including cluster labels and outliers
plt.scatter(middle_layer_output[:, 0], middle_layer_output[:, 1], c=kmeans.labels_)
plt.scatter(middle_layer_output[outliers, 0], middle_layer_output[outliers, 1], c='red')
plt.show()