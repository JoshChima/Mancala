from Mancala_Rules import Board, PlayAgent
from Mancala_DQN import Agent

import random


testGame = Board()
agent1 = Agent(gamma=0.99, epsilon=0.0,alpha=0.0005, input_dims=len(testGame.positions), n_actions=6, mem_size=1000000, batch_size=64, epsilon_end=0.01)
agent1.load_model()

player1 = PlayAgent(testGame,'A')
player2 = PlayAgent(testGame,'B')

scores_A = []
scores_B = []

for i in range(20):
    testGame.reset()
    player1.reset()
    player2.reset()
    while testGame.gameover == False:
        validmove = -1
        while validmove == -1:
            action = agent1.choose_action(testGame.game_state)
            observation_, reward, done, info = player1.act(action)
            agent1.remember(testGame.game_state, action, reward, observation_, done)
            validmove = info
        #testGame.display()
        player2.act((random.randint(0,6))-1)
        testGame.display()
    
    scores_A.append(PA_1.score)
    scores_B.append(PA_2.score)

    avg_score_A = np.mean(scores_A[max(0, i-100):(i+1)])
    avg_score_B = np.mean(scores_B[max(0, i-100):(i+1)])
    print('episode ', i)
    print('score A %.2f' % player1.score, 'average score A %.2f' % avg_score_A)
    print('score B %.2f' % player2.score, 'average score B %.2f' % avg_score_B)

import pygame
from Mancala_Game import draw_board
from Mancala_Rules import Board, PlayAgent
from Mancala_DQN import Agent
import numpy as np
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

    agent = Agent(gamma=0.99, epsilon=0.1,alpha=0.0005, input_dims=len(Mancala.positions),
                 n_actions=6, mem_size=1000000, batch_size=64, epsilon_end=0.01, agent_num='2')
    agent.load_model()
    PA = PlayAgent(Mancala, 'B')
    PA_R = PlayAgent(Mancala, 'A')
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

    draw_board(Mancala, ButtonStore)
    pygame.display.update()
    while not game_over:
        donzo = False
        observation = Mancala.game_state
        while Mancala.is_player_A == False and donzo == False:
            #validmove = -1
            #while validmove == -1:
            action = agent.choose_action(observation)
            observation_, reward, done, info = PA.act(PA_R, action)
            #PA_2.end_check(PA_R)
            agent.remember(observation, action, reward, observation_, done)
            #    validmove = info
            #env.display()
            draw_board(Mancala, ButtonStore)
            observation = observation_
            donzo = PA.Game.gameover
        while Mancala.is_player_B == False and donzo == False:
            validmove = -1
            while validmove == -1:
                PA_R.act((random.randint(0,6))-1)
            draw_board(Mancala, ButtonStore)
            donzo = PA_R.Game.gameover
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(Mancala.get_is_A())
                # if Mancala.get_is_A():
                #     validmove = -1
                #     while validmove == -1:
                #         action = agent.choose_action(observation)
                #         observation_, reward, done, info = PA.act(action)
                #         agent.remember(observation, action, reward, observation_, done)
                #         validmove = info
                #     draw_board(Mancala, ButtonStore)
                #     observation = observation_
                #     agent.learn()
                for label, button in ButtonStore.items():
                    if button.collidepoint(event.pos):
                        Mancala.move(label)
                        print(label)
                draw_board(Mancala, ButtonStore)
                game_over = Mancala.gameover
                if game_over:
                    pygame.time.wait(3000)