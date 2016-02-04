import util

EMPTY_SPOT = -1
FROM_UNUSED = -2
PLAYERS = 2
SIZE = 4
PEICE_COUNT = SIZE - 1

class GobletState:
	def __init__(self):
		self.board = [[[EMPTY_SPOT for x in range(SIZE)] for x in range(SIZE)] for x in range(SIZE)]
		self.peices = [[PEICE_COUNT for x in range(PEICE_COUNT)] for x in range(PLAYERS)]

		self.stable = False
		self.simple = []

		self.horzCount = [[ 0 for x in range(SIZE) ] for p in range(PLAYERS) ]
		self.vertCount = [[ 0 for y in range(SIZE) ] for p in range(PLAYERS) ]
		self.diagCount = [[ 0 for d in range(2) ] for p in range(PLAYERS) ]

	def __hash__(self):
		total_hash = 0
		for x in range(SIZE):
			for y in range(SIZE):
				for peice in range(SIZE):
					total_hash += hash(x) + hash(SIZE*y) + hash(SIZE*SIZE*peice)
		return hash(total_hash)

	def _setBoard(self, board):
		self.board = [[[board[x][y][p] for p in range(SIZE)] for y in range(SIZE)] for x in range(SIZE)]
		self.stable = False

	def _setPeices(self, peices):
		self.peices = [[peices[p][y] for y in range(PEICE_COUNT)]  for p in range(PLAYERS)]
		self.stable = False

	def getBoard(self):
		return self.board

	def getSize(self):
		return SIZE

	def getPlayers(self):
		return PLAYERS

	def getPeices(self):
		return self.peices

	def generateSucessor(self, agentId, action):
		new_state = GobletState()
		new_state.board = util.copyList(self.board)
		new_state.peices = util.copyList(self.peices)
		new_state.horzCount = util.copyList(self.horzCount)
		new_state.vertCount = util.copyList(self.vertCount)
		new_state.diagCount = util.copyList(self.diagCount)
		new_state.applyAction(agentId, action)

		return new_state

	def getLegalActions(self, agentId):
		boardOpen = []
		boardVisible = []
		
		simplifiedBoard = self._simplifyBoard()
		for x in range(SIZE):
			for y in range(SIZE):
				player, size = simplifiedBoard[x][y]
				if player is not agentId and size + 1 < SIZE:
					boardOpen.append((size + 1, (x, y)))
				elif player is agentId:
					boardVisible.append((size, (x, y)))


		moves = []
		for sizePeice, posPeice in boardVisible:
			for sizeOpen, posOpen in boardOpen:
				if sizeOpen <= sizePeice:
					moves.append((posPeice, posOpen, sizePeice))

		for peice in self.peices[agentId]:
			for sizeOpen, posPeice in boardOpen:
				if sizeOpen <= peice:
					move = (FROM_UNUSED, posPeice, peice)
					if move not in moves:
						moves.append(move)
		return moves

	def applyAction(self, agentId, action):
		startPos, endPos, size = action

		if startPos is FROM_UNUSED:
			self.peices[agentId][self.peices[agentId].index(size)] -= 1

		else:
			self.board[startPos[0]][startPos[1]][size] = EMPTY_SPOT	

			revealedPlayer = EMPTY_SPOT
			for p in range(SIZE):
				player = self.board[startPos[0]][startPos[1]][p]
				if player is not EMPTY_SPOT:
					revealedPlayer = player

			self._updateRowCounts(startPos, agentId, False)

		self._updateRowCounts(endPos, agentId, True)

		self.board[endPos[0]][endPos[1]][size] = agentId
		self.stable = False

	def _updateRowCounts(self, pos, agentId, cover=True):
		increment = 1 if cover else -1

		coveredPlayer = EMPTY_SPOT
		for p in range(SIZE):
			player = self.board[pos[0]][pos[1]][p]
			if player is not EMPTY_SPOT:
				coveredPlayer = player

		if coveredPlayer is not EMPTY_SPOT:
			self.horzCount[coveredPlayer][pos[0]] -= increment
			self.vertCount[coveredPlayer][pos[1]] -= increment
			if pos[0] is pos[1]:
				self.diagCount[coveredPlayer][0] -= increment
			if pos[0] is SIZE - 1 - pos[1]:
				self.diagCount[coveredPlayer][1] -= increment

		self.horzCount[agentId][pos[0]] += increment
		self.vertCount[agentId][pos[1]] += increment
		if pos[0] is pos[1]:
			self.diagCount[agentId][0] += increment
		if pos[0] is SIZE - 1 - pos[1]:
			self.diagCount[agentId][1] += increment

	def getNumAgents(self):
		return PLAYERS

	def getSize(self):
		return SIZE

	def _simplifyBoard(self):
		if self.stable:
			return self.simple

		simplifiedBoard = [[(EMPTY_SPOT, EMPTY_SPOT) for x in range(SIZE)] for x in range(SIZE)]
		for x in range(SIZE):
			for y in range(SIZE):
				size = EMPTY_SPOT
				player = EMPTY_SPOT
				for peice in range(SIZE):
					currentPeice = self.board[x][y][peice]
					if currentPeice is not EMPTY_SPOT:
						player = currentPeice
						size = peice
				if player is not EMPTY_SPOT:
					simplifiedBoard[x][y] = (player, size)

		self.simple = simplifiedBoard
		self.stable = True
		return simplifiedBoard

	def isGoalState(self, agentId):
		for count in self.horzCount[agentId]:
			if count is 4:
				return True

		for count in self.vertCount[agentId]:
			if count is 4:
				return True

		for count in self.diagCount[agentId]:
			if count is 4:
				return True

		return False

	def isEndState(self):
		for player in range(PLAYERS):
			if self.isGoalState(player):
				return True
		return False

	def toString(self):
		out = ''

		simplifiedBoard = self._simplifyBoard()
		for x in range(SIZE):
			line = ''
			for y in range(SIZE):
				player, size = simplifiedBoard[x][y]
				if player is EMPTY_SPOT:
					line += '-(-) '
				else:
					line += str(player) + '(' + str(size) + ') '
			out += line + '\n'

		for player in range(PLAYERS):
			out += 'Player ' + str(player) + ' ' + str(self.peices[player]) + '\n'

		return out + '\n'

	def printState(self):
		print self.toString()
