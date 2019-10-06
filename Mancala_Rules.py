import numpy as np
import sys
import math


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
        self.POINTS_A = 0.00
        self.POINTS_B = 0.00
        self.gameover = False
        self.winner_is_A = None
        self.game_state = np.array([self.pockets[p] for p in self.positions])
    def reset(self):
        self.pockets = {}
        self.is_player_A = True
        for p in self.positions:
            if p != 'BStore' and p != 'AStore':
                self.pockets[p] = 4
            else:
                self.pockets[p] = 0
        self.game_state = np.array([self.pockets[p] for p in self.positions])
        self.POINTS_A = 0.00
        self.POINTS_B = 0.00
        self.winner_is_A = None
        self.gameover = False
        return self.game_state
    def display(self):
        pocket_positions = [self.pockets[p] for p in self.positions[:6]]
        print('StoreB[{}]'.format(self.pockets['BStore']))
        print('    [ {} ] [ {} ] [ {} ] | [ {} ] [ {} ] [ {} ]    '.format(self.pockets['B6'],self.pockets['B5'],self.pockets['B4'],self.pockets['B3'],self.pockets['B2'],self.pockets['B1']))
        print('    [ {} ] [ {} ] [ {} ] | [ {} ] [ {} ] [ {} ]    '.format(self.pockets['A1'],self.pockets['A2'],self.pockets['A3'],self.pockets['A4'],self.pockets['A5'],self.pockets['A6']))
        print('StoreA[{}]'.format(self.pockets['AStore']))

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
        if self.pockets[pocket_name] == 0:
            return False
        if self.is_player_A:
            positions = self.positions_A
        else:
            positions = self.positions_B
        if pocket_name in positions[:6]:
            return True
        else:
            return False
    def move(self, pocket_name):
        if self.is_player_A:
            positions = self.positions_A
        else:
            positions = self.positions_B
        if self.can_start_here(pocket_name):
            pieces = self.pockets.get(pocket_name)
            self.pockets[pocket_name] = 0
            n = self.position_index(pocket_name)
            while pieces > 0:
                n = n + 1
                if n > len(positions)-1:
                    n = 0
                p_name = positions[n]
                is_tos = self.take_other_side(pieces,p_name)
                if is_tos == False:
                    self.pockets[p_name] = self.pockets[p_name] + 1
                pieces = pieces - 1
                if pieces == 0 and p_name in ['AStore','BStore'] and is_tos == False:
                    self.is_player_A = not self.is_player_A
            self.win_check()
            self.is_player_A = not self.is_player_A
            return 0.00
        else:
            return -1.00
    def Player_A(self, choice):
        positions = self.positions_A[:7]
        if choice in [0,1,2,3,4,5]:
            return self.move(positions[choice])
        else:
            return -1.00
    def Player_B(self, choice):
        positions = self.positions_B[:7]
        if choice in [0,1,2,3,4,5]:
            return self.move(positions[choice])
        else:
            return -1.00
    def out_of_rules_move(self, current_pocket, dest_pocket):
        pieces = self.pockets[current_pocket]
        self.pockets[dest_pocket] += pieces
        self.pockets[current_pocket] = 0

    def take_other_side(self, piece_count, dest_pocket):
        if self.is_player_A:
            positions = self.positions_A
        else:
            positions = self.positions_B
        inverse_n_dest = self.positions.index(dest_pocket) * -1
        if piece_count == 1 and self.pockets[dest_pocket] == 0 and self.pockets[self.positions[inverse_n_dest]] > 0 and dest_pocket in positions[:6]:
            piece = self.pockets[self.positions[inverse_n_dest]] + 1
            if self.is_player_A:
                self.pockets['AStore'] += piece
            else:
                self.pockets['BStore'] += piece
            self.pockets[self.positions[inverse_n_dest]] = 0
            return True
        return False
    def win_check(self):
        A_positions = [self.pockets[p] for p in self.positions_A[:6]]
        B_positions = [self.pockets[p] for p in self.positions_B[:6]]
        A_sum = sum(A_positions)
        B_sum = sum(B_positions)
        SUMS = [A_sum,B_sum]
        self.POINTS_A = float(self.pockets['AStore'])
        self.POINTS_B = float(self.pockets['BStore'])
        if 0 in SUMS:
            for pl in [self.positions_A, self.positions_B]:
                for p in pl[:6]:
                    if self.pockets[p] > 0:
                        self.out_of_rules_move(p, pl[6])
            if self.POINTS_A > self.POINTS_B:
                self.winner_is_A = True
            elif self.POINTS_B > self.POINTS_A:
                self.winner_is_A = False
            else:
                self.winner_is_A = None

            self.gameover = True
        #print(A_positions,B_positions)
        #print(A_sum,B_sum)
    def get_positions(self):
        return self.positions
    def get_pockets(self):
        return self.pockets
    def get_is_A(self):
        return self.is_player_A
    def gameover(self):
        return self.gameover

import numbers
class PlayAgent:
    def __init__(self, Board, PlayerType):
        self.Game = Board #Remember to remove ()
        self.actionspace = [0,1,2,3,4,5]
        self.state = self.Game.game_state
        self.PlayerType = PlayerType #Either A or B
        self.score = 0.00
        self.bot_score = 0.00
        self.gameover = False
    
    def reset(self):
        self.Game.reset()
        self.actionspace = [0,1,2,3,4,5]
        self.state = self.Game.game_state
        self.score = 0.00
        self.bot_score = 0.00
        self.gameover = self.Game.gameover

    def act(self, other, agent_choice):
        if isinstance(agent_choice, numbers.Integral):
            info = 0.00
            if self.PlayerType == 'A':
                move = lambda choice: self.Game.Player_A(choice)
            else:
                move = lambda choice: self.Game.Player_B(choice)
            validmove = move(agent_choice)
            if validmove == -1.00:
                #print('invalid',end='\r')
                info = -1.00
            else:
                #print('valid',end='\r')
                info = 0.00
            
            if self.PlayerType == 'A':
                reward = abs(self.score - self.Game.POINTS_A)
                self.score = self.Game.POINTS_A
                self.bot_score += reward
            else:
                reward = abs(self.score - self.Game.POINTS_B)
                self.score = self.Game.POINTS_B
                self.bot_score += reward
            
            self.state = self.Game.game_state
            self.end_check(other)
            #self.Game.display()
            self.gameover = self.Game.gameover
            return self.state, reward, self.gameover, info
        else:
            print('not an integer move')
    
    def end_check(self, other):
        if self.Game.gameover == True:
                if self.Game.winner_is_A and self.PlayerType == 'A':
                    self.score += 100.00
                    self.bot_score += 100.00
                    other.score -= 100.00
                    other.bot_score -= 100.00
                elif self.Game.winner_is_A and self.PlayerType == 'B':
                    self.score -= 100.00
                    self.bot_score -= 100.00
                    other.score += 100.00
                    other.bot_score += 100.00
                if not self.Game.winner_is_A and self.PlayerType == 'A':
                    self.score -= 100.00
                    self.bot_score -= 100.00
                    other.score += 100.00
                    other.bot_score += 100.00
                elif not self.Game.winner_is_A and self.PlayerType == 'B':
                    self.score += 100.00
                    self.bot_score += 100.00
                    other.score -= 100.00
                    other.bot_score -= 100.00
                elif self.Game.winner_is_A == None:
                    self.score -= 100.00
                    self.bot_score -= 100.00
                    other.score -= 100.00
                    other.bot_score -= 100.00
        else:
            pass

def Mancala_test(board):
    Mancala = board
    Mancala.display()
    Mancala.move('A1')
    Mancala.move('B2')
    Mancala.move('A3')
    Mancala.move('B4')
    Mancala.move('A5')
    Mancala.move('B6')
    Mancala.__init__()
    Mancala.move('A1')

    # print('next set')
    # Mancala.move('A1', True)
    # Mancala.move('A2', True)
    # Mancala.move('A3', True)
    # Mancala.move('A4', True)
    # Mancala.move('A5', True)
    # Mancala.move('A6', True)
    #Mancala.display()
    #Mancala.win_check()


#Mancala_test()
