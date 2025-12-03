import pygame

WIDTH, HEIGHT = 700, 600
# Init pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

exit()
