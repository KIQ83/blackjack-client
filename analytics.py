import matplotlib.pyplot as plt
import pandas as pd

class RampAnalytics():
	def __init__(self, bot):
		self.bot = bot
		self.filename = 'models/bot' + str(bot) + '/win_rates_bot' + str(bot) + '.csv'
		self.read()

	def read(self):
		gamesDF = pd.read_csv(self.filename)
		self.sumGames(gamesDF, 'Rampa de jogos')

	def sumGames(self, games, name):
		sumTotal = 1
		sumWins = 0
		winsRate = []
		dealers = []
		countDealers = 0
		currentDealerID = 0
		for _, row in games.iterrows():
			win = row[3]
			dealerID = row[0]

			sumTotal += 1
			if (win == 'WIN'):
				sumWins += 1

			if (dealerID != currentDealerID):
				winsRate.append((sumWins / sumTotal) * 100)
				dealers.append(countDealers)

				countDealers += 1
				currentDealerID = dealerID
				
		
		plt.ylabel('Win rate')
		plt.xlabel('Dealers')
		plt.plot(dealers, winsRate)
		plt.savefig('models/bot' + str(self.bot) + '/' + name + '.png')
		plt.close()

GET_GAMES = 500

class CSVAnalytics():
	def __init__(self, bot):
		self.bot = bot
		self.filename = 'models/bot' + str(bot) + '/win_rates_bot' + str(bot) + '.csv'
		self.read()

	def read(self):
		gamesDF = pd.read_csv(self.filename)
		firstGames = gamesDF.head(GET_GAMES)
		lastGames = gamesDF.tail(GET_GAMES)

		self.sumGames(firstGames, 'Primeiros ' + str(GET_GAMES) + ' jogos')
		self.sumGames(lastGames, 'Últimos ' + str(GET_GAMES) + ' jogos')
	
	def sumGames(self, games, name):
		sumTotal = 1
		sumWins = 0
		winsRate = []
		yGames = []
		countGames = 0
		currentDealerID = 0
		for _, row in games.iterrows():
			win = row[3]
			dealerID = row[0]
			yGames.append(countGames)
			winsRate.append((sumWins / sumTotal) * 100)

			if (dealerID != currentDealerID):
				plt.plot(yGames, winsRate)

				sumTotal = 1
				sumWins = 0
				winsRate = []
				yGames = []
				countGames = 0
				currentDealerID = dealerID
			else:
				countGames += 1
				sumTotal += 1
				if (win == 'WIN'):
					sumWins += 1
		
		plt.ylabel('Win rate dos ' + name)
		plt.xlabel('Jogos')
		plt.savefig('models/bot' + str(self.bot) + '/' + name + '.png')
		plt.close()

