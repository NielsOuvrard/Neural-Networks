import json
import sys

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
            'r': 1,
            'n': 2,
            'b': 3,
            'q': 4,
            'k': 5,
            'p': 6,
            'R': 7,
            'N': 8,
            'B': 9,
            'Q': 10,
            'K': 11,
            'P': 12
        }
        board = [0 for _ in range(8 * 8)]

        fen_parts = fen.split(' ')
        rows = fen_parts[0].split('/')

        for i, row in enumerate(rows):
            j = 0
            for char in row:
                if char.isdigit():
                    j += int(char)
                else:
                    board[(i * 8) + j] = pieces[char]
                    j += 1

        return board, 'white' if fen_parts[1] == 'w' else 'black'


def board_to_json(board, checkmate):
    # Convert the board to the desired JSON format
    json_output = {
        "inputs": [board],
        "output": int(checkmate),
        "layer_sizes": [64, 32, 32, 32, 1], # ? not necessary
    }

    return json_output


def main(argv):
    if len(argv) != 3:
        print(f'Usage: {argv[0]} <input_file> <output_file>')
        return 84

    chess_instance = Chess.from_file(argv[1])

    json_output = board_to_json(chess_instance.board, chess_instance.checkmate)

    with open(argv[2], 'w') as file:
        json.dump(json_output, file)

    print(f'JSON output saved to {argv[2]}')
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
