import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np

class agent():

	def __init__(self, lr=0.001, s_size=15):

		self.input = tf.placeholder(tf.float32, (None,s_size), name='input')
		#self.action_holder = tf.placeholder(tf.float32, (None,), name='actions')
		self.reward_holder = tf.placeholder(tf.float32, (None,), name='reward')

		hidden_1 = tf.layers.dense(self.input, 50, activation=tf.nn.relu) 
		hidden_2 = tf.layers.dense(hidden_1, 30, activation=tf.nn.relu) 

		self.output = tf.layers.dense(hidden_2, 1, activation=tf.nn.sigmoid) 

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