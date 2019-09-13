from Mancala_DQN import Agent
from Mancala_Rules import Board
import numpy as np
#from utils import plotLearning

class PlayAgent:
    def __init__(self, Board, PlayerType):
        self.Game = Board() #Remember to remove ()
        self.actionspace = [0,1,2,3,4,5]
        self.state = [self.Game.pockets[p] for p in self.Game.positions]
        self.PlayerType = PlayerType #Either A or B
        self.score = 0

    def act(self, agent_choice):
        if self.PlayerType == 'A':
            move = lambda choice: self.Game.Player_A(choice)
        else:
            move = lambda choice: self.Game.Player_B(choice)
        move(agent_choice)

        resultingState = [self.Game.pockets[p] for p in self.Game.positions]

        if self.PlayerType == 'A':
            reward = abs(self.score - self.Game.POINTS_A)
            self.score = self.Game.POINTS_A
        else:
            reward = abs(self.score - self.Game.POINTS_B)
            self.score = self.Game.POINTS_B
        

if __name__ == '__main__':
    env = Board()
    n_games = 500
    agent1 = Agent(gamma=0.99, epsilon=1.0,alpha=0.0005, input_dims=len(env.positions),
                 n_actions=6, mem_size=1000000, batch_size=64, epsilon_end=0.01)

    agent2 = Agent(gamma=0.99, epsilon=1.0,alpha=0.0005, input_dims=len(env.positions),
                 n_actions=6, mem_size=1000000, batch_size=64, epsilon_end=0.01)

    #agent.load_model() if you already have a model saved
    score = []
    eps_history = []

    for i in range(n_games):
        done = False
        score = 0
        observation = env
