from Mancala_DQN import Agent
from Mancala_Rules import Board, PlayAgent
import numpy as np
import pygame
from Mancala_Game import draw_board
import sys
import keras
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
import os


#import numba

#from utils import plotLearning
from tensorflow.python.client import device_lib
from keras import backend as K
K.tensorflow_backend._get_available_gpus()

config = tf.ConfigProto( device_count = {'GPU': 2 , 'CPU': 2} ) 
sess = tf.Session(config=config) 
keras.backend.set_session(sess)
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

    n_games = 1000
    env = Board()

    agent1 = Agent(gamma=0.99, epsilon=10.0,alpha=0.0005, input_dims=len(env.positions),
                 n_actions=6, mem_size=1000000, batch_size=64, epsilon_end=0.01, agent_num='1')
    agent2 = Agent(gamma=0.99, epsilon=10.0,alpha=0.0005, input_dims=len(env.positions),
                 n_actions=6, mem_size=1000000, batch_size=64, epsilon_end=0.01, agent_num='2')
    #agent1.load_model() #if you already have a model saved
    #agent2.load_model()

    PA_1 = PlayAgent(env, 'A')
    PA_2 = PlayAgent(env, 'B')

    scores_A = []
    scores_B = []
    eps_history_A = []
    eps_history_B = []

    pygame.init()


    SQUARESIZE = 100
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT+1) * SQUARESIZE
    font = pygame.font.Font('freesansbold.ttf', 16) 

    size = (width, height)

    RADIUS = int(SQUARESIZE/2 - 5)

    screen = pygame.display.set_mode(size)
    draw_board(env, ButtonStore)
    pygame.display.update()
    donzo = False
    for i in range(n_games):
        #score = 0

        observation = env.reset()
        PA_1.reset()
        PA_2.reset()
        donzo = False

        while donzo == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                draw_board(env, ButtonStore)
            #Agent 1
            while env.is_player_A == True and donzo == False:
                validmove = -1
                while validmove == -1:
                    action = agent1.choose_action(observation)
                    observation_, reward, done, info = PA_1.act(PA_2, action)
                    agent1.remember(observation, action, reward, observation_, done)
                    validmove = info
                #env.display()
                draw_board(env, ButtonStore)
                observation = observation_
                agent1.learn()
                donzo = PA_2.Game.gameover
            
            #Agent 2
            while env.is_player_A == False and donzo == False:
                validmove = -1
                while validmove == -1:
                    action = agent2.choose_action(observation)
                    observation_, reward, done, info = PA_2.act(PA_1, action)
                    agent2.remember(observation, action, reward, observation_, done)
                    validmove = info
                print('action:',action,' /reward:',reward, end='\r')
                #env.display()
                draw_board(env, ButtonStore)
                observation = observation_
                agent2.learn()
                donzo = PA_2.Game.gameover
        
        eps_history_A.append(agent1.epsilon)
        eps_history_B.append(agent2.epsilon)
        scores_A.append(PA_1.score)
        scores_B.append(PA_2.score)

        avg_score_A = np.mean(scores_A[max(0, i-100):(i+1)])
        avg_score_B = np.mean(scores_B[max(0, i-100):(i+1)])

        print('episode ', i)
        print('Last Player Turn Was A ', env.winner_is_A)
        print('score A %.2f' % PA_1.score, 'average score A %.2f' % avg_score_A)
        print('score B %.2f' % PA_2.score, 'average score B %.2f' % avg_score_B)
        
        #print(device_lib.list_local_devices())

        if i % 10 == 0 and i > 0:
            agent1.save_model()
            agent2.save_model()
            x = np.linspace(0, 10, 11)
            A = np.cumsum(scores_A, 0)
            B = np.cumsum(scores_B, 0)
            
            # sns.set()
            # plt.plot(x, A)
            # plt.plot(x, B)
            # #plt.legend('ABCDEF', ncol=2, loc='upper left')
            # plt.show()
    

