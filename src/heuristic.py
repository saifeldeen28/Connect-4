# Person 1 — Greedy Heuristic Evaluation
# Task: Implement score_window() and score_position().
# These functions are the heart of the AI: every minimax node calls
# score_position() to judge how "good" a board is without playing to the end.

from src.constants import ROW_COUNT, COLUMN_COUNT
from src.board import check_win

PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0
WINDOW_LENGTH = 4


def score_window(window, piece):
    """
    Score a single 4-cell window for the given piece.

    Scoring rules (greedy heuristics):
        +100  — 4 in a row (piece wins this window)
        +5    — 3 of piece + 1 empty
        +2    — 2 of piece + 2 empty
        -4    — opponent has 3 in a row + 1 empty (threat — penalize)

    Args:
        window : list of 4 ints (each 0, 1, or 2)
        piece  : int, the AI's piece value (1 or 2)

    Returns:
        int: score contribution for this window
    """
    score = 0
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    # TODO: count piece and EMPTY occurrences in window
    # Hint: piece_count  = window.count(piece)
    #        empty_count  = window.count(EMPTY)
    #        opp_count    = window.count(opponent_piece)

    # TODO: apply scoring rules and return score
    pass


def score_position(board, piece):
    """
    Evaluate the entire board and return a heuristic score for `piece`.

    A higher score means the board is more favorable for `piece`.
    A lower (more negative) score means the board favors the opponent.

    Must evaluate:
        1. Center preference  — pieces in column 3 score +3 each
        2. Horizontal windows — all [r][c : c+4] windows
        3. Vertical windows   — all [r : r+4][c] windows
        4. Positive-slope diagonals (bottom-left → top-right)
        5. Negative-slope diagonals (top-left → bottom-right)

    Args:
        board : 6×7 2-D list of ints
        piece : int, the AI's piece value

    Returns:
        int: total heuristic score
    """
    score = 0

    # --- 1. Center column preference ---
    # TODO: collect center_array = [board[r][COLUMN_COUNT // 2] for r in range(ROW_COUNT)]
    # TODO: score += center_array.count(piece) * 3

    # --- 2. Horizontal windows ---
    # TODO: for r in range(ROW_COUNT):
    #           for c in range(COLUMN_COUNT - 3):
    #               window = [board[r][c + i] for i in range(WINDOW_LENGTH)]
    #               score += score_window(window, piece)

    # --- 3. Vertical windows ---
    # TODO: for c in range(COLUMN_COUNT):
    #           for r in range(ROW_COUNT - 3):
    #               window = [board[r + i][c] for i in range(WINDOW_LENGTH)]
    #               score += score_window(window, piece)

    # --- 4. Positive-slope diagonal windows ---
    # TODO: for r in range(ROW_COUNT - 3):
    #           for c in range(COLUMN_COUNT - 3):
    #               window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
    #               score += score_window(window, piece)

    # --- 5. Negative-slope diagonal windows ---
    # TODO: for r in range(3, ROW_COUNT):
    #           for c in range(COLUMN_COUNT - 3):
    #               window = [board[r - i][c + i] for i in range(WINDOW_LENGTH)]
    #               score += score_window(window, piece)

    return score
