import socket
import formatter
import json
import struct
import time
from input import Input

HOST = '127.0.0.1'
PORT = 3000
MSGLEN = 2048

class Client(object):
	socket = None

	table = None

	def __del__(self):
		self.close()

	def connect(self, host = HOST, port = PORT):
		self.socket = socket.socket()
		self.socket.connect((host, port))
		self.socket.setblocking(0)
		return self

	def send(self, data):
		if not self.socket:
			raise Exception('You have to connect first before sending data')
		_send(self.socket, data)
		return self

	def recv(self):
		if not self.socket:
			raise Exception('You have to connect first before receiving data')
		message = _recv(self.socket)
		if (message == None):
			return None
		# checking if the message is a regular message, or if it is a Table message	
		if (message['type'] == 'Table'):
			# table messages are stored, but were not our goal
			self.table = message
			# we will still read the rest of the socket input
			self.recv()
		else:
			# emptying buffer anyway
			self.recv()
			# now returning the message that was read
			return message

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
	try:
		serialized = json.dumps(data)
	except (TypeError, ValueError):
		raise Exception('You can only send JSON-serializable data')
	socket.send(serialized.encode())

def _recv(socket):
	try:
		# read the length of the data, letter by letter until we reach EOL
		length = _readNumber(socket)
		if (length == None):
			return None

		try:
			deserialized = json.loads(socket.recv(length))
		except (TypeError, ValueError):
			raise Exception('Data received was not in JSON format')
		return deserialized
	except (BlockingIOError):
		return None

# Read one number, sent from the server as a string terminated with a '#'
def _readNumber(socket):
	numberStr = ''
	c = socket.recv(1).decode('utf8')
	while(c != '#' and c != ''):
		numberStr += c
		c = socket.recv(1).decode('utf8')

	# Nothing to Read
	if (numberStr == ''):
		raise BlockingIOError()

	return int(numberStr)


class Player:
	connected = False
	name = None

	def connect(self):
		if (self.connected == False):
			self.client = Client()
			self.client.connect()
			self.connected = True

	def register(self, playerName = 'Jogador'):
		self.connect()
		self.name = playerName
		self.client.send(formatter.formatRegister(playerName))
		return self.client.recv()

	def hit(self):
		self._ensureConnection()
		self.client.send(formatter.formatHit())
		return self.client.recv()

	def stand(self):
		self._ensureConnection()
		self.client.send(formatter.formatStand())
		return self.client.recv()
	
	def tableState(self, input = False):
		self._ensureConnection()
		self.client.recv()
		if (input):
			aux = Input(self.client.table, self.name)
			aux.format()
		return self.client.table

	def close(self):
		self._ensureConnection()
		self.client.close()
		self.connected = False
		self.client = None
		self.name = None

	def _ensureConnection(self):
		if (self.connected == False):
			print("Must register before performing this action")
			raise Exception('Invalid action')

