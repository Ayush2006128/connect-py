import numpy as np
import pytest
from board import Board, ROW_COUNT, COLUMN_COUNT

def test_board_initialization():
    board = Board()
    assert board.board.shape == (ROW_COUNT, COLUMN_COUNT)
    assert np.all(board.board == 0)

def test_drop_piece():
    board = Board()
    row = 0
    col = 0
    piece = 1
    board.drop_piece(row, col, piece)
    assert board.board[row][col] == piece

def test_is_valid_location():
    board = Board()
    col = 0
    # Initially the column is empty, so it should be valid
    assert board.is_valid_location(col)
    
    # Fill the column
    for r in range(ROW_COUNT):
        board.drop_piece(r, col, 1)
        
    # Now it should be invalid (logic in board.py checks the top row)
    # Note: board.py's implementation of is_valid_location checks ROW_COUNT - 1
    # specifically: return self.board[ROW_COUNT - 1][col] == 0
    assert not board.is_valid_location(col)

def test_get_next_open_row():
    board = Board()
    col = 0
    
    # First drop should be at row 0
    assert board.get_next_open_row(col) == 0
    
    # Drop a piece
    board.drop_piece(0, col, 1)
    
    # Next drop should be at row 1
    assert board.get_next_open_row(col) == 1

def test_winning_move_horizontal():
    board = Board()
    piece = 1
    row = 0
    
    # Drop 3 pieces horizontally
    for c in range(3):
        board.drop_piece(row, c, piece)
    
    assert not board.winning_move(piece)
    
    # Drop the 4th piece
    board.drop_piece(row, 3, piece)
    assert board.winning_move(piece)

def test_winning_move_vertical():
    board = Board()
    piece = 1
    col = 0
    
    # Drop 3 pieces vertically
    for r in range(3):
        board.drop_piece(r, col, piece)
        
    assert not board.winning_move(piece)
    
    # Drop the 4th piece
    board.drop_piece(3, col, piece)
    assert board.winning_move(piece)

def test_winning_move_positive_diagonal():
    board = Board()
    piece = 1
    
    # Create a diagonal: (0,0), (1,1), (2,2), (3,3)
    # We need to stack pieces to get them to higher rows
    
    # Col 0: 1 piece
    board.drop_piece(0, 0, piece)
    
    # Col 1: 2 pieces (one dummy, one target)
    board.drop_piece(0, 1, 2)
    board.drop_piece(1, 1, piece)
    
    # Col 2: 3 pieces (two dummy, one target)
    board.drop_piece(0, 2, 2)
    board.drop_piece(1, 2, 2)
    board.drop_piece(2, 2, piece)
    
    # Col 3: 4 pieces (three dummy, one target)
    board.drop_piece(0, 3, 2)
    board.drop_piece(1, 3, 2)
    board.drop_piece(2, 3, 2)
    
    assert not board.winning_move(piece)
    
    board.drop_piece(3, 3, piece)
    assert board.winning_move(piece)

def test_winning_move_negative_diagonal():
    board = Board()
    piece = 1
    
    # Create a diagonal: (3,0), (2,1), (1,2), (0,3)
    
    # Col 0: 4 pieces (three dummy, one target)
    board.drop_piece(0, 0, 2)
    board.drop_piece(1, 0, 2)
    board.drop_piece(2, 0, 2)
    board.drop_piece(3, 0, piece)
    
    # Col 1: 3 pieces (two dummy, one target)
    board.drop_piece(0, 1, 2)
    board.drop_piece(1, 1, 2)
    board.drop_piece(2, 1, piece)
    
    # Col 2: 2 pieces (one dummy, one target)
    board.drop_piece(0, 2, 2)
    board.drop_piece(1, 2, piece)
    
    # Col 3: 1 piece
    
    assert not board.winning_move(piece)
    
    board.drop_piece(0, 3, piece)
    assert board.winning_move(piece)
