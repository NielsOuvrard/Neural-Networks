import sys
import pandas as pd
import numpy as np
import ast
import json


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)


class PerceptronArguments:
    def __init__(self):
        self.new_perceptron = False
        self.load_perceptron = False
        self.save_perceptron = False
        self.mode = ""
        self.nb_inputs = 0
        self.load_file = ""
        self.save_file = ""
        self.input_file = ""

def handle_perceptron_arguments(argv, args):
    x = 1
    if len(argv) == 1:
        print_perceptron_usage()
        return 84
    if argv[1] == "--help" or argv[1] == "-h":
        print_perceptron_usage()
        return 0
    while x < len(argv):
        if argv[x][0] != '-':
            # Non-option argument (FILE)
            args.input_file = argv[x]
            break

        option = argv[x][2]
        if option == 'n':
            args.new_perceptron = True
            x += 1  # move to the next argument
            args.nb_inputs = int(argv[x])
        elif option == 'l':
            args.load_perceptron = True
            x += 1
            args.load_file = argv[x]
        elif option == 's':
            args.save_perceptron = True
            x += 1
            args.save_file = argv[x]
        elif option == 'm':
            x += 1
            args.mode = argv[x]
            if args.mode not in ["train", "predict"]:
                print("Invalid mode. Use 'train' or 'predict'.")
                return 84
        else:
            print("Invalid option. Use --help for help.")
            return 84

        x += 1

    # Validate if mandatory arguments are provided
    if not (args.new_perceptron or args.load_perceptron):
        print("Either --new or --load must be specified. Use --help for help.")
        return 84

    if not args.mode:
        print("--mode must be specified. Use --help for help.")
        return 84

    return 0

def print_perceptron_arguments(args):
    print("Input File:", args.input_file)

    if args.new_perceptron:
        print("New Perceptron with", args.nb_inputs, "inputs.")

    if args.load_perceptron:
        print("Load Perceptron from:", args.load_file)

    print("Mode:", args.mode)

    if args.save_perceptron:
        print("Save Perceptron state into:", args.save_file)

def print_perceptron_usage():
    print("USAGE")
    print("\t./my_perceptron [--new NB_INPUTS | --load LOADFILE] [--save SAVEFILE] --mode [train | predict] FILE")
    print("DESCRIPTION")
    print("\t--new Creates a new perceptron with NB_INPUTS inputs.")
    print("\t--load Loads an existing perceptron from LOADFILE.")
    print("\t--save Save the perceptron’s state into SAVEFILE. If not provided, the state of the perceptron will be displayed on standard output.")
    print("\tFILE a file containing a list of inputs (and expected outputs) that the perceptron needs to evaluate (either for training, or predicting).")


# input values
# hidden layers, each with a number of neurons
# output values


class NeuralNetwork:
    def __init__(self, layers_sizes):
        self.layers_sizes = layers_sizes
        self.num_layers = len(layers_sizes)
        self.weights = [np.random.uniform(-1, 1, (layers_sizes[i+1], layers_sizes[i])) for i in range(self.num_layers - 1)]
        self.biases = [np.zeros((size, 1)) for size in layers_sizes[1:]]
        self.activations = [np.zeros((size, 1)) for size in layers_sizes]
        self.learning_rate = 0.01

    def feed_forward(self, inputs):
        self.activations[0] = inputs.reshape((len(inputs), 1))

        for i in range(self.num_layers - 1):
            weighted_sum = np.dot(self.weights[i], self.activations[i]) + self.biases[i]
            self.activations[i + 1] = sigmoid(weighted_sum)

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
            'biases': [arr.tolist() for arr in self.biases]
        }
        with open(filename, 'w') as file:
            json.dump(data, file)

    def load(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        self.weights = [np.array(data_list) for data_list in data['weights']]
        self.biases = [np.array(data_list) for data_list in data['biases']]

def main(argv):
    args = PerceptronArguments()

    if handle_perceptron_arguments(argv, args) == 84:
        return 84

    if args.new_perceptron:
        perceptron_data = pd.read_csv(args.input_file)
        to_train = perceptron_data.values.tolist()
        # Set up the NeuralNetwork
        input_size = args.nb_inputs
        output_size = 1
        hidden_layer_sizes = [8]  # adjust the number of hidden layers and nodes

        nn = NeuralNetwork([input_size] + hidden_layer_sizes + [output_size])

        # Training loop
        epochs = 10000
        for _ in range(epochs):
            for data_point in to_train:
                inputs = np.array(data_point[:-1])
                expected_output = np.array([data_point[-1]])
                nn.train(inputs, expected_output)

        # Test the trained model on AND gate inputs
        for data_point in to_train:
            inputs = np.array(data_point[:-1])
            expected_output = np.array([data_point[-1]])
            prediction = nn.predict(inputs)
            print(f"Inputs: {inputs}, Expected: {expected_output}, Predicted: {prediction} = {round(prediction[0][0])}")

        if args.save_perceptron:
            nn.save(args.save_file)

    elif args.load_perceptron:
        nn = NeuralNetwork([2, 8, 1])
        nn.load(args.load_file)
        perceptron_data = pd.read_csv(args.input_file)
        # line_of_data = len(perceptron_data.columns) - 1
        to_predict = perceptron_data.values.tolist()
        for data_point in to_predict:
            inputs = np.array(data_point[:-1])
            expected_output = np.array([data_point[-1]])
            prediction = nn.predict(inputs)
            print(f"Inputs: {inputs}, Expected: {expected_output}, Predicted: {prediction} = {round(prediction[0][0])}")

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

# ./my_perceptron --new 2 --save save.json --mode train and.csv
# ./my_perceptron --load save.json --mode predict and.csv