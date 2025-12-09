from unittest.mock import MagicMock

import numpy as np
import pytest

import ai
from ai import (
    AI_PIECE,
    COLUMN_COUNT,
    EMPTY,
    PLAYER_PIECE,
    ROW_COUNT,
    check_win,
    drop_piece_copy,
    get_best_move,
    get_next_open_row,
    get_valid_locations,
    is_terminal_node,
    minimax,
    score_position,
    score_window,
)


def create_empty_board():
    """Helper to create an empty board."""
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


def create_full_board():
    """Helper to create a full board (tie scenario)."""
    board = np.ones((ROW_COUNT, COLUMN_COUNT))
    # Alternate pieces to avoid wins
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            board[r][c] = 1 if (r + c) % 2 == 0 else 2
    return board


class TestGetValidLocations:
    def test_empty_board_all_columns_valid(self):
        board = create_empty_board()
        valid = get_valid_locations(board)
        assert valid == list(range(COLUMN_COUNT))

    def test_full_column_not_valid(self):
        board = create_empty_board()
        # Fill column 0
        for r in range(ROW_COUNT):
            board[r][0] = 1
        valid = get_valid_locations(board)
        assert 0 not in valid
        assert len(valid) == COLUMN_COUNT - 1

    def test_full_board_no_valid_locations(self):
        board = create_full_board()
        valid = get_valid_locations(board)
        assert valid == []

    def test_partially_filled_columns(self):
        board = create_empty_board()
        # Fill columns 0, 2, 4 completely
        for col in [0, 2, 4]:
            for r in range(ROW_COUNT):
                board[r][col] = 1
        valid = get_valid_locations(board)
        assert valid == [1, 3, 5, 6]


class TestGetNextOpenRow:
    def test_empty_column_returns_zero(self):
        board = create_empty_board()
        assert get_next_open_row(board, 0) == 0

    def test_partially_filled_column(self):
        board = create_empty_board()
        board[0][0] = 1
        board[1][0] = 2
        assert get_next_open_row(board, 0) == 2

    def test_almost_full_column(self):
        board = create_empty_board()
        for r in range(ROW_COUNT - 1):
            board[r][3] = 1
        assert get_next_open_row(board, 3) == ROW_COUNT - 1

    def test_full_column_returns_none(self):
        board = create_empty_board()
        for r in range(ROW_COUNT):
            board[r][0] = 1
        assert get_next_open_row(board, 0) is None


class TestDropPieceCopy:
    def test_does_not_modify_original(self):
        board = create_empty_board()
        original_sum = board.sum()
        new_board = drop_piece_copy(board, 0, 0, 1)
        assert board.sum() == original_sum
        assert new_board[0][0] == 1

    def test_returns_new_board_with_piece(self):
        board = create_empty_board()
        new_board = drop_piece_copy(board, 2, 3, AI_PIECE)
        assert new_board[2][3] == AI_PIECE

    def test_preserves_existing_pieces(self):
        board = create_empty_board()
        board[0][0] = PLAYER_PIECE
        new_board = drop_piece_copy(board, 1, 0, AI_PIECE)
        assert new_board[0][0] == PLAYER_PIECE
        assert new_board[1][0] == AI_PIECE


class TestCheckWin:
    def test_horizontal_win(self):
        board = create_empty_board()
        for c in range(4):
            board[0][c] = PLAYER_PIECE
        assert check_win(board, PLAYER_PIECE) is True
        assert check_win(board, AI_PIECE) is False

    def test_vertical_win(self):
        board = create_empty_board()
        for r in range(4):
            board[r][0] = AI_PIECE
        assert check_win(board, AI_PIECE) is True
        assert check_win(board, PLAYER_PIECE) is False

    def test_positive_diagonal_win(self):
        board = create_empty_board()
        for i in range(4):
            board[i][i] = PLAYER_PIECE
        assert check_win(board, PLAYER_PIECE) is True

    def test_negative_diagonal_win(self):
        board = create_empty_board()
        # (3,0), (2,1), (1,2), (0,3)
        for i in range(4):
            board[3 - i][i] = AI_PIECE
        assert check_win(board, AI_PIECE) is True

    def test_no_win_with_three_in_a_row(self):
        board = create_empty_board()
        for c in range(3):
            board[0][c] = PLAYER_PIECE
        assert check_win(board, PLAYER_PIECE) is False

    def test_no_win_empty_board(self):
        board = create_empty_board()
        assert check_win(board, PLAYER_PIECE) is False
        assert check_win(board, AI_PIECE) is False


class TestIsTerminalNode:
    def test_empty_board_not_terminal(self):
        board = create_empty_board()
        assert is_terminal_node(board) is False

    def test_full_board_is_terminal(self):
        board = create_full_board()
        assert is_terminal_node(board) is True

    def test_player_win_is_terminal(self):
        board = create_empty_board()
        for c in range(4):
            board[0][c] = PLAYER_PIECE
        assert is_terminal_node(board) is True

    def test_ai_win_is_terminal(self):
        board = create_empty_board()
        for r in range(4):
            board[r][0] = AI_PIECE
        assert is_terminal_node(board) is True


class TestScoreWindow:
    def test_four_in_a_row_scores_high(self):
        window = [AI_PIECE, AI_PIECE, AI_PIECE, AI_PIECE]
        assert score_window(window, AI_PIECE) == 100

    def test_three_with_empty_scores_medium(self):
        window = [AI_PIECE, AI_PIECE, AI_PIECE, EMPTY]
        assert score_window(window, AI_PIECE) == 5

    def test_two_with_two_empty_scores_low(self):
        window = [AI_PIECE, AI_PIECE, EMPTY, EMPTY]
        assert score_window(window, AI_PIECE) == 2

    def test_blocking_opponent_three(self):
        window = [PLAYER_PIECE, PLAYER_PIECE, PLAYER_PIECE, EMPTY]
        score = score_window(window, AI_PIECE)
        assert score < 0  # Should be negative for blocking

    def test_empty_window_scores_zero(self):
        window = [EMPTY, EMPTY, EMPTY, EMPTY]
        assert score_window(window, AI_PIECE) == 0

    def test_mixed_window_no_score(self):
        window = [AI_PIECE, PLAYER_PIECE, AI_PIECE, PLAYER_PIECE]
        assert score_window(window, AI_PIECE) == 0


class TestScorePosition:
    def test_empty_board_scores_zero(self):
        board = create_empty_board()
        assert score_position(board, AI_PIECE) == 0

    def test_center_column_preference(self):
        board = create_empty_board()
        center_col = COLUMN_COUNT // 2
        board[0][center_col] = AI_PIECE
        score = score_position(board, AI_PIECE)
        assert score > 0  # Center column should add points

    def test_winning_position_scores_high(self):
        board = create_empty_board()
        for c in range(4):
            board[0][c] = AI_PIECE
        score = score_position(board, AI_PIECE)
        assert score >= 100  # Should include the 100 for four in a row


class TestMinimax:
    def test_blocks_opponent_winning_move(self):
        board = create_empty_board()
        # Player has 3 in a row horizontally at row 0
        board[0][0] = PLAYER_PIECE
        board[0][1] = PLAYER_PIECE
        board[0][2] = PLAYER_PIECE
        # AI should block at column 3
        col, _ = minimax(board, 3, -float("inf"), float("inf"), True)
        assert col == 3

    def test_takes_winning_move(self):
        board = create_empty_board()
        # AI has 3 in a row horizontally at row 0
        board[0][0] = AI_PIECE
        board[0][1] = AI_PIECE
        board[0][2] = AI_PIECE
        # AI should take the win at column 3
        col, _ = minimax(board, 3, -float("inf"), float("inf"), True)
        assert col == 3

    def test_returns_valid_column(self):
        board = create_empty_board()
        col, _ = minimax(board, 3, -float("inf"), float("inf"), True)
        assert col in get_valid_locations(board)

    def test_terminal_state_returns_none_column(self):
        board = create_empty_board()
        # Create a win for AI
        for c in range(4):
            board[0][c] = AI_PIECE
        col, score = minimax(board, 3, -float("inf"), float("inf"), True)
        assert col is None
        assert score == 100000000  # AI win score


class TestGetBestMove:
    def test_returns_valid_column(self):
        # Create a mock board object
        board_obj = MagicMock()
        board_obj.board = create_empty_board()
        col = get_best_move(board_obj)
        assert col in range(COLUMN_COUNT)

    def test_takes_winning_move_with_board_object(self):
        board_obj = MagicMock()
        board_obj.board = create_empty_board()
        # AI has 3 in a row
        board_obj.board[0][0] = AI_PIECE
        board_obj.board[0][1] = AI_PIECE
        board_obj.board[0][2] = AI_PIECE
        col = get_best_move(board_obj)
        assert col == 3

    def test_blocks_player_win(self):
        board_obj = MagicMock()
        board_obj.board = create_empty_board()
        # Player has 3 in a row
        board_obj.board[0][0] = PLAYER_PIECE
        board_obj.board[0][1] = PLAYER_PIECE
        board_obj.board[0][2] = PLAYER_PIECE
        col = get_best_move(board_obj)
        assert col == 3
