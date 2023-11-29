import sys

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
    print("./my_perceptron [--new NB_INPUTS | --load LOADFILE] [--save SAVEFILE] --mode [train | predict] FILE")
    print("DESCRIPTION")
    print("--new Creates a new perceptron with NB_INPUTS inputs.")
    print("--load Loads an existing perceptron from LOADFILE.")
    print("--save Save the perceptron’s state into SAVEFILE. If not provided, the state of the perceptron will be displayed on standard output.")
    print("FILE a file containing a list of inputs (and expected outputs) that the perceptron needs to evaluate (either for training, or predicting).")

class NeuralNetwork:
    def __init__(self, nb_inputs):
        self.nb_inputs = nb_inputs
        self.weights = [0.0] * nb_inputs
        self.bias = 0.0

    def __str__(self):
        return "NeuralNetwork(nb_inputs={}, weights={}, bias={})".format(self.nb_inputs, self.weights, self.bias)

    def __repr__(self):
        return self.__str__()

    def train(self, inputs, expected_output):
        # TODO
        pass

    def predict(self, inputs):
        # TODO
        pass

def main(argv):
    args = PerceptronArguments()

    if handle_perceptron_arguments(argv, args) == 84:
        return 84

    print_perceptron_arguments(args)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
