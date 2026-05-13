import copy
import math

from src.constants import COLUMN_COUNT
from src.board import drop_piece, valid_location, get_next_open_row, check_win, check_draw
from src.heuristic import score_position

PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0


def is_terminal_node(board):
    """
    Return True if the game is over (either player has won, or board is full).

    Args:
        board: 6x7 2-D list
    Returns:
        bool
    """
    return (
        check_win(board, PLAYER_PIECE)
        or check_win(board, AI_PIECE)
        or check_draw(board)
    )


def get_valid_locations(board):
    """
    Return all columns that still have at least one empty cell.

    Args:
        board: 6x7 2-D list
    Returns:
        list[int]: valid column indices (0-6)
    """
    return [col for col in range(COLUMN_COUNT) if valid_location(board, col)]


def minimax(board, depth, maximizing_player):
    """
    Recursive minimax with a depth limit. No pruning.

    Base cases:
        - Terminal node  -> return (None, large positive/negative score or 0 for draw)
        - depth == 0     -> return (None, score_position(board, AI_PIECE))

    Recursive cases:
        - maximizing_player == True  -> choose column with HIGHEST child score
        - maximizing_player == False -> choose column with LOWEST child score

    Args:
        board             : 6x7 2-D list (current state)
        depth             : int, remaining search depth
        maximizing_player : bool, True when it is the AI's turn

    Returns:
        tuple (best_column, best_score)
            best_column is None at leaf nodes (caller ignores it there)
    """
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)

    if terminal:
        if check_win(board, AI_PIECE):
            return (None, 1_000_000)
        elif check_win(board, PLAYER_PIECE):
            return (None, -1_000_000)
        else:
            return (None, 0)

    if depth == 0:
        return (None, score_position(board, AI_PIECE))

    if maximizing_player:
        best_score = -math.inf
        best_col = valid_locations[0]

        for col in valid_locations:
            b_copy = copy.deepcopy(board)
            row = get_next_open_row(b_copy, col)
            drop_piece(b_copy, row, col, AI_PIECE)
            _, new_score = minimax(b_copy, depth - 1, False)
            if new_score > best_score:
                best_score = new_score
                best_col = col

        return best_col, best_score

    else:
        best_score = math.inf
        best_col = valid_locations[0]

        for col in valid_locations:
            b_copy = copy.deepcopy(board)
            row = get_next_open_row(b_copy, col)
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            _, new_score = minimax(b_copy, depth - 1, True)
            if new_score < best_score:
                best_score = new_score
                best_col = col

        return best_col, best_score


def get_best_move(board, depth=4):
    """
    Entry point for pure minimax AI.

    Args:
        board : 6x7 2-D list
        depth : int, search depth (default 4)

    Returns:
        int: best column index for the AI to play
    """
    col, _ = minimax(board, depth, True)
    return col
