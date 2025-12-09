from unittest.mock import MagicMock, patch

import pytest


# Test color constants
def test_color_constants():
    from ui import BLACK, BLUE, DARK_GREEN, GRAY, GREEN, ORANGE, WHITE, YELLOW

    # Verify colors are tuples of 3 integers (RGB)
    assert GREEN == (0, 128, 0)
    assert BLUE == (0, 0, 255)
    assert YELLOW == (255, 255, 0)
    assert BLACK == (0, 0, 0)
    assert WHITE == (255, 255, 255)
    assert GRAY == (50, 50, 50)
    assert ORANGE == (255, 165, 0)
    assert DARK_GREEN == (0, 100, 0)


def test_color_values_in_valid_range():
    from ui import BLACK, BLUE, DARK_GREEN, GRAY, GREEN, ORANGE, WHITE, YELLOW

    colors = [GREEN, BLUE, YELLOW, BLACK, WHITE, GRAY, ORANGE, DARK_GREEN]
    for color in colors:
        assert len(color) == 3, "Color should be RGB tuple"
        for component in color:
            assert 0 <= component <= 255, "Color component should be 0-255"


# Test board dimension constants
def test_board_dimensions():
    from ui import COLUMN_COUNT, HEIGHT, RADIUS, ROW_COUNT, SQUARESIZE, WIDTH

    assert SQUARESIZE == 100
    assert RADIUS == int(SQUARESIZE / 2 - 5)
    assert ROW_COUNT == 6
    assert COLUMN_COUNT == 7
    assert WIDTH == COLUMN_COUNT * SQUARESIZE
    assert HEIGHT == (ROW_COUNT + 1) * SQUARESIZE


def test_board_dimensions_consistency():
    from ui import COLUMN_COUNT, HEIGHT, RADIUS, ROW_COUNT, SQUARESIZE, WIDTH

    # Ensure radius fits within square
    assert RADIUS < SQUARESIZE / 2

    # Ensure width and height are correctly calculated
    assert WIDTH == 700  # 7 * 100
    assert HEIGHT == 700  # (6 + 1) * 100


# Test get_menu_choice function
def test_get_menu_choice_option1():
    from ui import get_menu_choice

    # Option 1 hitbox is y: 230-330
    assert get_menu_choice((350, 280)) == 1
    assert get_menu_choice((100, 230)) == 1
    assert get_menu_choice((600, 330)) == 1


def test_get_menu_choice_option2():
    from ui import get_menu_choice

    # Option 2 hitbox is y: 330-430
    assert get_menu_choice((350, 380)) == 2
    assert get_menu_choice((100, 331)) == 2
    assert get_menu_choice((600, 429)) == 2


def test_get_menu_choice_boundary():
    from ui import get_menu_choice

    # Test boundary between options
    assert get_menu_choice((350, 330)) == 1  # Upper boundary of option 1
    assert get_menu_choice((350, 331)) == 2  # Lower boundary starts option 2


def test_get_menu_choice_no_selection():
    from ui import get_menu_choice

    # Outside both hitboxes
    assert get_menu_choice((350, 100)) is None
    assert get_menu_choice((350, 500)) is None
    assert get_menu_choice((350, 229)) is None
    assert get_menu_choice((350, 431)) is None


def test_get_menu_choice_x_coordinate_ignored():
    from ui import get_menu_choice

    # X coordinate should not affect selection (full width clickable)
    assert get_menu_choice((0, 280)) == 1
    assert get_menu_choice((700, 280)) == 1
    assert get_menu_choice((0, 380)) == 2
    assert get_menu_choice((700, 380)) == 2


# Test get_smiley lazy loading
@patch("ui.pygame")
def test_get_smiley_lazy_loading(mock_pygame):
    # Reset the cached smiley
    import ui

    ui._smiley = None

    mock_image = MagicMock()
    mock_pygame.image.load.return_value.convert_alpha.return_value = mock_image
    mock_pygame.transform.scale.return_value = mock_image

    # First call should load the image
    result = ui.get_smiley()

    assert mock_pygame.image.load.called
    assert mock_pygame.transform.scale.called


@patch("ui.pygame")
def test_get_smiley_caching(mock_pygame):
    # Reset the cached smiley
    import ui

    ui._smiley = None

    mock_image = MagicMock()
    mock_pygame.image.load.return_value.convert_alpha.return_value = mock_image
    mock_pygame.transform.scale.return_value = mock_image

    # Call twice
    result1 = ui.get_smiley()
    result2 = ui.get_smiley()

    # Image should only be loaded once
    assert mock_pygame.image.load.call_count == 1
    assert result1 is result2


# Test draw_board function
@patch("ui.pygame")
def test_draw_board_calls_pygame_draw(mock_pygame):
    from unittest.mock import MagicMock

    from ui import draw_board

    mock_screen = MagicMock()
    mock_board = MagicMock()
    mock_board.board = [[0] * 7 for _ in range(6)]

    draw_board(mock_screen, mock_board)

    # Should call pygame.draw.rect and pygame.draw.circle
    assert mock_pygame.draw.rect.called
    assert mock_pygame.draw.circle.called
    assert mock_pygame.display.update.called


@patch("ui.pygame")
def test_draw_board_with_pieces(mock_pygame):
    from unittest.mock import MagicMock

    from ui import BLUE, YELLOW, draw_board

    mock_screen = MagicMock()
    mock_board = MagicMock()
    # Board with some pieces
    mock_board.board = [[0] * 7 for _ in range(6)]
    mock_board.board[0][0] = 1  # Player 1 piece
    mock_board.board[0][1] = 2  # Player 2 piece

    draw_board(mock_screen, mock_board)

    # Verify circles are drawn for pieces
    assert mock_pygame.draw.circle.called


# Test draw_menu function
@patch("ui.get_smiley")
@patch("ui.pygame")
def test_draw_menu_calls_pygame(mock_pygame, mock_get_smiley):
    from unittest.mock import MagicMock

    from ui import draw_menu

    mock_screen = MagicMock()
    mock_font = MagicMock()
    mock_pygame.font.Font.return_value = mock_font
    mock_font.render.return_value = MagicMock()
    mock_font.render.return_value.get_rect.return_value = MagicMock()

    mock_smiley = MagicMock()
    mock_get_smiley.return_value = mock_smiley

    draw_menu(mock_screen, "fake/font/path.ttf")

    # Should fill screen with black
    mock_screen.fill.assert_called()

    # Should load fonts
    assert mock_pygame.font.Font.called

    # Should draw line for decoration
    assert mock_pygame.draw.line.called

    # Should draw circles for player icons
    assert mock_pygame.draw.circle.called

    # Should update display
    assert mock_pygame.display.update.called


@patch("ui.get_smiley")
@patch("ui.pygame")
def test_draw_menu_renders_text(mock_pygame, mock_get_smiley):
    from unittest.mock import MagicMock

    from ui import draw_menu

    mock_screen = MagicMock()
    mock_font = MagicMock()
    mock_pygame.font.Font.return_value = mock_font

    mock_text_surface = MagicMock()
    mock_font.render.return_value = mock_text_surface
    mock_text_surface.get_rect.return_value = MagicMock()

    mock_smiley = MagicMock()
    mock_get_smiley.return_value = mock_smiley

    draw_menu(mock_screen, "fake/font/path.ttf")

    # Should render multiple text elements (title, options, subtitle, tagline)
    assert mock_font.render.call_count >= 5

    # Should blit text to screen
    assert mock_screen.blit.called
