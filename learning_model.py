import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np
from math import log

from agent import agent

N_STATES = 170
N_ACTIONS = 1

# REWARD_LOSS = -200
# REWARD_OK = -500
# REWARD_WIN = 1500

REWARD_STAND = 200
REWARD_HIT = -200
REWARD_OK = -100

E = 0.02

class learning_model():

	def __init__(self, modelfile):
		self.modelfile = modelfile

		tf.reset_default_graph() #Clear the Tensorflow graph.

		self.myAgent = agent(lr=0.001, s_size=N_STATES, a_size=N_ACTIONS) #Load the agent.
		self.weights = tf.trainable_variables()[0] #The weights we will evaluate to look into the network.

		self.saver = tf.train.Saver()
		self.sess = tf.Session()
		try: 
			self.restore()
			print('MODEL RESTORED')
		except:
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
		e = E
		if np.random.rand(1) < e:
			print('escolha random')
			action = np.random.randint(N_ACTIONS)
		else:
			print('escolha treinada')
			chose = self.sess.run(self.myAgent.chosen_action,feed_dict={self.myAgent.state_in:s})
			print('prob stand:', chose)
			action = (not (not np.random.rand(1) < chose))

		print(action)
		return action

	def feed_reward(self, playerSum, dealerSum, finalPlayerSum, finalDealerSum, action, gameEnded, isWinner):
		s = [playerSum, dealerSum]

		print('---')
		print('action:', action)
		print('acabou:', gameEnded)
		print('ganhou:', isWinner)
		print('---')

		if (gameEnded):
			if (isWinner):
				if (action): # stand
					reward = REWARD_STAND
				else: # hit
					reward = REWARD_HIT
			else:
				diff = 1
				if (finalPlayerSum > 21):
					diff = finalPlayerSum - 21
				else:
					diff = abs(finalDealerSum - finalPlayerSum) + 1
				reward = round(log(diff, 10) * 300)

				if (action): # stand
					reward = -reward
				print('perdeu por', diff)
				print('reward', reward)
				# reward = REWARD_LOSS
		else:
			if (not action): # hit
				reward = REWARD_OK

		#Update the network.
		feed_dict={self.myAgent.reward_holder:[reward],self.myAgent.action_holder:[action],self.myAgent.state_in:s}
		_, ww = self.sess.run([self.myAgent.update, self.weights], feed_dict=feed_dict)

		print(ww)

		self.save()

	def save(self):
		self.saver.save(self.sess, self.modelfile)
	
	def restore(self):
		self.saver.restore(self.sess, self.modelfile)
