import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPRegressor
from sklearn.metrics.pairwise import pairwise_distances
import matplotlib.pyplot as plt
from sas7bdat import SAS7BDAT
import numpy as np
import os
from imblearn.over_sampling import SMOTE

def hidden_layer_output(model, X):
    layer_output = X
    for i in range(len(model.coefs_) - 1):
        layer_output = np.dot(layer_output, model.coefs_[i]) + model.intercepts_[i]
    return layer_output

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Join the directory with the filename
file_path = os.path.join(script_dir, 'provider_summary.csv')

# Set number of available cores
num_cores = 1  # fill this with your number of cores

# Set the number of outliers to find (default=5)
num_outliers = 5

# Load data
#with SAS7BDAT(file_path) as file:
#    provider_summary = file.to_data_frame()
provider_summary = pd.read_csv(file_path)

# Filter columns
cols_to_keep = [col for col in provider_summary.columns if col not in ['provider_id', 'name']]
provider_summary = provider_summary[cols_to_keep]

# Separate the features and the target
# Assuming 'MAX_university_flag' is the target column
X = provider_summary.drop('MAX_university_flag', axis=1)
y = provider_summary['MAX_university_flag']

# Initialize a SMOTE object
smote = SMOTE(random_state=0)

# Generate synthetic data
X_resampled, y_resampled = smote.fit_resample(X, y)

# Combine the resampled features and target into a new DataFrame
synthetic_df = pd.concat([pd.DataFrame(X_resampled, columns=X.columns), pd.DataFrame(y_resampled, columns=['MAX_university_flag'])], axis=1)
provider_summary = synthetic_df

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