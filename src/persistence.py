def check_name(user_input):
    file_name = user_input + '.txt'
    try:
        with open(file_name, 'r'):
            pass
        with open(file_name, 'a'):
            pass
        return True, file_name
    except FileNotFoundError:
        with open(file_name, 'a'):
            pass
        return False, file_name


def save_game(file_name, board):
    with open(file_name, 'w') as f:
        for row in board:
            f.write(''.join(str(v) for v in row) + '\n')


def load_game(file_name):
    board = []
    with open(file_name, 'r') as f:
        for line in f:
            row = [int(v) for v in line.strip()]
            board.append(row)
    return board
