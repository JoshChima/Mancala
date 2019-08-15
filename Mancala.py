from collections import OrderedDict
import numpy as np
import pygame
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

class Board:
    def __init__(self):
        self.positions = ['BStore','A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'AStore', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6']
        self.positions_A = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'AStore', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6']
        self.positions_B = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'BStore', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6']
        self.pockets = {}
        self.is_player_A = True
        for p in self.positions:
            if p != 'BStore' and p != 'AStore':
                self.pockets[p] = 4
            else:
                self.pockets[p] = 0
    def display(self):
        print(self.pockets)
    def position_index(self, pocket_name):
        if self.is_player_A:
            positions = self.positions_A
        else:
            positions = self.positions_B
        for n in range(len(positions)):
            if positions[n] == pocket_name:
                return n
            else:
                continue
        return "This is not a pocket"
    
    def can_start_here(self, pocket_name):
        if self.is_player_A:
            positions = self.positions_A
        else:
            positions = self.positions_B
        if pocket_name in positions[:6]:
            return True
        else:
            return False
    def move(self, pocket_name, is_player_A):
        self.is_player_A = is_player_A
        if self.is_player_A:
            positions = self.positions_A
        else:
            positions = self.positions_B
        pieces = self.pockets.get(pocket_name)
        self.pockets[pocket_name] = 0
        n = self.position_index(pocket_name)
        while pieces > 0:
            n = n + 1
            if n > 12:
                n = 0
            p_name = positions[n]
            self.take_other_side(pieces,p_name)
            self.pockets[p_name] = self.pockets[p_name] + 1
            pieces = pieces - 1
        self.win_check()
    def out_of_rules_move(self, current_pocket, dest_pocket):
        pieces = self.pockets[current_pocket]
        self.pockets[dest_pocket] += pieces
        self.pockets[current_pocket] = 0

    def take_other_side(self, piece_count, dest_pocket):
        if piece_count == 1 and self.pockets[dest_pocket] == 0:
            inverse_n_dest = self.positions.index(dest_pocket) * -1
            piece = self.pockets[positions[inverse_n_dest]]
            if self.is_player_A:
                self.pockets['AStore'] += piece
            else:
                self.pockets['BStore'] += piece
            self.pockets[positions[inverse_n_dest]] = 0
    def win_check(self):
        A_positions = [self.pockets[p] for p in self.positions_A[:6]]
        B_positions = [self.pockets[p] for p in self.positions_B[:6]]
        A_sum = sum(A_positions)
        B_sum = sum(B_positions)
        SUMS = [A_sum,B_sum]
        if 0 in SUMS:
            for pl in [self.positions_A, self.positions_B]:
                for p in pl[:6]:
                    if self.pockets[p] > 0:
                        self.out_of_rules_move(p, pl[6])
        print(A_positions,B_positions)
        print(A_sum,B_sum)
    def get_positions(self):
        return self.positions
    def get_pockets(self):
        return self.pockets
    def get_is_A(self):
        return self.is_player_A

positions = ['BStore','A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'AStore', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6']
positions_A = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'AStore', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6']
positions_B = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'BStore', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6']
pockets = {}

def Mancala_test(board):
    Mancala.display()
    Mancala.move('A1', True)
    Mancala.move('A2', True)
    Mancala.move('A3', True)
    Mancala.move('A4', True)
    Mancala.move('A5', True)
    Mancala.move('A6', True)
    # Mancala.move('A1', True)
    # Mancala.move('A2', True)
    # Mancala.move('A3', True)
    # Mancala.move('A4', True)
    # Mancala.move('A5', True)
    # Mancala.move('A6', True)
    Mancala.display()
    Mancala.win_check()


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
                pygame.display.set_caption('Stores') 
                pieces = board.get_pockets()[(board.get_positions()[c])]
                text = font.render(str(pieces), True, BLACK, ROSYBROWN)
                textRect = text.get_rect()
                textRect.center = ((c*SQUARESIZE+(c*100)+100) // 2,(SQUARESIZE+300) // 2)
                screen.blit(text, textRect)
        else:
            for r in range(ROW_COUNT):
                pygame.display.set_caption('Stores') 
                
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
        
    
    # for c in range(COLUMN_COUNT):
    #     if c in [0,COLUMN_COUNT-1]:
    #             pygame.draw.rect(screen, BURLYWOOD, (c*SQUARESIZE, 0*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
    #             pygame.draw.rect(screen, BURLYWOOD, (c*SQUARESIZE, 1*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
    #             pygame.draw.ellipse(screen, PERU, pygame.Rect(c*SQUARESIZE+15,0*SQUARESIZE+SQUARESIZE+25, SQUARESIZE*(3/4),SQUARESIZE*2*(3/4)))

    #     else:
    #         for r in range(ROW_COUNT):
    #             pygame.draw.rect(screen, BURLYWOOD, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
    #             pygame.draw.circle(screen, PERU, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()         
Mancala = Board()
Mancala_test(Mancala)
game_over = False
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