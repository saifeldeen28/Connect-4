# Person 2 — Pure Minimax with Depth Limit
# Task: Implement minimax() without alpha-beta pruning.
# This is the baseline AI. The maximizing player is the AI (piece 2);
# the minimizing player is the human (piece 1).
#
# NOTE: Do NOT import from alphabeta.py or transposition.py here.
#       Those modules depend on this one, not the other way around.

import copy
import math

from src.constants import ROW_COUNT, COLUMN_COUNT
from src.board import drop_piece, valid_location, get_next_open_row, check_win, check_draw
from src.heuristic import score_position

PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0


def is_terminal_node(board):
    """
    Return True if the game is over (either player has won, or board is full).

    Args:
        board: 6×7 2-D list
    Returns:
        bool
    """
    # TODO: return True if check_win(board, PLAYER_PIECE)
    #                    or check_win(board, AI_PIECE)
    #                    or check_draw(board)
    pass


def get_valid_locations(board):
    """
    Return all columns that still have at least one empty cell.

    Args:
        board: 6×7 2-D list
    Returns:
        list[int]: valid column indices (0–6)
    """
    # TODO: return [col for col in range(COLUMN_COUNT) if valid_location(board, col)]
    pass


def minimax(board, depth, maximizing_player):
    """
    Recursive minimax with a depth limit. No pruning.

    Base cases:
        - Terminal node  → return (None, large positive/negative score or 0 for draw)
        - depth == 0     → return (None, score_position(board, AI_PIECE))

    Recursive cases:
        - maximizing_player == True  → choose column with HIGHEST child score
        - maximizing_player == False → choose column with LOWEST child score

    To simulate a move without modifying the real board, use copy.deepcopy(board).

    Args:
        board             : 6×7 2-D list (current state)
        depth             : int, remaining search depth
        maximizing_player : bool, True when it is the AI's turn

    Returns:
        tuple (best_column, best_score)
            best_column is None at leaf nodes (caller ignores it there)
    """
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)

    # --- Base cases ---
    if terminal:
        # TODO: if AI wins  → return (None, 1_000_000)
        # TODO: if human wins → return (None, -1_000_000)
        # TODO: draw         → return (None, 0)
        pass

    if depth == 0:
        # TODO: return (None, score_position(board, AI_PIECE))
        pass

    # --- Maximizing (AI's turn) ---
    if maximizing_player:
        best_score = -math.inf
        best_col = valid_locations[0]  # fallback

        for col in valid_locations:
            # TODO: b_copy = copy.deepcopy(board)
            # TODO: row = get_next_open_row(b_copy, col)
            # TODO: drop_piece(b_copy, row, col, AI_PIECE)
            # TODO: _, new_score = minimax(b_copy, depth - 1, False)
            # TODO: if new_score > best_score: update best_score, best_col

        return best_col, best_score

    # --- Minimizing (human's turn) ---
    else:
        best_score = math.inf
        best_col = valid_locations[0]  # fallback

        for col in valid_locations:
            # TODO: same pattern as above but use PLAYER_PIECE and track MIN score
            pass

        return best_col, best_score


def get_best_move(board, depth=4):
    """
    Entry point for pure minimax AI.

    Args:
        board : 6×7 2-D list
        depth : int, search depth (default 4)

    Returns:
        int: best column index for the AI to play
    """
    # TODO: col, _ = minimax(board, depth, True)
    # TODO: return col
    pass
