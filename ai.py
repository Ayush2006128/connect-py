"""
Pyoneer - Connect 4 AI using Minimax with Alpha-Beta Pruning
A tiny, smart, and performant AI opponent.
"""

import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4

AI_PIECE = 2
PLAYER_PIECE = 1
EMPTY = 0

# Search depth (higher = smarter but slower)
DEPTH = 5


def get_valid_locations(board):
    """Get all columns that can accept a piece."""
    valid = []
    for col in range(COLUMN_COUNT):
        if board[ROW_COUNT - 1][col] == 0:
            valid.append(col)
    return valid


def get_next_open_row(board, col):
    """Find the next open row in a column."""
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
    return None


def drop_piece_copy(board, row, col, piece):
    """Drop a piece on a copy of the board (doesn't modify original)."""
    import numpy as np

    new_board = board.copy()
    new_board[row][col] = piece
    return new_board


def is_terminal_node(board):
    """Check if the game is over (win or tie)."""
    return (
        check_win(board, PLAYER_PIECE)
        or check_win(board, AI_PIECE)
        or len(get_valid_locations(board)) == 0
    )


def check_win(board, piece):
    """Check if a piece has won."""
    # Horizontal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Positive diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Negative diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True

    return False


def score_window(window, piece):
    """Score a window of 4 slots."""
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    # Block opponent
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    """Evaluate the entire board position."""
    score = 0

    # Favor center column
    center_col = list(board[:, COLUMN_COUNT // 2])
    center_count = center_col.count(piece)
    score += center_count * 3

    # Horizontal
    for r in range(ROW_COUNT):
        row_array = list(board[r, :])
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c : c + WINDOW_LENGTH]
            score += score_window(window, piece)

    # Vertical
    for c in range(COLUMN_COUNT):
        col_array = list(board[:, c])
        for r in range(ROW_COUNT - 3):
            window = col_array[r : r + WINDOW_LENGTH]
            score += score_window(window, piece)

    # Positive diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += score_window(window, piece)

    # Negative diagonal
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r - i][c + i] for i in range(WINDOW_LENGTH)]
            score += score_window(window, piece)

    return score


def minimax(board, depth, alpha, beta, maximizing_player):
    """
    Minimax algorithm with Alpha-Beta pruning.
    Returns (column, score) tuple.
    """
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if check_win(board, AI_PIECE):
                return (None, 100000000)
            elif check_win(board, PLAYER_PIECE):
                return (None, -100000000)
            else:  # Tie
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))

    if maximizing_player:
        value = -math.inf
        best_col = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board, col)
            new_board = drop_piece_copy(board, row, col, AI_PIECE)
            new_score = minimax(new_board, depth - 1, alpha, beta, False)[1]

            if new_score > value:
                value = new_score
                best_col = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cutoff

        return best_col, value

    else:  # Minimizing player
        value = math.inf
        best_col = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board, col)
            new_board = drop_piece_copy(board, row, col, PLAYER_PIECE)
            new_score = minimax(new_board, depth - 1, alpha, beta, True)[1]

            if new_score < value:
                value = new_score
                best_col = col

            beta = min(beta, value)
            if alpha >= beta:
                break  # Alpha cutoff

        return best_col, value


def get_best_move(board_obj):
    """
    Public API: Get Pyoneer's best move.
    Takes a Board object and returns the best column to play.
    """
    col, _ = minimax(board_obj.board, DEPTH, -math.inf, math.inf, True)
    return col
