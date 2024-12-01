import numpy as np
import math
import tensorflow
from tensorflow.keras.models import load_model
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('sensor_values.csv')


X = df[['x_value', 'y_value', 'z_value']].values  
y = df['pos_value'].values  


model = load_model('model_synthetic_trained_with_noise.h5')


weights = model.get_weights()


def flatten(data):
    return np.array(data).flatten()

def relu(data):
    return np.maximum(0, data)

def normalize_single_point(input_point):
    means = [np.mean(X[:, i]) for i in range(X.shape[1])]
    stds = [np.std(X[:, i]) for i in range(X.shape[1])]
    return np.array([(input_point[i] - means[i]) / stds[i] for i in range(len(input_point))])

def dense_layer(input, weight, bias, activation=None):
    output = np.zeros(bias.shape)
    for i in range(bias.shape[0]):
        output[i] = bias[i]
        for j in range(weight.shape[0]):
            output[i] += input[j] * weight[j, i]
    if activation:
        output = activation(output)
    return output

def pass_through(input_data):
    input_data = flatten(input_data)
    weight1, bias1 = weights[0], weights[1]  
    output1 = dense_layer(input_data, weight1, bias1, activation=relu)
    
    weight2, bias2 = weights[2], weights[3]  
    output2 = dense_layer(output1, weight2, bias2, activation=relu)
    
    weight3, bias3 = weights[4], weights[5]  
    output3 = dense_layer(output2, weight3, bias3, activation=None)
    
    return output3

def normalize_predictions(predictions):
    """Normalize predictions to get probabilities."""
    exp_values = np.exp(predictions - np.max(predictions))  
    return exp_values / np.sum(exp_values)


input_point = np.array([1303.0,1629.0,1674.0])  


normalized_input = normalize_single_point(input_point)


keras_prediction = flatten(model.predict(normalized_input.reshape(1, -1)))  


custom_prediction = flatten(pass_through(normalized_input))


custom_prediction_normalized = normalize_predictions(custom_prediction)


print(f"Input point: {input_point}")
print(f"Keras Model Prediction (for positions 0-5): {keras_prediction}")
print(f"Custom Model Prediction (for positions 0-5): {custom_prediction_normalized}")


positions = np.array([0, 1, 2, 3, 4, 5])

# Create the bar plot
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
with open('model_weights.h', 'w') as f:
    f.write('#include <stdio.h>\n\n')
    
    # Iterate through weights and biases
    for i, (weight, bias) in enumerate(zip(weights[::2], weights[1::2])):  # Weights and biases alternate
        weight_array = np.array(weight)
        bias_array = np.array(bias)
        
        # Define array sizes
        f.write(f'// Layer {i + 1} Weights and Biases\n')
        
        # Write weight array to file
        f.write(f'float layer_{i + 1}_weights[] = {{')
        f.write(', '.join(map(str, weight_array.flatten())))
        f.write('};\n')
        
        # Write bias array to file
        f.write(f'float layer_{i + 1}_biases[] = {{')
        f.write(', '.join(map(str, bias_array.flatten())))
        f.write('};\n\n')
        
    print("Weights and biases saved to model_weights.h")