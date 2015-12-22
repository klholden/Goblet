import game
import util
import random

class GameAgent:

	def __init__(self, agentId=0):
		self.agentId = agentId

	def getAction(self, gameState):
		pass

	def getType(self):
		pass


class ExpectimaxAgent(GameAgent):

	def __init__(self, agentId=0, depth=1):
		GameAgent.__init__(self, agentId)
		self.evaluatedStates = {}
		self.depth = depth

	def getAction(self, gameState):
		startDepth = 1
		return self._getMax(gameState, startDepth, self.agentId)

	def getType(self):
		return 'Expectimax'


	def _getMax(self, gameState, depth, currId):
		if depth > self.depth:
			return 'End State'

		# print 'depth', depth, 'currId', currId, '\n', gameState.toString()

		actionOptions = util.PriorityQueue()
		for action in gameState.getLegalActions(currId):
			next = gameState.generateSucessor(currId, action)
			nextDepth = depth + 1 if currId is self.agentId else depth
			nextId = (currId + 1) % gameState.getPlayers()

			nextAction = self._getMax(next, nextDepth, nextId)
			nextState = next
			if nextAction != 'End State' and nextAction != 'Terminal State':
				nextState = next.generateSucessor(nextId, nextAction)
			evaluation = self.evaluationFunction(nextState, currId)

			actionOptions.push((action, evaluation), evaluation * -1)

		if actionOptions.isEmpty():
			return 'Terminal State'

		actionOption, actionEval = actionOptions.pop()
		maxOptions = [ actionOption ]

		maxEval = actionEval
		while not actionOptions.isEmpty() and actionEval is maxEval:
			actionOption, actionEval = actionOptions.pop()

			if actionEval is maxEval:
				maxOptions.append(actionOption)
		return random.choice(maxOptions)

	def evaluationFunction(self, gameState, currId):
		if gameState in self.evaluatedStates.keys():
			return self.evaluatedStates[gameState]

		if gameState.isGoalState(self.agentId):
			self.evaluatedStates[gameState] = float('inf')
			return float('inf')
		if gameState.isEndState():
			self.evaluatedStates[gameState] = -1 * float('inf')
			return -1 * float('inf')

		board = gameState.getBoard()
		size = gameState.getSize()

		peiceCount = 0
		for x in range(size):
			for y in range(size):
				for peice in range(size):
					if board[x][y][peice] is currId:
						peiceCount += 1

		simpleBoard = gameState._simplifyBoard()
		inARow = [0 for x in range(gameState.getSize())]
		for x in range(size):
			for y in range(size):
				horizontalCount = 0
				verticalCount = 0
				if simpleBoard[x][y][0] is currId:
					horizontalCount += 1
				if simpleBoard[y][x][0] is currId:
					verticalCount += 1
				inARow[verticalCount] += 1
				inARow[horizontalCount] += 1

		leftDiagCount = 0
		rightDiagCount = 0
		for i in range(size):
			if simpleBoard[i][i][0] is currId:
				leftDiagCount += 1
			if simpleBoard[i][size - 1 - i][0] is currId:
				rightDiagCount += 1

		if leftDiagCount is len(inARow) or rightDiagCount is len(inARow):
			print 'DIAGPROB', leftDiagCount, rightDiagCount, len(inARow)
			print gameState.printState()
			print simpleBoard
			print 'end', gameState.isEndState()
			print 'game', gameState.isGoalState(currId)

		inARow[leftDiagCount] += 1
		inARow[rightDiagCount] += 1

		evaluatedScore = 0
		for i in range(len(inARow)):
			evaluatedScore += i * inARow[i]

		self.evaluatedStates[gameState] = evaluatedScore
		return evaluatedScore

class PerceptronAgent(GameAgent):

	def __init__(self, agentId=1):
		GameAgent.__init__(self, agentId)
		self.chosenActions = []
		self.legalFeatures = []

		self.corners = ['topL', 'topR', 'botL', 'botR']
		self.grouping = ['one', 'two', 'three', 'four']
		self.generateFeatures()

		self.weights = util.Counter()
		for label in self.legalFeatures:
			self.weights[label] = 0 #util.Counter()

	def getType(self):
		return 'Perceptron'

	def getWeights(self):
		return self.weights

	def generateFeatures(self):
		for player in range(2 + 1):
			for corner in self.corners:
				self.legalFeatures.append(corner + str(player))
			for count in range(8 + 1):
				for group in self.grouping:
					self.legalFeatures.append('P' + str(player) + group + str(count))

		for x in range(4):
			for y in range(4):
				for player in range(3):
					self.legalFeatures.append((x, y, player))

	def _findFeatures(self, gameState):
		simpleBoard = gameState._simplifyBoard()
		size = gameState.getSize()
		players = gameState.getPlayers()

		features = util.Counter()

		playersInARow = [[0 for x in range(size + 1)] for x in range(players + 1)]
		for x in range(size):
			inARowHor = [0 for x in range(players + 1)]
			inARowVert = [0 for x in range(players + 1)]
			for y in range(size):
				inARowHor[simpleBoard[x][y][0]] += 1
				inARowVert[simpleBoard[x][y][0]] += 1

			for player in range(players + 1):

				playersInARow[player][inARowHor[player]] += 1
				playersInARow[player][inARowVert[player]] += 1



		for player in range(players + 1):
			# Corner Features
			for corner in self.corners:
				x, y = 0, 0
				if corner[0] is 'b':
					x = size - 1
				if corner[3] is 'R':
					y = size - 1
				features[corner + str(player)] = 1 if simpleBoard[x][y][0] is player else 0
			
			# InARow Features
			for count in range(size * 2 + 1):
				for group in self.grouping:
					correctCount = playersInARow[player][self.grouping.index(group)] == count
					features['P' + str(player) + group + str(count)] = 1 if correctCount else 0

		# Possesion Features
		for x in range(4):
			for y in range(4):
				for player in range(3):
					features[(x, y, player)] = 1 if simpleBoard[x][y][0] is player else 0

		return features


	def getAction(self, gameState):
		allActions = gameState.getLegalActions(self.agentId)
		features = self._findFeatures(gameState)

		actions = self.classify([(features, allActions)])

		action = random.choice(actions)
		self.chosenActions.append((features, allActions))
		return action

	def classifyActions(self, win):
		for data in self.chosenActions:
			features, allActions = data

			for action in allActions:
				# If it is a win increase weights
				if win:
					self.weights[action] += features
				# If it is a loss decrease weights
				else:
					self.weights[action] -= features	
		self.chosenActions = []


	def classify(self, data):
		guesses = []

		for datum, legalMoves in data:
			vectors = util.Counter()
        	for l in legalMoves:
        		vectors[l] = self.weights * datum #changed from datum to datum[l]
			guesses.append(vectors.argMax())
		return guesses


