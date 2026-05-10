---
name: Connect 4 project structure
description: Module layout after refactoring monolithic connect4.py into src/ package
type: project
---

Refactored from single connect4.py into a src/ package. Entry point is connect4.py (thin shell). Images moved to assets/.

Structure:
- connect4.py — entry point only (imports src.display then calls main_menu)
- assets/ — dark_bg.jpg, main_menu_bg.png, rules.jpeg
- src/__init__.py — empty
- src/constants.py — pure Python constants (ROW_COUNT, COLUMN_COUNT, SQUARE_SIZE, RADIUS, width, height, size, ORANGE)
- src/display.py — calls pygame.init() at module level; exports screen, surface, font, rules, main_bg, dark_bg
- src/board.py — pure game logic, zero pygame imports (create_board, drop_piece, valid_location, get_next_open_row, check_win, check_draw, print_board)
- src/renderer.py — draw_board, pause_page
- src/persistence.py — check_name (returns bool, str tuple), save_game, load_game
- src/screens.py — all UI screens (kept together due to mutual recursive calls)

**Why:** All screens call each other recursively (name_page→check_game→game_mode→play_page→win_page→main_menu). Splitting screens into multiple files would create circular imports with no benefit.

**How to apply:** board.py can be unit-tested in isolation. display.py is the pygame init boundary — import it first.
