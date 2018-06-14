import json

#Class responsible for formating messages to be sent to the game server
def formatRegister(playerName):
    return {
		'action': 'Register',
		'player': { 'name': playerName }
	}

def formatHit():
    return {
		'action': 'Hit'
	}

def formatStand():
    return {
		'action': 'Stand'
	}

def formatUpdateMe():
    return {
		'action': 'Update Me'
	}

