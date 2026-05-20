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
    def __init__(self):
        self.table = [
            [[0, random.getrandbits(64), random.getrandbits(64)]
             for _ in range(COLUMN_COUNT)]
            for _ in range(ROW_COUNT)
        ]

    def hash_board(self, board):
        h = 0
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                piece = board[r][c]
                if piece != EMPTY:
                    h ^= self.table[r][c][piece]
        return h

    def update_hash(self, current_hash, row, col, piece):
        return current_hash ^ self.table[row][col][piece]


class TranspositionTable:
    def __init__(self):
        self.table = {}
        self.hits = 0
        self.misses = 0

    def lookup(self, board_hash):
        entry = self.table.get(board_hash, None)
        if entry is not None:
            self.hits += 1
        else:
            self.misses += 1
        return entry

    def store(self, board_hash, score, depth, flag='EXACT'):
        if board_hash not in self.table or depth >= self.table[board_hash]['depth']:
            self.table[board_hash] = {'score': score, 'depth': depth, 'flag': flag}

    def get_stats(self):
        total = self.hits + self.misses
        rate = (self.hits / total * 100) if total > 0 else 0.0
        return (
            f"TT size: {len(self.table)} | "
            f"hits: {self.hits} | misses: {self.misses} | "
            f"hit rate: {rate:.1f}%"
        )


def minimax_with_tt(board, depth, alpha, beta, maximizing_player,
                    tt, zobrist, current_hash=None):
    if current_hash is None:
        current_hash = zobrist.hash_board(board)

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
    zobrist = ZobristHasher()
    tt = TranspositionTable()
    col, _ = minimax_with_tt(board, depth, -math.inf, math.inf, True, tt, zobrist)
    return col
