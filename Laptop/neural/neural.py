import numpy as np
import math
import tensorflow
from tensorflow.keras.models import load_model
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('sensor_values.csv')


X = df[['x_value', 'y_value', 'z_value']].values  
y = df['pos_value'].values  


model = load_model('model_synthetic_trained_with_noise_one_layer.h5')


weights = model.get_weights()


def flatten(data):
    return np.array(data).flatten()


def relu(data):
    return np.maximum(0, data)


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
    output1 = dense_layer(input_data, weight1, bias1, activation=None)  
    
    return output1


input_point = np.array([1626.0, 1629.0, 1974.0])  


keras_prediction = flatten(model.predict(input_point.reshape(1, -1)))  


custom_prediction = flatten(pass_through(input_point))

def normalize_predictions(predictions):
    """Normalize predictions to get probabilities."""
    exp_values = np.exp(predictions - np.max(predictions))  
    return exp_values / np.sum(exp_values)


custom_prediction_normalized = normalize_predictions(custom_prediction)


print(f"Input point: {input_point}")
print(f"Keras Model Prediction (for positions 0-5): {keras_prediction}")
print(f"Custom Model Prediction (for positions 0-5): {custom_prediction_normalized}")


positions = np.array([0, 1, 2, 3, 4, 5])


fig, ax = plt.subplots(figsize=(12, 6))


ax.bar(positions - 0.2, keras_prediction, width=0.4, label='Keras Model', color='blue', align='center')


ax.bar(positions + 0.2, custom_prediction_normalized, width=0.4, label='Custom Model', color='green', align='center')


ax.set_xlabel('Position')
ax.set_ylabel('Prediction Likelihood')
ax.set_title(f'Predictions for Input Point: {input_point}')
ax.legend()


plt.tight_layout()
plt.show()


with open('model_weights_and_stats.h', 'w') as f:
    f.write('#include <stdio.h>\n\n')
    
    
    weight_array = np.array(weights[0])
    bias_array = np.array(weights[1])
    
    f.write(f'// Weights and Biases for the One-Layer Model\n')
    

    f.write(f'float layer_1_weights[] = {{')
    f.write(', '.join(map(str, weight_array.flatten())))
    f.write('};\n')
    
  
    f.write(f'float layer_1_biases[] = {{')
    f.write(', '.join(map(str, bias_array.flatten())))
    f.write('};\n\n')

    print("Weights, biases saved to model_weights_and_stats.h")
