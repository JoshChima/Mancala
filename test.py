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