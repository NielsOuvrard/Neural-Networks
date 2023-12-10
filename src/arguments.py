class Arguments:
    def __init__(self):
        self.help = False
        self.new_network = False
        self.load_network = False
        self.train_mode = False
        self.predict_mode = False
        self.save_network = False
        self.load_file = ""
        self.save_file = ""
        self.layers = []
        self.input_file = ""

def handle_arguments(argv, args):
    for x in range(1, len(argv)):
        if argv[x][0] != '-':
            # Non-option argument (FILE)
            args.input_file = argv[x]
            continue

        option = argv[x][2]
        if option == 'n':
            args.new_network = True
            x += 1  # move to the next argument
            while x < len(argv) and argv[x][0] != '-':
                args.layers.append(int(argv[x]))
                x += 1
        elif option == 'l':
            args.load_network = True
            x += 1
            args.load_file = argv[x]
        elif option == 't':
            args.train_mode = True
        elif option == 'p':
            args.predict_mode = True
        elif option == 's':
            args.save_network = True
            x += 1
            args.save_file = argv[x]
        elif option == 'h':
            args.help = True
            print_usage()
            return 0
        else:
            print("Invalid option. Use --help for help.")
            return 84

    # Validate if mandatory arguments are provided
    if not args.new_network and not args.load_network:
        print("Either --new or --load must be specified. Use --help for help.")
        return 84

    if not args.train_mode and not args.predict_mode:
        print("Either --train or --predict must be specified. Use --help for help.")
        return 84

    if args.new_network and args.load_network:
        print("--new and --load cannot be used together. Use --help for help.")
        return 84

    return 0

def print_arguments(args):
    # Adjust the output based on the new structure of arguments_t for the neural network project

    print("Input File:", args.input_file)

    if args.new_network:
        print("New Network:", *args.layers)

    if args.load_network:
        print("Load Network:", args.load_file)

    print("Train Mode:", args.train_mode)
    print("Predict Mode:", args.predict_mode)

    if args.save_network:
        print("Save Network:", args.save_file)

def print_usage():
    print("USAGE")
    print("\t./my_torch [--new IN_LAYER [HIDDEN_LAYERS...] OUT_LAYER | --load LOADFILE] [--train | --predict] [--save SAVEFILE] FILE")
    print("DESCRIPTION")
    print("\t--new Creates a new neural network with random weights. Each subsequent number represents the number of neurons on each layer, from left to right. For example, ./my_torch –new 3 4 5 will create a neural network with an input layer of 3 neurons, a hidden layer of 4 neurons, and an output layer of 5 neurons.")
    print("\t--load Loads an existing neural network from LOADFILE.")
    print("\t--train Launches the neural network in training mode. Each board in FILE must contain inputs to send to the neural network, as well as the expected output.")
    print("\t--predict Launches the neural network in prediction mode. Each board in FILE must contain inputs to send to the neural network, and optionally an expected output.")
    print("\t--save Save neural network internal state into SAVEFILE.")
    print("\tFILE FILE containing chessboards")
