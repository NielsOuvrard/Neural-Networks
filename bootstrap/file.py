import sys
import random
import math
import pandas as pd
import numpy as np

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

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
    def __init__(self, nb_inputs: int):
        self.nb_inputs = nb_inputs
        self.weights = [0.0] * nb_inputs
        self.inputs = [0.0] * nb_inputs
        self.bias = round(random.uniform(-10, 10))

        for i in range(nb_inputs):
            self.weights[i] = round(random.uniform(-1, 1), 3)
            self.inputs[i] = round(random.uniform(-1, 1), 3)

        print("self.inputs")
        print(self.inputs)
        print("self.weights")
        print(self.weights)
        print("self.bias")
        print(self.bias)
        print("")

    def __init__(self, perceptron_data: list):
        # perceptron_data until the last one are the inputs
        # the last one is the expected output
        self.nb_inputs = len(perceptron_data) - 1
        self.weights = [1.0] * self.nb_inputs
        self.inputs = [0.0] * self.nb_inputs
        self.bias = -1.5
        self.expected_output = perceptron_data[self.nb_inputs]
        self.predicted_output = 0.0

        for i in range(self.nb_inputs):
            self.inputs[i] = perceptron_data[i]

        print("self.inputs")
        print(self.inputs)
        print("self.weights")
        print(self.weights)
        print("self.bias")
        print(self.bias)

    def __str__(self):
        return "NeuralNetwork(nb_inputs={}, weights={}, bias={})".format(self.nb_inputs, self.weights, self.bias)

    def __repr__(self):
        return self.__str__()

    def train(self):
        tmp = self.predicted_output - self.expected_output

    # def feed_forward(self, a):
    #     """Return the output of the neural network if `inputs` are given."""
    #     for b, w in zip(self.biases, self.weights):
    #         a = sigmoid(np.dot(w, a)+b)
    #     return a

    def cost(self):
        cost_value = 0.0
        for i in range(self.nb_inputs):
            cost_value += pow(self.inputs[i] - self.expected_output[i], 2)
        return cost_value

    def predict(self): # inputs
        value = 0.0
        for i in range(self.nb_inputs):
            value += self.inputs[i] * self.weights[i]
        value += self.bias # how calculate the bias ?
        sigmoid_value = sigmoid(value)
        self.predicted_output = sigmoid_value
        return sigmoid_value

def main(argv):
    args = PerceptronArguments()

    if handle_perceptron_arguments(argv, args) == 84:
        return 84

    if args.new_perceptron:
        perceptron = NeuralNetwork(args.nb_inputs)
        print(perceptron.predict())
    elif args.load_perceptron:
        perceptron_data = pd.read_csv(args.load_file)
        line_of_data = len(perceptron_data.columns) - 1
        perceptron_list = perceptron_data.values.tolist()

        for line in perceptron_list:
            print(line)
            perceptron = NeuralNetwork(line) # remove the first column
            prediction = perceptron.predict()
            if prediction != perceptron.expected_output:
                perceptron.train()
            print("prediction:", (prediction), "expected:", line[line_of_data])
            print("", end="\n\n")
            #

    # print_perceptron_arguments(args)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
