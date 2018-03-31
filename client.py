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
	except (TypeError, ValueError), e:
		raise Exception('You can only send JSON-serializable data')
	# send the length of the serialized data first
	socket.send('%d\n' % len(serialized))
	# send the serialized data
	socket.sendall(serialized)

def _recv(socket):
	# read the length of the data, letter by letter until we reach EOL
	length_str = ''
	char = socket.recv(1)
	while char != '\n':
		length_str += char
	char = socket.recv(1)
	total = int(length_str)
	# use a memoryview to receive the data chunk by chunk efficiently
	view = memoryview(bytearray(total))
	next_offset = 0
	while total - next_offset > 0:
		recv_size = socket.recv_into(view[next_offset:], total - next_offset)
	next_offset += recv_size
	try:
		deserialized = json.loads(view.tobytes())
	except (TypeError, ValueError), e:
		raise Exception('Data received was not in JSON format')
	print(deserialized)
	return deserialized

class Player:
	def __init__(self):
		self.client = Client()

	def start(self):
		self.client.connect()
		print('Conectado')

	def register(self, playerName = 'Jogador'):
		self.client.send(formatter.formatRegister(playerName))
		print(self.client.recv())

	def hit(self):
		self.client.send(formatter.formatHit())
		print(self.client.recv())

	def stand(self):
		self.client.send(formatter.formatStand())
		print(self.client.recv())
	
	def updateMe(self):
		print('me atualiza')
		self.client.send(formatter.formatUpdateMe())
		print(self.client.recv())
		print('me atualizou')

	def close(self):
		self.client.close()
