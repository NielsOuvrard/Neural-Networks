import sys
import pandas as pd
import numpy as np
from arguments import Arguments, handle_arguments
from NeuralNetwork import NeuralNetwork
class Chess:
    def __init__(self, checkmate, res, board, turn):
        self.checkmate = checkmate
        self.res = res
        self.board = board
        self.turn = turn

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as file:
            data = file.readlines()

        checkmate_line = [line.strip() for line in data if line.startswith('CHECKMATE:')][0]
        checkmate_value = checkmate_line.split(': ')[1].lower() == 'true'

        res_line = [line.strip() for line in data if line.startswith('RES:')][0]
        res_value = res_line.split(': ')[1]

        fen_line = [line.strip() for line in data if line.startswith('FEN:')][0]
        fen_value = fen_line.split(': ')[1]

        board, turn = cls.parse_fen(fen_value)

        return cls(checkmate=checkmate_value, res=res_value, board=board, turn=turn)

    @staticmethod
    def parse_fen(fen):
        pieces = {
            'r': 'black_rook',
            'n': 'black_knight',
            'b': 'black_bishop',
            'q': 'black_queen',
            'k': 'black_king',
            'p': 'black_pawn',
            'R': 'white_rook',
            'N': 'white_knight',
            'B': 'white_bishop',
            'Q': 'white_queen',
            'K': 'white_king',
            'P': 'white_pawn'
        }
        board = [['' for _ in range(8)] for _ in range(8)]

        fen_parts = fen.split(' ')
        rows = fen_parts[0].split('/')

        for i, row in enumerate(rows):
            j = 0
            for char in row:
                if char.isdigit():
                    j += int(char)
                else:
                    board[i][j] = pieces[char]
                    j += 1

        return board, 'white' if fen_parts[1] == 'w' else 'black'


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

    # open self.load_file
    chess_instance = Chess.from_file(args.input_file)
    print(f'Checkmate: {chess_instance.checkmate}')
    print(f'RES: {chess_instance.res}')
    print(f'Board:')
    for row in chess_instance.board:
        print(row)
    print(f'Turn: {chess_instance.turn}')


    # return execute(args)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
