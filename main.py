import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import math
import sys
import time

import pygame

import ai  # Import Pyoneer AI
import sound  # Import sound module
from board import Board
from ui import (  # Import from ui.py
    BLACK,
    BLUE,
    HEIGHT,
    ORANGE,
    RADIUS,
    SQUARESIZE,
    WIDTH,
    YELLOW,
    draw_board,
    draw_menu,
    get_menu_choice,
)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# --- Remove logs ---
sys.stdin = os.devnull
sys.stderr = os.devnull

# --- Pygame Setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Py")
icon = pygame.image.load(resource_path("assets/connect-py-logo.png"))
pygame.display.set_icon(icon)

font_path = resource_path("assets/font.ttf")
myfont = pygame.font.Font(font_path, 65)


def show_menu():
    """Display the menu and return the selected game mode."""
    draw_menu(screen, font_path)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return False  # 2 Player mode
                elif event.key == pygame.K_2:
                    return True  # vs Pyoneer AI

            if event.type == pygame.MOUSEBUTTONDOWN:
                choice = get_menu_choice(event.pos)
                if choice == 1:
                    return False  # 2 Player mode
                elif choice == 2:
                    return True  # vs Pyoneer AI


def run_game(vs_ai):
    """Run a single game. Returns when game is over and player clicks."""
    board_obj = Board()
    game_over = False
    turn = 0  # 0 for Player 1 (Blue), 1 for Player 2/Pyoneer (Yellow)

    draw_board(screen, board_obj)
    sound.play_start_game_sound()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                # If game is over, a click returns to menu
                return

            if not game_over:
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                    posx = event.pos[0]
                    if turn == 0:
                        pygame.draw.circle(
                            screen, BLUE, (posx, int(SQUARESIZE / 2)), RADIUS
                        )
                    elif not vs_ai:  # Only show preview for Player 2 in 2P mode
                        pygame.draw.circle(
                            screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS
                        )
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Player's turn
                    if turn == 0 or not vs_ai:
                        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))

                        posx = event.pos[0]
                        col = int(math.floor(posx / SQUARESIZE))

                        if board_obj.is_valid_location(col):
                            row = board_obj.get_next_open_row(col)

                            if turn == 0:
                                board_obj.drop_piece(row, col, 1)
                                sound.play_drop_sound()
                                if board_obj.winning_move(1):
                                    label = myfont.render("Player 1 wins!!", 1, BLUE)
                                    screen.blit(label, (40, 10))
                                    game_over = True
                                    sound.play_win_sound()
                            else:
                                board_obj.drop_piece(row, col, 2)
                                sound.play_drop_sound()
                                if board_obj.winning_move(2):
                                    label = myfont.render("Player 2 wins!!", 1, YELLOW)
                                    screen.blit(label, (40, 10))
                                    game_over = True
                                    sound.play_win_sound()

                            if not game_over and board_obj.is_tie():
                                label = myfont.render("It's a Tie!!", 1, (255, 0, 0))
                                screen.blit(label, (40, 10))
                                game_over = True
                                sound.play_tie_sound()

                            draw_board(screen, board_obj)

                            turn += 1
                            turn = turn % 2
                        else:
                            sound.play_invalid_move_sound()

                        if game_over:
                            pygame.display.update()

        # Pyoneer AI's turn
        if not game_over and vs_ai and turn == 1:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
            pygame.display.update()

            # Small delay so AI doesn't feel instant
            time.sleep(0.5)

            col = ai.get_best_move(board_obj)

            if col is not None and board_obj.is_valid_location(col):
                row = board_obj.get_next_open_row(col)
                board_obj.drop_piece(row, col, 2)
                sound.play_drop_sound()

                if board_obj.winning_move(2):
                    label = myfont.render("Pyoneer wins!!", 1, ORANGE)
                    screen.blit(label, (40, 10))
                    game_over = True
                    sound.play_win_sound()

                if not game_over and board_obj.is_tie():
                    label = myfont.render("It's a Tie!!", 1, (255, 0, 0))
                    screen.blit(label, (40, 10))
                    game_over = True
                    sound.play_tie_sound()

                draw_board(screen, board_obj)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.display.update()


# --- Main Loop ---
while True:
    vs_ai = show_menu()
    run_game(vs_ai)
