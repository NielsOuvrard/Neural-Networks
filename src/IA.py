import sys
import numpy as np
from arguments import Arguments, handle_arguments
from NeuralNetwork import NeuralNetwork
import json

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return np.where(x > 0, 1, 0)

def tanh(x):
    return np.tanh(x)

def tanh_derivative(x):
    return 1 - np.tanh(x)**2

def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)

def leaky_relu_derivative(x, alpha=0.01):
    return np.where(x > 0, 1, alpha)

def execute(args : Arguments):
    nn = NeuralNetwork(layers_sizes=args.layers, learning_rate=args.learning_rate)#, evaluation_function=relu, evaluation_function_derivative=relu_derivative)
    if args.new_network:
        # Set up the NeuralNetwork

        if args.train_mode:
            with open(args.input_file, 'r') as json_file:
                data = json.load(json_file)
            to_train = data["inputs"]
            output_value = data["output"]
            for _ in range(args.epochs):

                # * Training loop
                for i in range(len(to_train)):
                    inputs = np.array(to_train[i])
                    nn.train(inputs, output_value[i])

                # Test the trained model on AND gate inputs
                for i in range(len(to_train)):
                    inputs = np.array(to_train[i])
                    expected_output = np.array(output_value[i])
                    prediction = nn.predict(inputs)
                    # print(f"Expected: {expected_output}, Predicted: {prediction} = {round(prediction[0][0])}")

        if args.save_network:
            nn.save(args.save_file)

    elif args.load_network:

        nn.load(args.load_file)

        with open(args.input_file, 'r') as json_file:
            data = json.load(json_file)

        to_predict = data["inputs"]
        output_value = data["output"]

        # * Training loop
        if args.train_mode:
            for i in range(len(to_predict)):
                inputs = np.array(to_predict[i])
                expected_output = np.array([output_value[i]])
                nn.train(inputs, expected_output)

            if args.save_network:
                nn.save(args.save_file)

        # * Predicting loop
        if args.predict_mode:
            all_predictions = []
            for i in range(len(to_predict)):
                inputs = np.array(to_predict[i])
                prediction = nn.predict(inputs)
                output_value[i] = int(output_value[i])
                all_predictions.append(round(prediction[0][0]) == output_value[i])
                # print(f"Expected: {output_value[i]}, Predicted: {round(prediction[0][0], 3)} = {round(prediction[0][0])} -> {round(prediction[0][0]) == output_value[i]}")
            print("Accuracy: ", sum(all_predictions) / len(all_predictions))

    return 0


def main(argv):
    args = Arguments()

    if handle_arguments(argv, args) == 84:
        return 84
    elif args.help:
        return 0
    return execute(args)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
