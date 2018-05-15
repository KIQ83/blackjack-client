import matplotlib.pyplot as plt

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
		self.winsRate.append(self.sumWins / self.sumTotal)
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
