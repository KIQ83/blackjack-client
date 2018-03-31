import json

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

