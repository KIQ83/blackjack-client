import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np
from math import log

from agent import agent

# Number of possible actions to take
N_ACTIONS = 2

# Reward values for feeding the model
REWARD_STAND = 200
REWARD_HIT = -200
# Reward OK is used when the player HIT and hasn't got busted
REWARD_OK = -100

# This variable indicates the probability of completely ignoring the model and randomly deciding what to do
E = 0.02

# This is the class responsible for saving and restoring our trained model
# It has the responsibility of being an interface between our agent and our bot
# Provides decide function, for out bot to decide whether hitting or standing
# Provides feed_reward function, in order to update the network
class LearningModel():

	# We receive the name of the modelfile on the constructor, so we can train different models 
	def __init__(self, modelfile):
		self.modelfile = modelfile

		tf.reset_default_graph() 

		# Instantiating the agent with 0.001 as learning rate
		self.myAgent = agent(lr=0.001) 
		self.weights = tf.trainable_variables()[0] 

		self.saver = tf.train.Saver()
		self.sess = tf.Session()
		try: 
			# Restoring our trained model
			self.restore()
			print('MODEL RESTORED')
		except:
			# there is no model to restore, lets initialize from zero
			self.sess = tf.Session()
			self.sess.run(tf.initialize_all_variables())

		self.save()

	# Based on the playerSum, dealerSum and cardProbabilities, should decide what action to take
	def decide(self, playerSum, dealerSum, cardProbabilities):
		# storing variables on an array of state
		s = [playerSum, dealerSum]
		for prob in cardProbabilities:
			s.append(prob)

		# We may decide to ignore our trained model
		e = E
		if np.random.rand(1) < e:
			# choosing randomly
			action = np.random.randint(N_ACTIONS)
		else:
			# choosing based on our model
			# first, converting the state to a hot encoded state
			hotEncodedState = self.myAgent.convertToHotEncodedState(s)
			# deciding the action by running our model
			chose = self.sess.run(self.myAgent.output,feed_dict={self.myAgent.inputSums:[hotEncodedState[:28]], self.myAgent.inputCards:[hotEncodedState[28:]]})
			# the value returning is a probability of standing
			action = (not (not np.random.rand(1) < chose))

		return action

	# Informs an outcome of a decision to our model, so it can feed reward to the network
	def feed_reward(self, playerSum, dealerSum, cardProbabilities, finalPlayerSum, finalDealerSum, decidedToStand, gameEnded, isWinner):
		# storing variables on an array of state
		s = [playerSum, dealerSum]
		for prob in cardProbabilities:
			s.append(prob)

		if (gameEnded):
			if (isWinner):
				if (decidedToStand): 
					# game has ended, bot won by deciding to stand
					reward = REWARD_STAND
				else: 
					# game has ended, bot won by deciding to hit
					reward = REWARD_HIT
			else:
				# We use a different logic to calculate the reward when the bot loses
				# we decide a reward based on how far the bot was from winning
				diff = 1
				if (finalPlayerSum > 21):
					# on this case, the bot got busted. The diff is the amount of points he exceeded
					diff = finalPlayerSum - 21
				else:
					# on this case, the bot got sum lower than the dealer
					diff = abs(finalDealerSum - finalPlayerSum) + 1

				# we calculate reward = log(diff) * 300
				reward = round(log(diff, 10) * 300)

				if (decidedToStand): 
					# making reward negative, because we want to lower the probability of standing on this case
					reward = -reward
		else:
			if (not decidedToStand): 
				# Bot hit and did not get busted. We feed a small reward
				reward = REWARD_OK

		# Creating the hot encode state
		hotEncodedState = self.myAgent.convertToHotEncodedState(s)
		# Feeding the reward to the model
		feed_dict={self.myAgent.reward_holder:[reward], self.myAgent.inputSums:[hotEncodedState[:28]], self.myAgent.inputCards:[hotEncodedState[28:]]}
		_, ww = self.sess.run([self.myAgent.train_op, self.weights], feed_dict=feed_dict)

		self.save()

	# saves our model on a file
	def save(self):
		self.saver.save(self.sess, self.modelfile)
	
	# restores our model from a file
	def restore(self):
		self.saver.restore(self.sess, self.modelfile)
