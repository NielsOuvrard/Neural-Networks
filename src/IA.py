import sys
import numpy as np
from arguments import Arguments, handle_arguments
from NeuralNetwork import NeuralNetwork
import json

def execute(args : Arguments):
    if args.new_network:
        with open(args.input_file, 'r') as json_file:
            data = json.load(json_file)

        to_train = data["inputs"]
        output_value = data["output"]

        # Set up the NeuralNetwork
        nn = NeuralNetwork(args.layers)

        # Training loop
        epochs = 10000
        for _ in range(epochs):
            for i in range(len(to_train)):
                inputs = np.array(to_train[i])
                expected_output = np.array([output_value[i]])
                nn.train(inputs, expected_output)

        # Test the trained model on AND gate inputs
        for i in range(len(to_train)):
            inputs = np.array(to_train[i])
            expected_output = np.array([output_value[i]])
            prediction = nn.predict(inputs)
            print(f"Inputs: {inputs}, Expected: {expected_output}, Predicted: {prediction} = {round(prediction[0][0])}")

        if args.save_network:
            nn.save(args.save_file)

    elif args.save_network:
        nn = NeuralNetwork(args.layers)
        nn.load(args.load_file)

        with open(args.input_file, 'r') as json_file:
            data = json.load(json_file)

        to_predict = data["inputs"]
        output_value = data["output"]

        for i in range(len(to_train)):
            inputs = np.array(to_train[i])
            expected_output = np.array([output_value[i]])
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
