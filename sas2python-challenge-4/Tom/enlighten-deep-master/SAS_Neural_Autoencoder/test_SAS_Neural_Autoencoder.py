import numpy as np
from SAS_Neural_Autoencoder import hidden_layer_output

# Test case 1: Simple 2-layer model
model = {
    'coefs_': [np.array([[1, 2], [3, 4]]), np.array([[5], [6]])],
    'intercepts_': [np.array([1, 2]), np.array([3])]
}
X = np.array([[1, 2]])
expected_output = np.array([[35]])
assert np.array_equal(hidden_layer_output(model, X), expected_output)

# Test case 2: 3-layer model
model = {
    'coefs_': [np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]]), np.array([[9], [10]])],
    'intercepts_': [np.array([1, 2]), np.array([3, 4]), np.array([5])]
}
X = np.array([[1, 2]])
expected_output = np.array([[537]])
assert np.array_equal(hidden_layer_output(model, X), expected_output)

# Test case 3: Empty input
model = {
    'coefs_': [],
    'intercepts_': []
}
X = np.array([])
expected_output = np.array([])
assert np.array_equal(hidden_layer_output(model, X), expected_output)

# Test case 4: Random input
model = {
    'coefs_': [np.array([[1, 2, 3], [4, 5, 6]]), np.array([[7], [8], [9]])],
    'intercepts_': [np.array([1, 2]), np.array([3])]
}
X = np.array([[1, 2, 3]])
expected_output = np.array([[228]])
assert np.array_equal(hidden_layer_output(model, X), expected_output)

print("All test cases passed!")