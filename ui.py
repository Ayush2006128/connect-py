import pygame

# --- Colors ---
GREEN = (0, 128, 0)  # Shade of green for the board
BLUE = (0, 0, 255)  # Player 1 chip color
YELLOW = (255, 255, 0)  # Player 2 chip color
BLACK = (0, 0, 0)  # Empty slot color
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
ORANGE = (255, 165, 0)  # Pyoneer accent color
DARK_GREEN = (0, 100, 0)

# --- Board Dimensions ---
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

ROW_COUNT = 6
COLUMN_COUNT = 7

WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE  # +1 for the piece drop area


# --- Functions ---
def draw_board(screen, board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen,
                GREEN,
                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE),
            )
            pygame.draw.circle(
                screen,
                BLACK,
                (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2),
                ),
                RADIUS,
            )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board.board[r][c] == 1:
                pygame.draw.circle(
                    screen,
                    BLUE,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )
            elif board.board[r][c] == 2:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )
    pygame.display.update()


def draw_menu(screen, font_path):
    """Draw the game mode selection menu."""
    screen.fill(BLACK)

    # Load fonts
    title_font = pygame.font.Font(font_path, 70)
    option_font = pygame.font.Font(font_path, 40)
    small_font = pygame.font.Font(font_path, 25)

    # Title
    title_text = title_font.render("CONNECT PY", True, GREEN)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 105))
    screen.blit(title_text, title_rect)

    # Decorative line
    pygame.draw.line(screen, GREEN, (100, 160), (WIDTH - 100, 160), 3)

    # Option 1: 2 Player
    option1_text = option_font.render("[1] vs Player", True, BLUE)
    option1_rect = option1_text.get_rect(center=(WIDTH // 2, 280))
    screen.blit(option1_text, option1_rect)

    # Player icons for option 1
    pygame.draw.circle(screen, BLUE, (WIDTH // 2 - 180, 280), 20)
    pygame.draw.circle(screen, YELLOW, (WIDTH // 2 + 180, 280), 20)

    # Option 2: vs AI (Pyoneer)
    option2_text = option_font.render("[2] vs Pyoneer", True, ORANGE)
    option2_rect = option2_text.get_rect(center=(WIDTH // 2, 380))
    screen.blit(option2_text, option2_rect)

    # AI icon for option 2
    pygame.draw.circle(screen, BLUE, (WIDTH // 2 - 180, 380), 20)
    pygame.draw.circle(screen, ORANGE, (WIDTH // 2 + 180, 380), 20)
    # Robot face on AI circle
    pygame.draw.circle(screen, BLACK, (WIDTH // 2 + 165, 377), 4)  # Left eye
    pygame.draw.circle(screen, BLACK, (WIDTH // 2 + 175, 377), 4)  # Right eye
    pygame.draw.line(
        screen, BLACK, (WIDTH // 2 + 173, 386), (WIDTH // 2 + 187, 386), 2
    )  # Mouth

    # Subtitle
    subtitle_text = small_font.render("Click or press 1/2 to select", True, GRAY)
    subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, 500))
    screen.blit(subtitle_text, subtitle_rect)

    # Pyoneer tagline
    tagline_text = small_font.render("Pyoneer: A Pythonic AI", True, DARK_GREEN)
    tagline_rect = tagline_text.get_rect(center=(WIDTH // 2, 550))
    screen.blit(tagline_text, tagline_rect)

    pygame.display.update()


def get_menu_choice(pos):
    """
    Determine which menu option was clicked.
    Returns 1 for 2-player, 2 for AI, or None if no option clicked.
    """
    x, y = pos

    # Option 1 hitbox (vs Player)
    if 230 <= y <= 330:
        return 1

    # Option 2 hitbox (vs Pyoneer)
    if 330 <= y <= 430:
        return 2

    return None
