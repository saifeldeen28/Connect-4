# Person 5 — Test Cases + AI Integration
#
# TWO responsibilities:
#
#   A) Update src/screens.py so the computer player uses the real AI.
#      Find the line  (around line 388):
#          col = random.randint(0, COLUMN_COUNT - 1)
#      Replace the entire AI block with:
#          col = get_best_move_with_tt(board, depth=5)
#          if valid_location(board, col):
#              pygame.time.wait(500)
#              row = get_next_open_row(board, col)
#              drop_piece(board, row, col, 2)
#              ...
#      Also add at the top of screens.py:
#          from src.transposition import get_best_move_with_tt
#      And REMOVE the now-unused:
#          import random
#
#   B) Implement the three mandatory test cases below.
#      Run this file directly to verify: python tests/test_cases.py

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.board import create_board, drop_piece, valid_location, get_next_open_row, check_win
from src.transposition import get_best_move_with_tt

PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def setup_board_from_moves(moves):
    """
    Build a board by replaying a sequence of moves in order.

    Args:
        moves: list of (col, piece) tuples
               e.g. [(3, 1), (4, 2), (3, 1)] means:
                    P1 drops in col 3, P2 drops in col 4, P1 drops in col 3

    Returns:
        board: 6×7 2-D list with all moves applied
    """
    board = create_board()
    for col, piece in moves:
        # TODO: row = get_next_open_row(board, col)
        # TODO: drop_piece(board, row, col, piece)
        pass
    return board


# ---------------------------------------------------------------------------
# Test Case 1 — Near Win (Horizontal)
# ---------------------------------------------------------------------------

def test_near_win_horizontal():
    """
    Spec — Test Case 1:
        Player 1 (AI) has 3 horizontal discs at Row 0, Cols 0, 1, 2.
        Player 2 has discs elsewhere.
        Expected: AI must detect the winning move at Col 3.

    Suggested board setup (row 0 = bottom row):
        Row 0: P1 P1 P1  .  P2  .  .
        Row 1:  .  .  P2  .  .  .  .

    Move sequence to achieve this:
        (0, P1), (4, P2), (1, P1), (2, P2), (2, P1)
        → P1 occupies cols 0, 1, 2 in row 0 (with P2 at col 4 row 0, col 2 row 1)

    Returns:
        bool: True if the AI correctly chooses col 3
    """
    # TODO: moves = [(0, PLAYER_PIECE), (4, AI_PIECE), (1, PLAYER_PIECE),
    #                (2, AI_PIECE),     (2, PLAYER_PIECE)]
    # TODO: board = setup_board_from_moves(moves)
    # TODO: best_col = get_best_move_with_tt(board, depth=5)
    # TODO: passed = (best_col == 3)
    # TODO: print(f"TC1 Near-Win Horizontal: {'PASS' if passed else 'FAIL'} "
    #             f"(AI chose col {best_col}, expected 3)")
    # TODO: return passed
    pass


# ---------------------------------------------------------------------------
# Test Case 2 — Defensive Block (Vertical)
# ---------------------------------------------------------------------------

def test_defensive_block_vertical():
    """
    Spec — Test Case 2:
        Player 1 has 3 discs stacked vertically in Column 3 (rows 0, 1, 2).
        It is Player 2 (AI)'s turn.
        Expected: AI must block by placing in Column 3.

    Suggested board setup:
        Row 2:  .  .  . P1  .  .  .
        Row 1:  .  .  . P1  .  .  .
        Row 0:  . P2  . P1  .  .  .

    Move sequence:
        (3, P1), (1, P2), (3, P1), (3, P1)
        → P1 has rows 0,1,2 in col 3; P2 has one disc at col 1 row 0

    Note: get_best_move_with_tt() always thinks from AI_PIECE (piece 2) perspective.
          Make sure the board position correctly shows P2 (AI) needs to block.

    Returns:
        bool: True if the AI correctly chooses col 3
    """
    # TODO: moves = [(3, PLAYER_PIECE), (1, AI_PIECE),
    #                (3, PLAYER_PIECE), (3, PLAYER_PIECE)]
    # TODO: board = setup_board_from_moves(moves)
    # TODO: best_col = get_best_move_with_tt(board, depth=5)
    # TODO: passed = (best_col == 3)
    # TODO: print(f"TC2 Defensive Block Vertical: {'PASS' if passed else 'FAIL'} "
    #             f"(AI chose col {best_col}, expected 3)")
    # TODO: return passed
    pass


# ---------------------------------------------------------------------------
# Test Case 3 — Deep Strategy: First Move on Empty Board
# ---------------------------------------------------------------------------

def test_first_move_center():
    """
    Spec — Test Case 3:
        Empty board, AI plays first.
        Expected: AI should place the first disc in Column 3 (center).

    This tests that the heuristic center-preference and move ordering
    are both working correctly.

    Returns:
        bool: True if the AI correctly chooses col 3
    """
    # TODO: board = create_board()
    # TODO: best_col = get_best_move_with_tt(board, depth=5)
    # TODO: passed = (best_col == 3)
    # TODO: print(f"TC3 First Move Center: {'PASS' if passed else 'FAIL'} "
    #             f"(AI chose col {best_col}, expected 3)")
    # TODO: return passed
    pass


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_all_tests():
    """Execute all three required test cases and report a summary."""
    print("=" * 55)
    print("  Connect Four — Required AI Test Cases")
    print("=" * 55)

    results = {
        "TC1  Near Win (Horizontal)":       test_near_win_horizontal(),
        "TC2  Defensive Block (Vertical)":  test_defensive_block_vertical(),
        "TC3  First Move Center":           test_first_move_center(),
    }

    print()
    print("=" * 55)
    print("  Summary")
    print("=" * 55)
    all_passed = True
    for name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}]  {name}")
        if not passed:
            all_passed = False

    print("=" * 55)
    print(f"  Overall: {'ALL PASSED' if all_passed else 'SOME FAILED'}")
    print("=" * 55)
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
