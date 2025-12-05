import pygame

# --- Colors ---
GREEN = (0, 128, 0)  # Shade of green for the board
BLUE = (0, 0, 255)    # Player 1 chip color
YELLOW = (255, 255, 0) # Player 2 chip color
BLACK = (0, 0, 0)     # Empty slot color

# --- Board Dimensions ---
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

ROW_COUNT = 6
COLUMN_COUNT = 7

WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE # +1 for the piece drop area

# --- Functions ---
def draw_board(screen, board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, GREEN, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            if board.board[r][c] == 1:
                pygame.draw.circle(screen, BLUE, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board.board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()
