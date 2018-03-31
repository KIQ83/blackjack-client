import json
from enum import Enum

class Actions(Enum):
    REGISTER = 0
    HIT = 1
    STAND = 2

def formatRegister(playerName):
    message = {}
    message['action'] = 'Register'
    message['player'] = {}
    message['player']['name'] = playerName
    return json.dumps(message)

def formatHit():
    message = {}
    message['action'] = 'Hit'
    return json.dumps(message)

def formatStand():
    message = {}
    message['action'] = 'Stand'
    return json.dumps(message)

