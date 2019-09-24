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
    PA_1 = PlayAgent(Mancala, 'A')
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
            validmove = -1
            while validmove == -1:
                action = agent.choose_action(observation)
                observation_, reward, done, info = PA.act(PA_1, action)
                validmove = info
            #PA_2.end_check(PA_1)
            agent.remember(observation, action, reward, observation_, done)
            #env.display()
            draw_board(Mancala, ButtonStore)
            observation = observation_
            donzo = PA.Game.gameover
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