import copy
import math

from src.constants import COLUMN_COUNT
from src.board import drop_piece, valid_location, get_next_open_row, check_win, check_draw
from src.heuristic import score_position
from src.minimax import is_terminal_node

PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0


def get_ordered_moves(board):
    """
    Return valid column indices sorted by proximity to the center column.

    For a 7-column board the order is: [3, 2, 4, 1, 5, 0, 6]
    Trying center columns first maximises the probability of an alpha-beta
    cutoff on the very first child, effectively doubling usable search depth.

    Args:
        board: 6x7 2-D list

    Returns:
        list[int]: valid column indices ordered center-first
    """
    center = COLUMN_COUNT // 2
    return sorted(
        [c for c in range(COLUMN_COUNT) if valid_location(board, c)],
        key=lambda c: abs(c - center)
    )


def minimax_alphabeta(board, depth, alpha, beta, maximizing_player):
    """
    Minimax with Alpha-Beta Pruning.

    Identical logic to minimax() in minimax.py except:
        - Uses get_ordered_moves() instead of get_valid_locations()
        - After each child evaluation:
              maximizing: alpha = max(alpha, score); prune if alpha >= beta
              minimizing: beta  = min(beta,  score); prune if alpha >= beta

    Args:
        board             : 6x7 2-D list
        depth             : int, remaining search depth
        alpha             : float, best score the maximizer can guarantee (-inf at root)
        beta              : float, best score the minimizer can guarantee (+inf at root)
        maximizing_player : bool

    Returns:
        tuple (best_column, best_score)
    """
    valid_locations = get_ordered_moves(board)
    terminal = is_terminal_node(board)

    if terminal:
        if check_win(board, AI_PIECE):
            return (None, 1_000_000 + depth)
        elif check_win(board, PLAYER_PIECE):
            return (None, -1_000_000 - depth)
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
            _, new_score = minimax_alphabeta(b_copy, depth - 1, alpha, beta, False)
            if new_score > best_score:
                best_score = new_score
                best_col = col
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        return best_col, best_score

    else:
        best_score = math.inf
        best_col = valid_locations[0]

        for col in valid_locations:
            b_copy = copy.deepcopy(board)
            row = get_next_open_row(b_copy, col)
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            _, new_score = minimax_alphabeta(b_copy, depth - 1, alpha, beta, True)
            if new_score < best_score:
                best_score = new_score
                best_col = col
            beta = min(beta, best_score)
            if alpha >= beta:
                break

        return best_col, best_score


def get_best_move_alphabeta(board, depth=5):
    """
    Entry point for the alpha-beta AI.

    Uses a deeper default depth than pure minimax (5 vs 4) because pruning
    makes the extra depth affordable in practice.

    Args:
        board : 6x7 2-D list
        depth : int (default 5)

    Returns:
        int: best column index for the AI to play
    """
    col, _ = minimax_alphabeta(board, depth, -math.inf, math.inf, True)
    return col
