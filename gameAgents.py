import game
import heuristics
import util
import random

class GameAgent:

	def __init__(self, agentId=0):
		self.agentId = agentId

	def getAction(self, gameState):
		return gameState.getLegalActions(self.agentId)[-1]

	def getType(self):
		return 'GameAgent'

class InputAgent(GameAgent):
	def __init__(self, agentId=0):
		self.agentId = agentId

	def getAction(self, gameState):
		legalActions = gameState.getLegalActions(self.agentId)
		numActions = len(legalActions)

		print gameState.toString()
		for i in range(numActions):
			print i, legalActions[i]

		choice = input('Choose Action: ')
		choice = max(0, choice)
		choice = min(choice, numActions - 1)

		return legalActions[choice]

	def getType(self):
		return 'InputAgent'

class HeuristicAgent(GameAgent):

	def __init__(self, agentId=0, depth=1):
		GameAgent.__init__(self, agentId)
		self.evaluatedStates = {}

	def getAction(self, gameState):
		return self._getMax(gameState, startDepth, self.agentId)

	def getType(self):
		return 'Heuristic'


	def _getMax(self, gameState, currId):
		if depth > self.depth:
			return 'End State'

		# Maximize your moves and minimize oppoent's score (secondarily)
		actionOptions = util.PriorityQueue()
		opposingRanking
		for action in gameState.getLegalActions(currId):
			next = gameState.generateSucessor(currId, action)
			evaluation = heuristics.basicEvaluationFunction(next, currId)

			actionOptions.push((action, evaluation), evaluation * -1)

		if actionOptions.isEmpty():
			return 'Terminal State'

		maxOptions = self._getSameGroup(actionOptions)
		minOpponents = util.PriorityQueue()
		for option in maxOptions:
			evaluation = 0
			for player in game.PLAYERS:
				next = gameState.generateSucessor(currId, option)
				evaluation += heuristics.basicEvaluationFunction(next, player)
			minOpponents.push((option, evaluation), evaluation)

		return random.choice(_getSameGroup(minOpponents))

	def _getSameGroup(actionOptions):
		actionOption, actionEval = actionOptions.pop()
		maxOptions = [ actionOption ]

		maxEval = actionEval
		while not actionOptions.isEmpty() and actionEval is maxEval:
			actionOption, actionEval = actionOptions.pop()
			if actionEval is maxEval:
				maxOptions.append(actionOption)

		return maxOptions


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
			evaluation = heuristics.basicEvaluationFunction(nextState, currId)

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

class RandomAgent(GameAgent):
	def __init__(self, agentId=3):
		GameAgent.__init__(self, agentId)

	def getType(self):
		return 'Random'

	def getAction(self, gameState):
		return random.choice(gameState.getLegalActions(self.agentId))

class PerceptronAgent(GameAgent):

	def __init__(self, agentId=1, startFromDefault=True):
		GameAgent.__init__(self, agentId)
		self.chosenActions = []

		self.legalFeatures = []
		self.corners = ['topL', 'topR', 'botL', 'botR']
		self.grouping = ['one', 'two', 'three', 'four']
		self.generateFeatures()

		self.legalLabels = []
		self.generateLabels()

		defaultCounter = self.generateDefaultCounter()

		self.weights = {}
		for label in self.legalLabels:
			if startFromDefault:
				self.weights[label] = defaultCounter.copy()
			else: 
				self.weights[label] = util.Counter()

	def getType(self):
		return 'Perceptron'

	def getWeights(self):
		return self.weights

	def generateDefaultCounter(self):
		weight = util.Counter()
		for feature in self.legalFeatures:
			if feature[0] is '(':
				weight[feature] = int(feature[-2])
			elif feature[0] is 'P':
				coe = -1 if int(feature[1]) is not self.agentId else 1
				weight[feature] = coe * int(feature[-1]) * 100
			else:
				weight[feature] = 0
		return weight

	def generateLabels(self):
		for x in range(game.SIZE):
			for y in range(game.SIZE):
				for p in range(game.SIZE):
					self.legalLabels.append((game.FROM_UNUSED, (x, y), p))
					for x2 in range(game.SIZE):
						for y2 in range(game.SIZE):
							if x is not x2 or y is not y2:
								self.legalLabels.append(((x2, y2), (x, y), p))

	def generateFeatures(self):
		for player in range(game.PLAYERS):
			for corner in self.corners:
				self.legalFeatures.append(corner + str(player))
			for count in range(2 * game.SIZE + 1):
				for group in self.grouping:
					self.legalFeatures.append('P' + str(player) + group + str(count))

		for x in range(game.SIZE):
			for y in range(game.SIZE):
				for player in range(game.PLAYERS):
					self.legalFeatures.append((x, y, player))

	def _findFeatures(self, gameState):
		simpleBoard = gameState._simplifyBoard()
		size = gameState.getSize()
		players = gameState.getPlayers()

		features = util.Counter()

		playersInARow = [[0 for x in range(size + 1)] for x in range(players)]
		for x in range(size):
			inARowHor = [0 for x in range(players)]
			inARowVert = [0 for x in range(players)]
			for y in range(size):
				inARowHor[simpleBoard[x][y][0]] += 1
				inARowVert[simpleBoard[x][y][0]] += 1

			for player in range(players):

				playersInARow[player][inARowHor[player]] += 1
				playersInARow[player][inARowVert[player]] += 1



		for player in range(players):
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
		for x in range(game.SIZE):
			for y in range(game.SIZE):
				for player in range(game.PLAYERS):
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
		for features, legalMoves in data:
			vectors = util.Counter()
        	for l in legalMoves:
        		for feature in features.keys():
        			vectors[l] += self.weights[l][feature] * features[feature]
        		# vectors[l] = self.weights[l] * datum #changed from datum to datum[l]
			guesses.append(vectors.argMax())
		return guesses

	def printWeights(self):
		weights = self.getWeights()
		for action in weights.keys():
			if weights[action].totalCount() is not 0:
				print '\n', action, ':'
				for feature in weights[action].keys():
					val = weights[action][feature]
					if val is not 0:
						print feature, '->', weights[action][feature]


