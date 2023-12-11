import json
import sys
class Chess:
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_file(cls, filename):
        all_data = []

        with open(filename, 'r') as file:
            lines = file.readlines()

        for i in range(0, len(lines), 12):
            game_data = lines[i:i + 12]

            checkmate_line = [line.strip() for line in game_data if line.startswith('CHECKMATE:')][0]
            checkmate_value = checkmate_line.split(': ')[1].lower() == 'true'

            res_line = [line.strip() for line in game_data if line.startswith('RES:')][0]
            res_value = res_line.split(': ')[1] # ? not necessary

            fen_line = [line.strip() for line in game_data if line.startswith('FEN:')][0]
            fen_value = fen_line.split(': ')[1]

            board, turn = cls.parse_fen(fen_value)

            data = {
                "inputs": board,
                "output": checkmate_value
            }

            all_data.append(data)
        return all_data

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


def board_to_json(chess_instance):
    # Convert the board to the desired JSON format
    inputs = []
    for i in range(0, 1000):
        inputs.append(chess_instance[i]["inputs"])

    output = []
    for i in range(0, 1000):
        output.append(chess_instance[i]["output"])

    json_output = {
        "inputs": inputs,
        "output": output,
        "layer_sizes": [64, 32, 32, 32, 1], # ? not necessary
    }

    return json_output


def main(argv):
    if len(argv) != 3:
        print(f'Usage: {argv[0]} <input_file> <output_file>')
        return 84

    chess_instance = Chess.from_file(argv[1])

    print(f'Loaded {len(chess_instance)} games from {argv[1]}')

    json_output = board_to_json(chess_instance)
    with open(argv[2], 'w') as file:
        json.dump(json_output, file)

    print(f'JSON output saved to {argv[2]}')
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))


# changer la fonction d'activation
# changer le nombre de repetition du training