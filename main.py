import pygame
import sys
import math
import sound # Import sound module
from board import Board
from ui import draw_board, WIDTH, HEIGHT, SQUARESIZE, RADIUS, BLUE, YELLOW, BLACK # Import from ui.py

# --- Pygame Setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect π")
myfont = pygame.font.Font("assets/font.ttf", 65)

# --- Game Initialization ---
board_obj = Board()
game_over = False
turn = 0 # 0 for Player 1 (Blue), 1 for Player 2 (Yellow)

draw_board(screen, board_obj) # Initial board draw
sound.play_start_game_sound() # Play start game sound

while True: # Main game loop, runs continuously
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            # If game is over, a click restarts it
            board_obj = Board() # Reset board
            game_over = False
            turn = 0
            draw_board(screen, board_obj)
            sound.play_start_game_sound() # Play start game sound on restart
            pygame.display.update()
            continue # Skip rest of loop for this event

        if not game_over: # Only process game moves if game is not over
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, BLUE, (posx, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
                
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if board_obj.is_valid_location(col):
                    row = board_obj.get_next_open_row(col)
                    
                    if turn == 0:
                        board_obj.drop_piece(row, col, 1)
                        sound.play_drop_sound() # Play drop sound
                        if board_obj.winning_move(1):
                            label = myfont.render("Player 1 wins!!", 1, BLUE)
                            screen.blit(label, (40,10))
                            game_over = True
                            sound.play_win_sound() # Play win sound
                    else:               
                        board_obj.drop_piece(row, col, 2)
                        sound.play_drop_sound() # Play drop sound
                        if board_obj.winning_move(2):
                            label = myfont.render("Player 2 wins!!", 1, YELLOW)
                            screen.blit(label, (40,10))
                            game_over = True
                            sound.play_win_sound() # Play win sound
                    
                    board_obj.print_board()
                    draw_board(screen, board_obj)

                    turn += 1
                    turn = turn % 2
                else:
                    sound.play_invalid_move_sound() # Play invalid move sound
                    print("Invalid move. Try again.") # Optional: add a message for invalid moves
                
                if game_over:
                    # After game is over, keep the winning message on screen
                    pygame.display.update()
