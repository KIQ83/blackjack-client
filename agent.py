import tensorflow as tf
import tflearn
import tensorflow.contrib.slim as slim
import numpy as np

# number of neurons representing the player and dealer sum (with one hot encoding)
CARDS_SUM_WITH_HOT_ENCODING_NEURONS_COUNT = 28
# number of neurons representing the card probabilities
CARDS_PROBABILITY_NEURONS_COUNT = 13

# Agent is responsible defining our neural network
# He is the one describing how our input layer is build,
#  how each layer connects to the next, what loss and optimizer function we are using,
#  and how the rewards are applied to the network
class agent():

	def __init__(self, lr=0.001):
		# The first part of our input layer is composed by the player and dealer's sum, all hot encoded
		self.inputSums = tf.placeholder(tf.float32, (None, CARDS_SUM_WITH_HOT_ENCODING_NEURONS_COUNT), name='inputSums')
		# The second part of our input layer is composed by the cards probabilities
		self.inputCards = tf.placeholder(tf.float32, (None,CARDS_PROBABILITY_NEURONS_COUNT), name='inputCards')

		# The first part of the hidden layer is fully connected to the sums' input layer part
		# It has 180 neurons and ReLU as activation function
		hiddenHotEncoding = tf.layers.dense(self.inputSums, 180, activation=tf.nn.relu) 

		# The second part of the hidden layer is fully connected to the cards probabilities input layer part
		# It has 50 neurons and ReLU as activation function
		hiddenCards = tf.layers.dense(self.inputCards, 50, activation=tf.nn.relu) 

		# Here we are just constructing one layer that is the sum of the two parts
		hidden_1 = tflearn.layers.merge_ops.merge([hiddenHotEncoding, hiddenCards], 'concat', axis=1, name='Merge')

		# Our output layer is fully connected to the hidden layer, and it has sigmoid as activation function
		self.output = tf.layers.dense(hidden_1, 1, activation=tf.nn.sigmoid) 

		# The reward holder is used for updating the netwotk
		self.reward_holder = tf.placeholder(tf.float32, (None,), name='reward')

		# We applied a log of the output value multiplied by the reward as our loss function
		self.loss = -(tf.log(tf.clip_by_value(self.output, 1e-10,1.0)) * self.reward_holder)
		# We use AdamOptimizer to update the network
		optimizer = tf.train.AdamOptimizer(lr)
		# Here we are updating the gradients using our optimizer
		grads = tf.gradients(self.loss, tf.trainable_variables())
		grads, _ = tf.clip_by_global_norm(grads, 40) # gradient clipping
		grads_and_vars = list(zip(grads, tf.trainable_variables()))
		self.train_op = optimizer.apply_gradients(grads_and_vars)

	# Function that receives an array with sums and card probabilites, hot encode the sums and returns the array
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
# the maximum possible sum is 11 (when the dealer has an ACE) 
def hotEncodeDealerSum(dealerSum):
	encodedState = np.zeros(10)
	encodedState[dealerSum - 2] = 1
	return encodedState.tolist()
