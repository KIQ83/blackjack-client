import matplotlib.pyplot as plt
import pandas as pd

class RealTimeAnalytics():
	def __init__(self):
		self.sumWins = 0
		self.sumTotal = 1
		self.countDealers = 0

		self.winsRate = []
		self.dealers = []

		plt.ion()
		self.fig = plt.figure()

		self.ax = self.fig.add_subplot(111)
		self.line, = self.ax.plot(self.dealers, self.winsRate, 'b-')
		self.ax.set_autoscaley_on(True)

	def changeDealer(self):
		self.countDealers += 1
		self.plot()

	def sumGame(self, win = False):
		self.sumTotal += 1
		if (win):
			self.sumWins += 1

	def plot(self):
		self.winsRate.append((self.sumWins / self.sumTotal) * 100)
		self.dealers.append(self.countDealers)
		self.line.set_xdata(self.dealers)
		self.line.set_ydata(self.winsRate)
		self.draw()

	def draw(self):
		self.ax.relim()
		self.ax.autoscale_view()
		self.fig.canvas.draw()
		self.fig.canvas.flush_events()
		plt.pause(0.5)

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

