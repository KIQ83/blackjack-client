import socket
import formatter

HOST = '127.0.0.1'
PORT = 3000

class Player:
	def __init__(self):
   		self.connect()

	def connect(self, host = HOST, port = PORT):
		self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		dest = (HOST, PORT)
		self.tcp.connect(dest)
		print('Conectado')

	def register(self, playerName = 'Jogador'):
		self.tcp.send(formatter.formatRegister(playerName))

	def hit(self):
		self.tcp.send(formatter.formatHit())

	def stand(self):
		self.tcp.send(formatter.formatStand())

	def close(self):
		self.tcp.close()
