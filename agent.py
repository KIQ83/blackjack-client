import tensorflow as tf
import tflearn
import tensorflow.contrib.slim as slim
import numpy as np

class agent():

	def __init__(self, lr=0.001, sumSize=28,cardsSize=13):

		self.inputSums = tf.placeholder(tf.float32, (None, sumSize), name='inputSums')
		self.inputCards = tf.placeholder(tf.float32, (None,cardsSize), name='inputCards')


		hiddenHotEncoding = tf.layers.dense(self.inputSums, 180, activation=tf.nn.relu) 
		hiddenCards = tf.layers.dense(self.inputCards, 50, activation=tf.nn.relu) 

		#hidden_1 = tf.concat([hiddenHotEncoding, hiddenCards], 1)
		hidden_1 = tflearn.layers.merge_ops.merge([hiddenHotEncoding, hiddenCards], 'concat', axis=1, name='Merge')

		#hidden_2 = tflearn.layers.merge_ops.merge(hidden_1, mode, axis=1, name='Merge')

		self.output = tf.layers.dense(hidden_1, 1, activation=tf.nn.sigmoid) 

		self.reward_holder = tf.placeholder(tf.float32, (None,), name='reward')


		self.loss = -(tf.log(tf.clip_by_value(self.output, 1e-10,1.0)) * self.reward_holder)
		optimizer = tf.train.AdamOptimizer(lr)
		grads = tf.gradients(self.loss, tf.trainable_variables())
		grads, _ = tf.clip_by_global_norm(grads, 40) # gradient clipping
		grads_and_vars = list(zip(grads, tf.trainable_variables()))
		self.train_op = optimizer.apply_gradients(grads_and_vars)

		#These lines established the feed-forward part of the network. The agent takes a state and produces an action.
		#self.state_in = tf.placeholder(shape=(2,), dtype=tf.int32)
		#state_in_OH = slim.one_hot_encoding(self.state_in, s_size)

		# hidden = slim.fully_connected(state_in_OH, 50, biases_initializer=None,activation_fn=tf.nn.relu, weights_initializer=tf.ones_initializer())
		#hidden2 = slim.fully_connected(hidden, 15, biases_initializer=None,activation_fn=tf.nn.relu, weights_initializer=tf.ones_initializer())

		#argmax = tf.argmax(self.output, 0)
		#self.chosen_action = self.output[argmax] # traz a prob de dar stand
		# self.temp = tf.placeholder(shape=[],dtype=tf.float32)
		# self.Q_dist = slim.softmax(self.output/self.temp)
 
		#The next six lines establish the training proceedure. We feed the reward and chosen action into the network
		#to compute the loss, and use it to update the network.
		#self.reward_holder = tf.placeholder(shape=[1], dtype=tf.float32)
		#self.action_holder = tf.placeholder(shape=[1], dtype=tf.int32)
		#self.responsible_weight = tf.slice(self.output, self.action_holder, [1])
		#self.loss = -(tf.log(tf.clip_by_value(self.responsible_weight,1e-10,1.0)) * self.reward_holder) # clip_by_value = nao dar nan
		#optimizer = tf.train.GradientDescentOptimizer(learning_rate=lr)		
		#self.update = optimizer.minimize(self.loss)

	def convertToHotEncodedState(self, state):
		return hotEncodePlayerSum(state[0]) + hotEncodeDealerSum(state[1]) + state[2:]

# for player sum, we have 17 possibilities
# the minimum possible sum is 4 (2 + 2)
def hotEncodePlayerSum(playerSum):
	encodedState = np.zeros(18)
	encodedState[playerSum - 4] = 1
	return encodedState.tolist()

# for player sum, we have 10 possibilities
# the minimum possible sum is 2 
def hotEncodeDealerSum(dealerSum):
	encodedState = np.zeros(10)
	encodedState[dealerSum - 2] = 1
	return encodedState.tolist()
