import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.board import create_board, drop_piece, get_next_open_row
from src.transposition import get_best_move_with_tt

PLAYER_PIECE = 1
AI_PIECE = 2


def setup_board_from_moves(moves):
    """
    Build a board by replaying a sequence of (col, piece) moves in order.

    Args:
        moves: list of (col, piece) tuples

    Returns:
        board: 6x7 2-D list with all moves applied
    """
    board = create_board()
    for col, piece in moves:
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, piece)
    return board


# ---------------------------------------------------------------------------
# Test Case 1 — Near Win (Horizontal)
# ---------------------------------------------------------------------------

def test_near_win_horizontal():
    """
    Spec — Test Case 1:
        Player 1 (AI) has 3 horizontal discs at Row 0, Cols 0, 1, 2.
        Player 2 has discs at Cols 4 and 5 in Row 0.
        Expected: AI must detect the winning move at Col 3.

    Board (row 0 = bottom):
        Row 0: P1 P1 P1  .  P2 P2  .
    """
    moves = [
        (0, PLAYER_PIECE), (4, AI_PIECE),
        (1, PLAYER_PIECE), (5, AI_PIECE),
        (2, PLAYER_PIECE),
    ]
    board = setup_board_from_moves(moves)
    best_col = get_best_move_with_tt(board, depth=5)
    passed = (best_col == 3)
    print(f"TC1 Near-Win Horizontal:      {'PASS' if passed else 'FAIL'} "
          f"(AI chose col {best_col}, expected 3)")
    return passed


# ---------------------------------------------------------------------------
# Test Case 2 — Defensive Block (Vertical)
# ---------------------------------------------------------------------------

def test_defensive_block_vertical():
    """
    Spec — Test Case 2:
        Player 1 has 3 discs stacked vertically in Column 3 (rows 0, 1, 2).
        It is Player 2 (AI)'s turn.
        Expected: AI must block by placing in Column 3.

    Board (row 0 = bottom):
        Row 2:  .  .  . P1  .  .  .
        Row 1:  .  .  . P1  .  .  .
        Row 0:  . P2  . P1  .  .  .
    """
    moves = [
        (3, PLAYER_PIECE), (1, AI_PIECE),
        (3, PLAYER_PIECE),
        (3, PLAYER_PIECE),
    ]
    board = setup_board_from_moves(moves)
    best_col = get_best_move_with_tt(board, depth=5)
    passed = (best_col == 3)
    print(f"TC2 Defensive Block Vertical: {'PASS' if passed else 'FAIL'} "
          f"(AI chose col {best_col}, expected 3)")
    return passed


# ---------------------------------------------------------------------------
# Test Case 3 — Deep Strategy: First Move on Empty Board
# ---------------------------------------------------------------------------

def test_first_move_center():
    """
    Spec — Test Case 3:
        Empty board, AI plays first.
        Expected: AI should place the first disc in Column 3 (center).

    Validates that center preference in the heuristic and center-first
    move ordering both work correctly.
    """
    board = create_board()
    best_col = get_best_move_with_tt(board, depth=5)
    passed = (best_col == 3)
    print(f"TC3 First Move Center:        {'PASS' if passed else 'FAIL'} "
          f"(AI chose col {best_col}, expected 3)")
    return passed


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_all_tests():
    """Execute all three required test cases and report a summary."""
    print("=" * 55)
    print("  Connect Four — Required AI Test Cases")
    print("=" * 55)

    results = {
        "TC1  Near Win (Horizontal)":      test_near_win_horizontal(),
        "TC2  Defensive Block (Vertical)": test_defensive_block_vertical(),
        "TC3  First Move Center":          test_first_move_center(),
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
