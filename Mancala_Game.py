import pygame
import numpy as np
import sys
import math


BLUE = (0,0,255)
BLACK = (0,0,0)
BURLYWOOD = (222,184,135)
PERU = (205,133,63)
ROSYBROWN = (188,143,143)
YELLOW = (255,255,0)
ROW_COUNT = 2
COLUMN_COUNT = 8


def draw_board(board):
    for c in range(COLUMN_COUNT):
        if c in [0,COLUMN_COUNT-1]:
                
                pygame.draw.rect(screen, BURLYWOOD, (c*SQUARESIZE, 0*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.rect(screen, BURLYWOOD, (c*SQUARESIZE, 1*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.ellipse(screen, PERU, pygame.Rect(c*SQUARESIZE+15,0*SQUARESIZE+SQUARESIZE+25, SQUARESIZE*(3/4),SQUARESIZE*2*(3/4)))
                pygame.display.set_caption('Stores') 
        else:
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, BURLYWOOD, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, PERU, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
                pygame.display.set_caption('Stores') 
    for c in range(COLUMN_COUNT):
        if c in [0,COLUMN_COUNT-1]:
                pygame.display.set_caption('Pockets') 
                pieces = board.get_pockets()[(board.get_positions()[c])]
                text = font.render(str(pieces), True, BLACK, ROSYBROWN)
                textRect = text.get_rect()
                textRect.center = ((c*SQUARESIZE+(c*100)+100) // 2,(SQUARESIZE+300) // 2)
                screen.blit(text, textRect)
        else:
            for r in range(ROW_COUNT):
                pygame.display.set_caption('Pockets') 
                
                if r == 0:
                    pieces = board.get_pockets()[(board.get_positions()[c])]
                    text = font.render(str(pieces), True, BLACK, ROSYBROWN)
                    textRect = text.get_rect()
                    textRect.center = ((c*SQUARESIZE+(c*100)+100) // 2,(r*SQUARESIZE+500) // 2)
                    screen.blit(text, textRect)
                elif r == 1:
                    pieces = board.get_pockets()[(board.get_positions()[14-c])]
                    text = font.render(str(pieces), True, BLACK, ROSYBROWN)
                    textRect = text.get_rect()
                    textRect.center = ((c*SQUARESIZE+(c*100)+100) // 2,(r*SQUARESIZE+200) // 2)
                    screen.blit(text, textRect)
                else:
                    continue
    for c in range(COLUMN_COUNT):
        if c in [0,COLUMN_COUNT-1]:
                pygame.display.set_caption('Pocket Name') 
                pieces = board.get_positions()[c]
                text = font.render(str(pieces), True, BLACK, ROSYBROWN)
                textRect = text.get_rect()
                textRect.center = ((c*SQUARESIZE+(c*100)+100) // 2,(SQUARESIZE+300-50) // 2)
                screen.blit(text, textRect)
        else:
            for r in range(ROW_COUNT):
                pygame.display.set_caption('Pocket Name') 
                
                if r == 0:
                    pieces = board.get_positions()[c]
                    text = font.render(str(pieces), True, BLACK, ROSYBROWN)
                    textRect = text.get_rect()
                    textRect.center = ((c*SQUARESIZE+(c*100)+100) // 2,(r*SQUARESIZE+450) // 2)
                    screen.blit(text, textRect)
                elif r == 1:
                    pieces = board.get_positions()[14-c]
                    text = font.render(str(pieces), True, BLACK, ROSYBROWN)
                    textRect = text.get_rect()
                    textRect.center = ((c*SQUARESIZE+(c*100)+100) // 2,(r*SQUARESIZE+150) // 2)
                    screen.blit(text, textRect)
                else:
                    continue
    pygame.display.update()         
Mancala = Board()
#Mancala_test(Mancala)
game_over = True #Change this to start
turn = 0

pygame.init()

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
font = pygame.font.Font('freesansbold.ttf', 16) 

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(Mancala)
pygame.display.update()
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
