import random
import copy
import math

from src.constants import ROW_COUNT, COLUMN_COUNT
from src.board import drop_piece, valid_location, get_next_open_row, check_win, check_draw
from src.heuristic import score_position
from src.minimax import is_terminal_node
from src.alphabeta import get_ordered_moves

PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0


class ZobristHasher:
    """
    Computes and incrementally maintains a Zobrist hash for a Connect Four board.

    The hash of an empty board is 0.
    Placing or removing a piece at (row, col) with value `piece` flips the
    hash by XOR-ing self.table[row][col][piece].
    """

    def __init__(self):
        # table[r][c][0] unused (EMPTY), [1] = P1 bitstring, [2] = P2 bitstring
        self.table = [
            [[0, random.getrandbits(64), random.getrandbits(64)]
             for _ in range(COLUMN_COUNT)]
            for _ in range(ROW_COUNT)
        ]

    def hash_board(self, board):
        """
        Compute the Zobrist hash for an entire board from scratch.

        Args:
            board: 6x7 2-D list
        Returns:
            int: 64-bit hash
        """
        h = 0
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                piece = board[r][c]
                if piece != EMPTY:
                    h ^= self.table[r][c][piece]
        return h

    def update_hash(self, current_hash, row, col, piece):
        """
        Incrementally update the hash after placing (or removing) a piece.

        XOR is its own inverse: XOR-ing the same value twice restores the
        original hash, so this method works for both placing and undoing moves.

        Args:
            current_hash : int, the hash before the move
            row, col     : int, board position
            piece        : int, 1 or 2
        Returns:
            int: updated hash
        """
        return current_hash ^ self.table[row][col][piece]


class TranspositionTable:
    """
    Dictionary-backed cache mapping Zobrist hashes to evaluated scores.

    Each entry: {'score': int, 'depth': int, 'flag': str}
    flag: 'EXACT' | 'LOWERBOUND' | 'UPPERBOUND'
    """

    def __init__(self):
        self.table = {}
        self.hits = 0
        self.misses = 0

    def lookup(self, board_hash):
        """
        Retrieve a cached entry for board_hash, if any.

        Args:
            board_hash: int
        Returns:
            dict or None
        """
        entry = self.table.get(board_hash, None)
        if entry is not None:
            self.hits += 1
        else:
            self.misses += 1
        return entry

    def store(self, board_hash, score, depth, flag='EXACT'):
        """
        Cache an evaluated position.

        Only overwrites an existing entry if the new depth is at least as deep
        (deeper searches produce more accurate scores).

        Args:
            board_hash : int
            score      : int
            depth      : int
            flag       : str ('EXACT', 'LOWERBOUND', 'UPPERBOUND')
        """
        if board_hash not in self.table or depth >= self.table[board_hash]['depth']:
            self.table[board_hash] = {'score': score, 'depth': depth, 'flag': flag}

    def get_stats(self):
        """Return a human-readable hit-rate string (useful for the project report)."""
        total = self.hits + self.misses
        rate = (self.hits / total * 100) if total > 0 else 0.0
        return (
            f"TT size: {len(self.table)} | "
            f"hits: {self.hits} | misses: {self.misses} | "
            f"hit rate: {rate:.1f}%"
        )


def minimax_with_tt(board, depth, alpha, beta, maximizing_player,
                    tt, zobrist, current_hash=None):
    """
    Alpha-Beta Minimax enhanced with Transposition Table look-up and storage.

    Algorithm:
        1. Compute (or accept) the current Zobrist hash.
        2. TT look-up — if a sufficiently deep entry exists, return it immediately.
        3. Check base cases (terminal / depth 0).
        4. Recurse over center-ordered moves; compute each child's hash
           incrementally using zobrist.update_hash() — O(1), no deepcopy for hash.
        5. Store the result in the TT before returning.

    Args:
        board             : 6x7 2-D list
        depth             : int, remaining search depth
        alpha, beta       : float, pruning bounds
        maximizing_player : bool
        tt                : TranspositionTable instance
        zobrist           : ZobristHasher instance
        current_hash      : int or None (computed from scratch if None)

    Returns:
        tuple (best_column, best_score)
    """
    if current_hash is None:
        current_hash = zobrist.hash_board(board)

    # TT look-up
    entry = tt.lookup(current_hash)
    if entry is not None and entry['depth'] >= depth:
        return (None, entry['score'])

    valid_locations = get_ordered_moves(board)
    terminal = is_terminal_node(board)

    if terminal:
        if check_win(board, AI_PIECE):
            score = 1_000_000 + depth
        elif check_win(board, PLAYER_PIECE):
            score = -1_000_000 - depth
        else:
            score = 0
        tt.store(current_hash, score, depth)
        return (None, score)

    if depth == 0:
        leaf_score = score_position(board, AI_PIECE)
        tt.store(current_hash, leaf_score, depth)
        return (None, leaf_score)

    if maximizing_player:
        best_score = -math.inf
        best_col = valid_locations[0]

        for col in valid_locations:
            b_copy = copy.deepcopy(board)
            row = get_next_open_row(b_copy, col)
            drop_piece(b_copy, row, col, AI_PIECE)
            child_hash = zobrist.update_hash(current_hash, row, col, AI_PIECE)
            _, new_score = minimax_with_tt(
                b_copy, depth - 1, alpha, beta, False, tt, zobrist, child_hash
            )
            if new_score > best_score:
                best_score = new_score
                best_col = col
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        tt.store(current_hash, best_score, depth)
        return best_col, best_score

    else:
        best_score = math.inf
        best_col = valid_locations[0]

        for col in valid_locations:
            b_copy = copy.deepcopy(board)
            row = get_next_open_row(b_copy, col)
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            child_hash = zobrist.update_hash(current_hash, row, col, PLAYER_PIECE)
            _, new_score = minimax_with_tt(
                b_copy, depth - 1, alpha, beta, True, tt, zobrist, child_hash
            )
            if new_score < best_score:
                best_score = new_score
                best_col = col
            beta = min(beta, best_score)
            if alpha >= beta:
                break

        tt.store(current_hash, best_score, depth)
        return best_col, best_score


def get_best_move_with_tt(board, depth=5):
    """
    Entry point for the full AI (alpha-beta + transposition table).

    This is the function called by src/screens.py to replace random moves.

    Args:
        board : 6x7 2-D list
        depth : int (default 5)

    Returns:
        int: best column index for the AI to play
    """
    zobrist = ZobristHasher()
    tt = TranspositionTable()
    col, _ = minimax_with_tt(board, depth, -math.inf, math.inf, True, tt, zobrist)
    return col
