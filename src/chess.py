import json
import sys


#     'r' = 'black_rook',    = -5
#     'n' = 'black_knight',  = -3
#     'b' = 'black_bishop',  = -3
#     'q' = 'black_queen',   = -9
#     'k' = 'black_king',    = -200
#     'p' = 'black_pawn',    = -1
#
#     'R' = 'white_rook',    = 5
#     'N' = 'white_knight',  = 3
#     'B' = 'white_bishop',  = 3
#     'Q' = 'white_queen',   = 9
#     'K' = 'white_king',    = 200
#     'P' = 'white_pawn',    = 1

# "output": [
#     1 if result_value == '1/2-1/2' else 0,
#     1 if result_value == '1-0' else 0,
#     1 if result_value == '0-1' else 0,
# ]
# "output":
#     1 if result_value == '1/2-1/2' else 0,

# RES: 1/2-1/2 / RES: 1-0 / RES: 0-1
# 1/2-1/2 # output equal
# 1-0     # output white win
# 0-1     # output black win
# result_value = result_line.split(': ')[1]
# result_line = [line.strip() for line in game_data if line.startswith('RES:')][0]

class Chess:
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_files(cls, *filenames):
        all_data = []
        all_files_data = []

        for filename in filenames:
            with open(filename, 'r') as file:
                lines = file.readlines()
                all_files_data.append(lines)

        def process_game_data(lines, all_data, cls, i):
            if i < len(lines):
                game_data = lines[i:i + 12]

                checkmate_line = [line.strip() for line in game_data if line.startswith('CHECKMATE:')][0]
                checkmate_value = checkmate_line.split(': ')[1].lower() == 'true'

                fen_line = [line.strip() for line in game_data if line.startswith('FEN:')][0]
                fen_value = fen_line.split(': ')[1]

                board = cls.parse_fen(fen_value) if hasattr(cls, 'parse_fen') else (cls.parse_fen(fen_value), None)

                data = {
                    "inputs": board,
                    "output": checkmate_value
                }
                all_data.append(data)
                return 0
            else:
                return 1

        for i in range(0, len(lines), 12):
            for lines in all_files_data:
                if process_game_data(lines, all_data, cls, i):
                    return all_data

        return all_data

    @staticmethod
    def parse_fen(fen):
        pieces = {
            'r': -5,
            'n': -3,
            'b': -3,
            'q': -9,
            'k': -200,
            'p': -1,

            'R': 5,
            'N': 3,
            'B': 3,
            'Q': 9,
            'K': 200,
            'P': 1
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

        return board


def board_to_json(chess_instance):
    # Convert the board to the desired JSON format
    inputs = []
    for i in range(len(chess_instance) - 1, len(chess_instance) - 1 - 50, -1):
    # for i in range(len(chess_instance) - 50):
        inputs.append(chess_instance[i]["inputs"])

    output = []
    for i in range(len(chess_instance) - 1, len(chess_instance) - 1 - 50, -1):
    # for i in range(len(chess_instance) - 50):
        output.append(chess_instance[i]["output"])

    json_output = {
        "inputs": inputs,
        "output": output,
        "layer_sizes": [64, 32, 32, 32, 1],  # ? not necessary
    }

    return json_output


def main(argv):
    if len(argv) < 4:
        print(f'Usage: {argv[0]} <input_file1> <input_file2> ... <output_file>')
        return 84

    input_files = argv[1:-1]
    output_file = argv[-1]

    chess_instance = Chess.from_files(*input_files)

    print(f'Loaded {len(chess_instance)} games from {", ".join(input_files)}')

    json_output = board_to_json(chess_instance)
    with open(output_file, 'w') as file:
        json.dump(json_output, file)

    print(f'JSON output saved to {output_file}')
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
