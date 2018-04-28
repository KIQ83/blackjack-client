import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np

from agent import agent

N_STATES = 170
N_ACTIONS = 2

REWARD_LOSS = -20
REWARD_OK = 5
REWARD_WIN = 15

class learning_model():

	def __init__(self, modelfile="/tmp/model.ckpt"):
		self.modelfile = modelfile

		tf.reset_default_graph() #Clear the Tensorflow graph.

		self.myAgent = agent(lr=0.001, s_size=N_STATES, a_size=N_ACTIONS) #Load the agent.
		self.weights = tf.trainable_variables()[0] #The weights we will evaluate to look into the network.

		self.e = 0.1 #Set the chance of taking a random action.

		self.saver = tf.train.Saver()
		self.sess = tf.Session()
		try: 
			self.restore()
			print('#### restored')
		except:
			print('not restored')
			self.sess = tf.Session()
			self.sess.run(tf.initialize_all_variables())

		self.save()


	def decide(self, playerSum, dealerSum):
		s = [playerSum, dealerSum]

		# t = 0.5
		# Q_probs = self.sess.run(self.myAgent.Q_dist, feed_dict={self.myAgent.state_in:s, self.myAgent.temp:t})
		# action_value = np.random.choice(Q_probs[0], p=Q_probs[0])
		# return np.argmax(Q_probs[0] == action_value)

		# Choose either a random action or one from our network.
		if np.random.rand(1) < self.e:
			action = np.random.randint(N_ACTIONS)
		else:
			action = self.sess.run(self.myAgent.chosen_action,feed_dict={self.myAgent.state_in:s})

		return action

	def feed_reward(self, playerSum, dealerSum, finalPlayerSum, finalDealerSum, action, gameEnded, isWinner):
		s = [playerSum, dealerSum]

		if (gameEnded):
			if (isWinner):
				reward = REWARD_WIN
			else:
				diff = 1
				if (finalPlayerSum > 21):
					diff = finalPlayerSum - 21
				else:
					diff = finalDealerSum - finalPlayerSum
				reward = REWARD_LOSS*diff
				reward = REWARD_LOSS
		else:
			reward = REWARD_OK

		#Update the network.
		feed_dict={self.myAgent.reward_holder:[reward],self.myAgent.action_holder:[action],self.myAgent.state_in:s}
		_,ww = self.sess.run([self.myAgent.update, self.weights], feed_dict=feed_dict)

		self.save()

	def save(self):
		self.saver.save(self.sess, self.modelfile)
	
	def restore(self):
		self.saver.restore(self.sess, self.modelfile)
