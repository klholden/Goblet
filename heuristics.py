import game

evaluatedStates = {}

def basicEvaluationFunction(gameState, currId):
	if gameState not in evaluatedStates.keys():
		evaluatedStates[gameState] = _evalFunc(gameState)
	return evaluatedStates[gameState][currId]	


def _evalFunc(gameState):
	scores = [0 for player in range(game.PLAYERS)]
	endState = gameState.isEndState()

	inARow = []
	if not endState:
		inARow = _getInARow(gameState)

	for player in range(game.PLAYERS):
		if endState:
			if gameState.isGoalState(currId):
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
		
			for i in range(len(inARow[player])):
				scores[player] += i ** inARow[player][i]

	return scores

def _getInARow(gameState):
	simpleBoard = gameState._simplifyBoard()
	inARow = [[0 for x in range(game.SIZE)] for player in range(game.PLAYERS)]
	for x in range(game.SIZE):
		horizontalCount = [0 for player in range(game.PLAYERS)]
		verticalCount = [0 for player in range(game.PLAYERS)]
		for y in range(game.SIZE):
			horzId = simpleBoard[x][y][0]
			vertId = simpleBoard[y][x][0]

			if horzId in range(game.PLAYERS):
				horizontalCount[horzId] += 1
			if vertId in range(game.PLAYERS):
				verticalCount[vertId] += 1 
			
		for player in range(game.PLAYERS):	
			print verticalCount[player], horizontalCount[player]	
			inARow[player][verticalCount[player]] += 1
			inARow[player][horizontalCount[player]] += 1



	leftDiagCount = [0 for player in range(game.PLAYERS)]
	rightDiagCount = [0 for player in range(game.PLAYERS)]
	for i in range(game.SIZE):
		left = simpleBoard[i][i][0]
		right = simpleBoard[i][game.SIZE - 1 - i][0]

		if left in range(game.PLAYERS):
			leftDiagCount[left] += 1
		if right in range(game.PLAYERS):
			rightDiagCount[right] += 1


	for player in range(game.PLAYERS):
		inARow[player][leftDiagCount[player]] += 1
		inARow[player][rightDiagCount[player]] += 1

	return inARow
