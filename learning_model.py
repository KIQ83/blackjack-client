import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np
from math import log

from agent import agent

N_ACTIONS = 2

REWARD_STAND = 200
REWARD_HIT = -200
REWARD_OK = -100

E = 0.02

class LearningModel():

	def __init__(self, modelfile):
		self.modelfile = modelfile

		tf.reset_default_graph() #Clear the Tensorflow graph.

		self.myAgent = agent(lr=0.001) #Load the agent.
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


	def decide(self, playerSum, dealerSum, cardProbabilities):
		s = [playerSum, dealerSum]
		for prob in cardProbabilities:
			s.append(prob)

		# Choose either a random action or one from our network.
		e = E
		if np.random.rand(1) < e:
			# choosing randomly
			action = np.random.randint(N_ACTIONS)
		else:
			hotEncodedState = self.myAgent.convertToHotEncodedState(s)
			chose = self.sess.run(self.myAgent.output,feed_dict={self.myAgent.inputSums:[hotEncodedState[:28]], self.myAgent.inputCards:[hotEncodedState[28:]]})
			action = (not (not np.random.rand(1) < chose))

		return action

	def feed_reward(self, playerSum, dealerSum, cardProbabilities, finalPlayerSum, finalDealerSum, decidedToStand, gameEnded, isWinner):
		s = [playerSum, dealerSum]
		for prob in cardProbabilities:
			s.append(prob)

		if (gameEnded):
			if (isWinner):
				if (decidedToStand): # stand
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

				if (decidedToStand): # stand
					reward = -reward
		else:
			if (not decidedToStand): # hit
				reward = REWARD_OK

		#Update the network.
		hotEncodedState = self.myAgent.convertToHotEncodedState(s)
		feed_dict={self.myAgent.reward_holder:[reward], self.myAgent.inputSums:[hotEncodedState[:28]], self.myAgent.inputCards:[hotEncodedState[28:]]}
		_, ww = self.sess.run([self.myAgent.train_op, self.weights], feed_dict=feed_dict)

		self.save()

	def save(self):
		self.saver.save(self.sess, self.modelfile)
	
	def restore(self):
		self.saver.restore(self.sess, self.modelfile)
