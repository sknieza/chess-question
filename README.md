# A chess question project
As per description, program asks user to input a white piece, one out of two types. 
Then, program asks user to input 1-16 black pieces in the same format, entering at least
one piece and terminating input with entering 'done', if they choose to play
with fewer than 16 pieces.

Program then evaluates the user input and, based on the position of white piece and 
black piece(s), returns, which black pieces can be taken.

## Now, some assumptions to make about this program:
1. There are two submitted files. `chess_q.ipynb` notebook is provided only to illustrate the thinking the behind program code. Not all blocks work there as intended, some being revised in VSCode and not commited. The last block, however, is the acutal version of the code and should work fine.
2. The script `chess_submit.py` is the actual working program, and last notebook's block mirrors it.
3. In this scope, program accepts only `pawn` and `rook` as available white pieces
4. The input for both black and white pieces is expected in format `piece_name a1`, e.g., `rook f5`
5. Program assumes that user will follow chessboard guidelines, that is, will place figure within (a-h) and (1-8).

### That's about it for now. Happy plays! 
