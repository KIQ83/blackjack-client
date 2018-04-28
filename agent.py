import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np

class agent():

	def __init__(self, lr=0.001, s_size=170, a_size=2):
		#These lines established the feed-forward part of the network. The agent takes a state and produces an action.
		self.state_in = tf.placeholder(shape=(2,), dtype=tf.int32)
		state_in_OH = slim.one_hot_encoding(self.state_in, s_size)

		#hidden = slim.fully_connected(state_in_OH, 6, biases_initializer=None,activation_fn=tf.nn.relu, weights_initializer=tf.ones_initializer())
		#hidden2 = slim.fully_connected(hidden, 15, biases_initializer=None,activation_fn=tf.nn.relu, weights_initializer=tf.ones_initializer())
		output = slim.fully_connected(state_in_OH, a_size, biases_initializer=None, activation_fn=tf.nn.sigmoid, weights_initializer=tf.ones_initializer())
		self.output = tf.reshape(output, [-1])

		self.chosen_action = tf.argmax(self.output, 0)
		# self.temp = tf.placeholder(shape=[],dtype=tf.float32)
		# self.Q_dist = slim.softmax(self.output/self.temp)
 
		#The next six lines establish the training proceedure. We feed the reward and chosen action into the network
		#to compute the loss, and use it to update the network.
		self.reward_holder = tf.placeholder(shape=[1], dtype=tf.float32)
		self.action_holder = tf.placeholder(shape=[1], dtype=tf.int32)
		self.responsible_weight = tf.slice(self.output, self.action_holder,[1])
		self.loss = -(tf.log(self.responsible_weight) * self.reward_holder)
		optimizer = tf.train.GradientDescentOptimizer(learning_rate=lr)
		self.update = optimizer.minimize(self.loss)