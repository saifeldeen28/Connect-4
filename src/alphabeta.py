# Person 3 — Alpha-Beta Pruning + Move Ordering
# Task: Implement minimax with alpha-beta pruning and center-first move ordering.
#
# Alpha-beta pruning eliminates branches that cannot affect the final decision,
# letting the AI search deeper within the same time budget as pure minimax.
#
# Move ordering (center-first) is a greedy insight: center columns tend to
# produce stronger positions, so evaluating them first increases the chance of
# early cutoffs, making alpha-beta even more effective.

import copy
import math

from src.constants import ROW_COUNT, COLUMN_COUNT
from src.board import drop_piece, valid_location, get_next_open_row, check_win, check_draw
from src.heuristic import score_position
from src.minimax import is_terminal_node   # reuse the terminal check from Person 2

PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0


def get_ordered_moves(board):
    """
    Return valid column indices sorted by proximity to the center column.

    For a 7-column board the ideal order is: [3, 2, 4, 1, 5, 0, 6]
    Trying center columns first maximises the probability of an alpha-beta
    cutoff on the very first child, effectively doubling search depth.

    Args:
        board: 6×7 2-D list

    Returns:
        list[int]: valid column indices ordered center-first
    """
    center = COLUMN_COUNT // 2
    # TODO: get all valid cols, then sort by abs(col - center)
    # Hint: sorted([c for c in range(COLUMN_COUNT) if valid_location(board, c)],
    #              key=lambda c: abs(c - center))
    pass


def minimax_alphabeta(board, depth, alpha, beta, maximizing_player):
    """
    Minimax with Alpha-Beta Pruning.

    Identical logic to minimax() in minimax.py EXCEPT:
        - Uses get_ordered_moves() instead of get_valid_locations()
        - After each child evaluation:
              maximizing: alpha = max(alpha, score); prune if alpha >= beta
              minimizing: beta  = min(beta,  score); prune if alpha >= beta

    Args:
        board             : 6×7 2-D list
        depth             : int, remaining search depth
        alpha             : float, best score the maximizer can guarantee (-inf at root)
        beta              : float, best score the minimizer can guarantee (+inf at root)
        maximizing_player : bool

    Returns:
        tuple (best_column, best_score)
    """
    valid_locations = get_ordered_moves(board)
    terminal = is_terminal_node(board)

    # --- Base cases ---
    if terminal:
        # TODO: same terminal scoring as minimax.py
        #   AI wins  → (None,  1_000_000)
        #   P1 wins  → (None, -1_000_000)
        #   draw     → (None, 0)
        pass

    if depth == 0:
        # TODO: return (None, score_position(board, AI_PIECE))
        pass

    # --- Maximizing (AI's turn) ---
    if maximizing_player:
        best_score = -math.inf
        best_col = valid_locations[0]

        for col in valid_locations:
            # TODO: b_copy = copy.deepcopy(board)
            # TODO: simulate move with AI_PIECE
            # TODO: _, new_score = minimax_alphabeta(b_copy, depth-1, alpha, beta, False)
            # TODO: if new_score > best_score: update best_score, best_col
            # TODO: alpha = max(alpha, best_score)
            # TODO: if alpha >= beta: break   ← PRUNING CUT
            pass

        return best_col, best_score

    # --- Minimizing (human's turn) ---
    else:
        best_score = math.inf
        best_col = valid_locations[0]

        for col in valid_locations:
            # TODO: simulate move with PLAYER_PIECE
            # TODO: _, new_score = minimax_alphabeta(b_copy, depth-1, alpha, beta, True)
            # TODO: if new_score < best_score: update best_score, best_col
            # TODO: beta = min(beta, best_score)
            # TODO: if alpha >= beta: break   ← PRUNING CUT
            pass

        return best_col, best_score


def get_best_move_alphabeta(board, depth=5):
    """
    Entry point for the alpha-beta AI.

    Uses a deeper default depth than pure minimax (5 vs 4) because pruning
    makes the extra depth affordable in practice.

    Args:
        board : 6×7 2-D list
        depth : int (default 5)

    Returns:
        int: best column index for the AI to play
    """
    # TODO: col, _ = minimax_alphabeta(board, depth, -math.inf, math.inf, True)
    # TODO: return col
    pass
