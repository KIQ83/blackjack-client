import socket
import json

HOST = '127.0.0.1'
PORT = 3000
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

print('Conectado')

def register(playerName):
	message = {}
	message['action'] = 'Register'
	message['player'] = {}
	message['player']['name'] = playerName
	messageJson = json.dumps(message)
	tcp.send (messageJson.encode())

def close():
	tcp.close()
