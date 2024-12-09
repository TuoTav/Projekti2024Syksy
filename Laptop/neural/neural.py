import numpy as np
import math
import tensorflow
from tensorflow.keras.models import load_model
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('sensor_values.csv')

# Extract the feature columns (raw sensor values) and labels
X = df[['x_value', 'y_value', 'z_value']].values  
y = df['pos_value'].values  

# Load the pre-trained Keras model
model = load_model('model_synthetic_trained_with_noise_one_layer.h5')

# Get the weights from the Keras model
weights = model.get_weights()

# Function to flatten the data
def flatten(data):
    return np.array(data).flatten()

# ReLU activation function
def relu(data):
    return np.maximum(0, data)

# Function for the dense layer (custom implementation)
def dense_layer(input, weight, bias, activation=None):
    output = np.zeros(bias.shape)
    for i in range(bias.shape[0]):
        output[i] = bias[i]
        for j in range(weight.shape[0]):
            output[i] += input[j] * weight[j, i]
    if activation:
        output = activation(output)
    return output

# Pass-through function for the custom model
def pass_through(input_data):
    input_data = flatten(input_data)
    
    # For the one-layer model, there's only one weight and bias pair
    weight1, bias1 = weights[0], weights[1]  
    output1 = dense_layer(input_data, weight1, bias1, activation=None)  # No activation since it's the output layer
    
    return output1

# Raw input point (no normalization)
input_point = np.array([1626.0, 1629.0, 1974.0])  

# Predict using the Keras model (raw input point)
keras_prediction = flatten(model.predict(input_point.reshape(1, -1)))  

# Predict using the custom model (raw input point)
custom_prediction = flatten(pass_through(input_point))

# Normalize the predictions to get probabilities
def normalize_predictions(predictions):
    """Normalize predictions to get probabilities."""
    exp_values = np.exp(predictions - np.max(predictions))  
    return exp_values / np.sum(exp_values)

# Normalize the predictions for comparison
custom_prediction_normalized = normalize_predictions(custom_prediction)

# Print predictions
print(f"Input point: {input_point}")
print(f"Keras Model Prediction (for positions 0-5): {keras_prediction}")
print(f"Custom Model Prediction (for positions 0-5): {custom_prediction_normalized}")

# Define the positions (assuming 6 output classes)
positions = np.array([0, 1, 2, 3, 4, 5])

# Create a bar plot for the predictions
fig, ax = plt.subplots(figsize=(12, 6))

# Bar plot for Keras model predictions
ax.bar(positions - 0.2, keras_prediction, width=0.4, label='Keras Model', color='blue', align='center')

# Bar plot for Custom model predictions (after normalization)
ax.bar(positions + 0.2, custom_prediction_normalized, width=0.4, label='Custom Model', color='green', align='center')

# Labels and title
ax.set_xlabel('Position')
ax.set_ylabel('Prediction Likelihood')
ax.set_title(f'Predictions for Input Point: {input_point}')
ax.legend()

# Show the plot
plt.tight_layout()
plt.show()

# Save weights, biases, means, and stds to a header file (if needed for C implementation)
with open('model_weights_and_stats.h', 'w') as f:
    f.write('#include <stdio.h>\n\n')
    
    # Write the single weight and bias pair (since it's a one-layer model)
    weight_array = np.array(weights[0])
    bias_array = np.array(weights[1])
    
    f.write(f'// Weights and Biases for the One-Layer Model\n')
    
    # Write weight array to file
    f.write(f'float layer_1_weights[] = {{')
    f.write(', '.join(map(str, weight_array.flatten())))
    f.write('};\n')
    
    # Write bias array to file
    f.write(f'float layer_1_biases[] = {{')
    f.write(', '.join(map(str, bias_array.flatten())))
    f.write('};\n\n')

    print("Weights, biases saved to model_weights_and_stats.h")