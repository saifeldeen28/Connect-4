from src.constants import ROW_COUNT, COLUMN_COUNT

PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0
WINDOW_LENGTH = 4


def score_window(window, piece):
    score = 0
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    piece_count = window.count(piece)
    empty_count = window.count(EMPTY)
    opp_count = window.count(opponent_piece)

    if piece_count == 4:
        score += 100
    elif piece_count == 3 and empty_count == 1:
        score += 5
    elif piece_count == 2 and empty_count == 2:
        score += 2

    if opp_count == 3 and empty_count == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    center_array = [int(board[r][COLUMN_COUNT // 2]) for r in range(ROW_COUNT)]
    score += center_array.count(piece) * 3

    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r][c + i] for i in range(WINDOW_LENGTH)]
            score += score_window(window, piece)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            window = [board[r + i][c] for i in range(WINDOW_LENGTH)]
            score += score_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += score_window(window, piece)

    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r - i][c + i] for i in range(WINDOW_LENGTH)]
            score += score_window(window, piece)

    return score
