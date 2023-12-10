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



chess_instance = Chess.from_file("data/test.txt")
print(f'Checkmate: {chess_instance.checkmate}')
print(f'RES: {chess_instance.res}')
print(f'Board:')
for row in chess_instance.board:
    print(row)
print(f'Turn: {chess_instance.turn}')