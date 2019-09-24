import pygame
from Mancala_Game import draw_board
from Mancala_Rules import Board
import sys
import math


if __name__ == '__main__':

    BLUE = (0,0,255)
    BLACK = (0,0,0)
    BURLYWOOD = (222,184,135)
    PERU = (205,133,63)
    ROSYBROWN = (188,143,143)
    YELLOW = (255,255,0)
    ROW_COUNT = 2
    COLUMN_COUNT = 8
    ButtonStore = {}
    Mancala = Board()
    #Mancala_test(Mancala)
    game_over = False #Change this if game not stable start

    pygame.init()
    SQUARESIZE = 100
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT+1) * SQUARESIZE
    font = pygame.font.Font('freesansbold.ttf', 16) 

    size = (width, height)

    RADIUS = int(SQUARESIZE/2 - 5)

    screen = pygame.display.set_mode(size)

    draw_board(Mancala, ButtonStore)
    pygame.display.update()
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print(Mancala.get_is_A())
                #print(event.pos)
                for label, button in ButtonStore.items():
                    if button.collidepoint(event.pos):
                        Mancala.move(label)
                        print(label)
                Mancala.display()
                draw_board(Mancala, ButtonStore)
                game_over = Mancala.gameover
                if game_over:
                    pygame.time.wait(3000)
