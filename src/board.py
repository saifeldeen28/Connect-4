from .constants import ROW_COUNT, COLUMN_COUNT


def create_board():
    return [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row


def check_win(board, piece):
    for col in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT):
            if all(board[row][col + i] == piece for i in range(4)):
                return True
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - 3):
            if all(board[row + i][col] == piece for i in range(4)):
                return True
    for col in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT - 3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True
    for col in range(COLUMN_COUNT - 3):
        for row in range(3, ROW_COUNT):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True
    return False


def check_draw(board):
    return all(board[ROW_COUNT - 1][col] != 0 for col in range(COLUMN_COUNT))


def print_board(board):
    for row in range(ROW_COUNT - 1, -1, -1):
        print(board[row])
