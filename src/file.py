import sys
import pandas as pd
import numpy as np
from arguments import Arguments, handle_arguments
from NeuralNetwork import NeuralNetwork

def execute(args : Arguments):
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



def main(argv):
    args = Arguments()

    if handle_arguments(argv, args) == 84:
        return 84
    elif args.help:
        return 0

    return execute(args)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
