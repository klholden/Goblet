import game
import threading

evaluatedStates = {}
dictLock = threading.Lock()

def basicEvaluationFunction(gameState, currId):
	if gameState not in evaluatedStates.keys():
		evalState = _evalFunc(gameState)
		with dictLock:
			evaluatedStates[gameState] = evalState
	return evaluatedStates[gameState][currId]

def threadEval(gameState):
	if gameState not in evaluatedStates.keys():
		evalState = _evalFunc(gameState)
		with dictLock:
			evaluatedStates[gameState] = evalState


def _evalFunc(gameState):
	scores = [0 for player in range(game.PLAYERS)]
	endState = gameState.isEndState()

	for player in range(game.PLAYERS):
		if endState:
			if gameState.isGoalState(player):
				scores[player] = float('inf')
			else:
				scores[player] = -1 * float('inf')

		else:
			board = gameState.getBoard()
			peiceCount = 0
			for x in range(game.SIZE):
				for y in range(game.SIZE):
					for peice in range(game.SIZE):
						if board[x][y][peice] is player:
							peiceCount += 1

			inARow = [ 0 for x in range(game.SIZE) ]
			seeableCount = 0

			for count in gameState.vertCount[player]:
				inARow[count] += 1
				seeableCount += count
			scores[player] += seeableCount

			for count in gameState.horzCount[player]:
				inARow[count] += 1 
			for count in gameState.diagCount[player]:
				inARow[count] += 1 
		
			for i in range(game.SIZE):
				scores[player] += i ** inARow[i]

	return scores


