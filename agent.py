import tensorflow as tf
import tflearn
import tensorflow.contrib.slim as slim
import numpy as np

# Agent is responsible defining our neural network
# he is the one 
class agent():

	def __init__(self, lr=0.001, sumSize=28,cardsSize=13):

		self.inputSums = tf.placeholder(tf.float32, (None, sumSize), name='inputSums')
		self.inputCards = tf.placeholder(tf.float32, (None,cardsSize), name='inputCards')


		hiddenHotEncoding = tf.layers.dense(self.inputSums, 180, activation=tf.nn.relu) 
		hiddenCards = tf.layers.dense(self.inputCards, 50, activation=tf.nn.relu) 

		hidden_1 = tflearn.layers.merge_ops.merge([hiddenHotEncoding, hiddenCards], 'concat', axis=1, name='Merge')

		self.output = tf.layers.dense(hidden_1, 1, activation=tf.nn.sigmoid) 

		self.reward_holder = tf.placeholder(tf.float32, (None,), name='reward')

		self.loss = -(tf.log(tf.clip_by_value(self.output, 1e-10,1.0)) * self.reward_holder)
		optimizer = tf.train.AdamOptimizer(lr)
		grads = tf.gradients(self.loss, tf.trainable_variables())
		grads, _ = tf.clip_by_global_norm(grads, 40) # gradient clipping
		grads_and_vars = list(zip(grads, tf.trainable_variables()))
		self.train_op = optimizer.apply_gradients(grads_and_vars)

	def convertToHotEncodedState(self, state):
		return hotEncodePlayerSum(state[0]) + hotEncodeDealerSum(state[1]) + state[2:]

# for player sum, we have 18 possibilities 
# the minimum possible sum is 4 (2 + 2)
# the maximum possible sum is 21
def hotEncodePlayerSum(playerSum):
	encodedState = np.zeros(18)
	encodedState[playerSum - 4] = 1
	return encodedState.tolist()

# for dealer sum, we have 10 possibilities
# the minimum possible sum is 2 
def hotEncodeDealerSum(dealerSum):
	encodedState = np.zeros(10)
	encodedState[dealerSum - 2] = 1
	return encodedState.tolist()
