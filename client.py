import socket
import formatter
import json
import struct
import time

HOST = '127.0.0.1'
PORT = 3000
MSGLEN = 2048

class Client(object):
	socket = None

	def __del__(self):
		self.close()

	def connect(self, host = HOST, port = PORT):
		self.socket = socket.socket()
		self.socket.connect((host, port))
		return self

	def send(self, data):
		if not self.socket:
			raise Exception('You have to connect first before sending data')
		_send(self.socket, data)
		return self

	def recv(self):
		if not self.socket:
			raise Exception('You have to connect first before receiving data')
		return _recv(self.socket)

	def recv_and_close(self):
		data = self.recv()
		self.close()
		return data

	def close(self):
		if self.socket:
			self.socket.close()
			self.socket = None


## helper functions ##

def _send(socket, data):
	print(data)
	try:
		serialized = json.dumps(data)
	except (TypeError, ValueError):
		raise Exception('You can only send JSON-serializable data')
	socket.send(serialized.encode())

def _recv(socket):
	# read the length of the data, letter by letter until we reach EOL
	length = int(socket.recv(4))

	try:
		deserialized = json.loads(socket.recv(length))
	except (TypeError, ValueError):
		raise Exception('Data received was not in JSON format')
	return deserialized

class Player:
	def __init__(self):
		self.client = Client()
		self.client.connect()

	def register(self, playerName = 'Jogador'):
		self.client.send(formatter.formatRegister(playerName))
		return self.client.recv()

	def hit(self):
		self.client.send(formatter.formatHit())
		return self.client.recv()

	def stand(self):
		self.client.send(formatter.formatStand())
		return self.client.recv()
	
	def updateMe(self):
		print('me atualiza')
		self.client.send(formatter.formatUpdateMe())
		print(self.client.recv())
		print('me atualizou')

	def close(self):
		self.client.close()
