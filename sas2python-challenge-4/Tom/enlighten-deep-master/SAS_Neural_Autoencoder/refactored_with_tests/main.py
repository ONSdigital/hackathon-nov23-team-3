import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPRegressor
from sklearn.metrics.pairwise import pairwise_distances
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
import numpy as np
import os

def load_data(file_path):
    # Load data
    raw_data = pd.read_csv(file_path)

    # Filter columns
    cols_to_keep = [col for col in raw_data.columns if col not in ['provider_id', 'name']]
    filtered_data = raw_data[cols_to_keep]

    return filtered_data
    
def generate_synthetic_data(filtered_data):
    # Separate the features and the target
    features = filtered_data.drop('MAX_university_flag', axis=1)
    target = filtered_data['MAX_university_flag']

    # Generate synthetic data
    smote = SMOTE(random_state=0)
    resampled_features, resampled_target = smote.fit_resample(features, target)

    # Combine the resampled features and target into a new DataFrame
    synthetic_data = pd.concat([pd.DataFrame(resampled_features, columns=features.columns), pd.DataFrame(resampled_target, columns=['MAX_university_flag'])], axis=1)

    return synthetic_data

def perform_clustering(synthetic_data):
    # Standardize numeric inputs for K-means clustering
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(synthetic_data)

    # K-means clustering
    kmeans = KMeans(n_clusters=16, max_iter=100, n_init=10, random_state=44444)
    kmeans.fit(standardized_data)

    # Add cluster labels to the data
    synthetic_data['cluster'] = kmeans.labels_

    return synthetic_data, standardized_data

def train_autoencoder(synthetic_data, standardized_data):
    # Train simple stacked autoencoder with 5 hidden layers
    autoencoder = MLPRegressor(hidden_layer_sizes=(5, synthetic_data.shape[1], synthetic_data.shape[1]//2, 2, synthetic_data.shape[1]//2, synthetic_data.shape[1], 5),
                               max_iter=5000, random_state=44444)
    autoencoder.fit(standardized_data, standardized_data)

    return autoencoder

def hidden_layer_output(model, X):
    layer_output = X
    for i in range(len(model.coefs_) - 1):
        layer_output = np.dot(layer_output, model.coefs_[i]) + model.intercepts_[i]
    return layer_output

def detect_outliers(score2D, num_outliers):
    # Set the median point as the origin of the new 2-D feature space
    origin = np.median(score2D, axis=0)

    # Calculate the distance of each point in new feature space from this origin
    distances = pairwise_distances(score2D, origin.reshape(1, -1))

    # Detect outliers as first 5 points farthest from the origin
    outliers = np.argsort(distances, axis=0)[-num_outliers:]

    return outliers

def plot_data(score2D, df, outliers):
    # Display the data in 2-D including cluster labels and outliers
    plt.scatter(score2D[:, 0], score2D[:, 1], c=df['cluster'])
    plt.scatter(score2D[outliers, 0], score2D[outliers, 1], c='red')
    plt.show()

def main():

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Join the directory with the filename
    file_path = os.path.join(script_dir, 'provider_summary.csv')

    # Set the number of outliers to find (default=5)
    num_outliers = 5

    raw_data = load_data(file_path)
    synthetic_data = generate_synthetic_data(raw_data)
    synthetic_data, standardized_data = perform_clustering(synthetic_data)
    autoencoder = train_autoencoder(synthetic_data, standardized_data)
    score2D = hidden_layer_output(autoencoder, standardized_data)
    outliers = detect_outliers(score2D, num_outliers)
    plot_data(score2D, synthetic_data, outliers)

if __name__ == "__main__":
    main()
