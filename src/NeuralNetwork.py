import numpy as np
import json

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

class NeuralNetwork:
    def __init__(self, layers_sizes):
        self.layers_sizes = layers_sizes
        self.num_layers = len(layers_sizes)
        self.weights = [np.random.uniform(-1, 1, (layers_sizes[i+1], layers_sizes[i])) for i in range(self.num_layers - 1)]
        self.biases = [np.random.uniform(-1, 1, (size, 1)) for size in layers_sizes[1:]]
        self.activations = [np.zeros((size, 1)) for size in layers_sizes]
        self.learning_rate = 0.01

    def feed_forward(self, inputs):
        self.activations[0] = inputs.reshape((len(inputs), 1))

        for i in range(self.num_layers - 1):
            weighted_sum = np.dot(self.weights[i], self.activations[i]) + self.biases[i]
            clipped_weighted_sum = np.clip(weighted_sum, -500, 500)
            self.activations[i + 1] = sigmoid(clipped_weighted_sum)

        return self.activations[-1]

    def train(self, inputs, expected_output):
        # Perform feedforward to compute activations
        self.feed_forward(inputs)

        # Compute the error at the output layer
        output_error = expected_output - self.activations[-1]

        # Backpropagation
        for i in reversed(range(self.num_layers - 1)):
            # Compute the gradient at the current layer
            gradient = sigmoid_derivative(self.activations[i + 1]) * output_error
            gradient *= self.learning_rate

            # Update weights and biases
            self.weights[i] += np.dot(gradient, self.activations[i].T)
            self.biases[i] += gradient

            # Propagate the error to the previous layer
            output_error = np.dot(self.weights[i].T, output_error)

    def cost(self, inputs, expected_output):
        predictions = self.feed_forward(inputs)
        return np.sum((expected_output - predictions) ** 2)

    def predict(self, inputs):
        return self.feed_forward(inputs)

    def save(self, filename):
        data = {
            'weights': [arr.tolist() for arr in self.weights],
            'biases': [arr.tolist() for arr in self.biases],
            'layer_sizes': self.layers_sizes
        }
        with open(filename, 'w') as file:
            json.dump(data, file)

    def load(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        layers_sizes = [arr for arr in data["layer_sizes"]]
        self.__init__(layers_sizes)
        self.weights = [np.array(data_list) for data_list in data['weights']]
        self.biases = [np.array(data_list) for data_list in data['biases']]
