from Mancala_Rules import Board
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

style.use("ggplot")
env = Board()
SIZE = 10

epsilon = 0.9
EPS_DECAY = 0.9998
SHOW_EVERY = 3000

start_q_table = None # or filename

LEARNING_RATE = 0.1
DISCOUNT = 0.95

