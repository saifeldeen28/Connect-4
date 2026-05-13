

## Connect Four
## Project Description
Connect Four is a two-player connection game. In this project, you will develop a Connect Four
game where the AI must determine the best column to drop a disc. The AI needs to look several
steps ahead to create winning lines ("four in a row") while blocking the opponent.
## Game Overview
The game is played on a vertical grid of 7 columns and 6 rows.
● Players alternate turns dropping discs into columns.
● The disc falls to the lowest available space within the column.
● The first player to form a horizontal, vertical, or diagonal line of four discs wins.
System Representation: A 2D array (6 rows × 7 columns).
## ●
## 1
→ Player 1 disc
## ●
## 2
→ Player 2 disc
## ●
## 0
→ Empty slot
## Required Features
Your program should be able to:
● Represent the 6×7 board and enforce gravity (discs fall down).
● Check for 4-in-a-row in all directions (horizontal, vertical, diagonal).
● Handle invalid moves (e.g., dropping a disc in a full column).
● Implement an AI opponent capable of planning moves.
● Display the board state after every move.
● Handle "Draw" conditions when the board is full.
## Required Algorithms
## Dynamic Programming Requirement
DP is applied here as Transposition Tables.
● Since Connect Four has a massive number of possible board states, storing every state
is memory-intensive.
● However, frequently visited states during the search tree can be cached.
● A hashing technique (like Zobrist hashing) should be used to store the evaluation score
of board positions encountered during the search.

● If the same position is reached via a different sequence of moves, the stored value is
retrieved, saving processing time.
## Greedy Requirement
Since the game tree is too deep to solve completely to the end, the AI relies on Greedy
Heuristics for non-terminal nodes. The AI must evaluate a board state by assigning a score
based on greedy features:
● Counting Potential: Give points for having 2 or 3 discs in a row.
● Center Preference: Assign higher points to discs in the center column (statistically leads
to more wins).
● Blocking: Penalize board states where the opponent has a winning threat. This guides
the AI to make "good enough" local decisions when the end of the game is not yet
visible.
AI Requirement
Students must implement a search strategy to play the game:
● Minimax with Depth Limit: Because the game tree is large, the AI searches only to a
fixed depth (e.g., 4 to 6 moves ahead).
● Alpha-Beta Pruning: This is mandatory for Connect Four to ensure the AI makes
decisions within a reasonable time. By pruning irrelevant branches, the AI can search
deeper in the same amount of time.
● Move Ordering: The AI should try moves in the center columns first (Greedy intuition),
as this increases the likelihood of pruning branches early (Alpha-Beta efficiency).
## Important Note
Students must clearly explain in their report:
● The Heuristic Function used to evaluate non-final states.
● How Alpha-Beta pruning improved the number of nodes explored (provide statistics).
● The difference in AI performance when increasing the search depth.
● How the Transposition Table (DP) was implemented (e.g., map of state → score).


Try hard test cases
## Board Width = 7, Board Height = 6
## Test Case 1:

Near Win Player 1 (X) has 3 horizontal discs at Row 0, Cols 0, 1, 2.
Player 2 (O) has random placements.
Goal: AI (Player 1) must detect the winning move at Col 3.
## Test Case 2:
Defensive Block Player 1 (X) is about to win vertically at Column 3 (3 discs stacked).
Player 2 (O) AI is to move.
Goal: AI must place disc at Column 3 to block the win.
## Test Case 3:
## Deep Strategy Empty Board.
AI plays first.
Goal: AI should place the first disc in the center column (Column 3) as it provides the highest
strategic advantage (Greedy/Heuristic).
