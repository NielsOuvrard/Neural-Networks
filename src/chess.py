import json

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

    #     'r' = 'black_rook',
    #     'n' = 'black_knight',
    #     'b' = 'black_bishop',
    #     'q' = 'black_queen',
    #     'k' = 'black_king',
    #     'p' = 'black_pawn',
    #
    #     'R' = 'white_rook',
    #     'N' = 'white_knight',
    #     'B' = 'white_bishop',
    #     'Q' = 'white_queen',
    #     'K' = 'white_king',
    #     'P' = 'white_pawn'
    @staticmethod
    def parse_fen(fen):
        board = ['.' for _ in range(8 * 8)]

        fen_parts = fen.split(' ')
        rows = fen_parts[0].split('/')

        for i, row in enumerate(rows):
            j = 0
            for char in row:
                if char.isdigit():
                    j += int(char)
                else:
                    board[i + j] = char
                    j += 1

        return board, 'white' if fen_parts[1] == 'w' else 'black'


def board_to_json(board, checkmate):
    # Create a 2D list representing the board
    board_list = [[piece if piece else '.' for piece in row] for row in board]

    # Convert the board to the desired JSON format
    json_output = {
        "inputs": [sum(board_list, [])],  # Flatten the 2D list into a 1D list
        "output": str(checkmate)
    }

    return json_output

chess_instance = Chess.from_file("datasets/test.txt")

# print(f'Checkmate: {chess_instance.checkmate}')
# print(f'RES: {chess_instance.res}')
# print(f'Board:')
# for i in range(8):
#     print(chess_instance.board[i * 8: i * 8 + 8])
# print(f'Turn: {chess_instance.turn}')


json_output = board_to_json(chess_instance.board, chess_instance.checkmate)
filename = 'datasets/test.json'
with open(filename, 'w') as file:
    json.dump(json_output, file)

print(f'JSON output saved to {filename}')

# call NN with:
# inputs = 8 * 8
# hidden layers = 2
# outputs = 1