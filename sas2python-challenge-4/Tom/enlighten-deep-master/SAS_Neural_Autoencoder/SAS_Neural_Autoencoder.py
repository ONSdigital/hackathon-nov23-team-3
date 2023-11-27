import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPRegressor
from sklearn.metrics.pairwise import pairwise_distances
import matplotlib.pyplot as plt
from sas7bdat import SAS7BDAT
import numpy as np

def hidden_layer_output(model, X):
    layer_output = X
    for i in range(len(model.coefs_) - 1):
        layer_output = np.maximum(0, np.dot(layer_output, model.coefs_[i]) + model.intercepts_[i])
    return layer_output

# Set GitHub data directory (must contain provider_summary.sas7bdat)
git_repo_dir = "D:\GitHub\hackathon-nov23-team-3\sas2python-challenge-4\Tom\enlighten-deep-master\SAS_Neural_Autoencoder"  # Set your directory path

# Set number of available cores
num_cores = 1  # fill this with your number of cores

# Set the number of outliers to find (default=5)
num_outliers = 5

# Load data
with SAS7BDAT(f'{git_repo_dir}\provider_summary.sas7bdat') as file:
    provider_summary = file.to_data_frame()

# Filter columns
cols_to_keep = [col for col in provider_summary.columns if col not in ['provider_id', 'name']]
provider_summary = provider_summary[cols_to_keep]

# Standardize numeric inputs for K-means clustering
scaler = StandardScaler()
std_provider_summary = scaler.fit_transform(provider_summary)

# K-means clustering
kmeans = KMeans(n_clusters=16, max_iter=100, n_init=10, random_state=44444)
kmeans.fit(std_provider_summary)

# Add cluster labels to the data
provider_summary['cluster'] = kmeans.labels_

# Train simple stacked autoencoder with 5 hidden layers
autoencoder = MLPRegressor(hidden_layer_sizes=(5, provider_summary.shape[1], provider_summary.shape[1]//2, 2, provider_summary.shape[1]//2, provider_summary.shape[1], 5),
                           max_iter=5000, random_state=44444)
autoencoder.fit(std_provider_summary, std_provider_summary)

# Score training data with trained neural network
score2D = hidden_layer_output(autoencoder, std_provider_summary)

# Set the median point as the origin of the new 2-D feature space
origin = np.median(score2D, axis=0)

# Calculate the distance of each point in new feature space from this origin
distances = pairwise_distances(score2D, origin.reshape(1, -1))

# Detect outliers as first 5 points farthest from the origin
outliers = np.argsort(distances, axis=0)[-num_outliers:]

# Display the data in 2-D including cluster labels and outliers
plt.scatter(score2D[:, 0], score2D[:, 1], c=provider_summary['cluster'])
plt.scatter(score2D[outliers, 0], score2D[outliers, 1], c='red')
plt.show()