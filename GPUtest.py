# import keras
# import tensorflow as tf
# import cudatoolkit

# from utils import plotLearning

# from keras import backend as K
# config = tf.ConfigProto( device_count = {'GPU': 1 , 'CPU': 1} ) 
# sess = tf.Session(config=config) 
# keras.backend.set_session(sess)
# print(K.tensorflow_backend._get_available_gpus()
# )
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
scores_A = [2,3,4,5,6,7,8,9,4,7]
scores_B = [3,6,5,3,2,1,5,7,9,8]
x = np.linspace(0, 10, 10)
A = np.cumsum(scores_A, 0)
B = np.cumsum(scores_B, 0)

sns.set()
plt.plot(x, A)
plt.plot(x, B)
plt.show()
