EMPTY_SPOT = -1
FROM_UNUSED = -2
PLAYERS = 2
SIZE = 3

class GobletState:
	def __init__(self):
		self.size = SIZE
		self.players = PLAYERS
		self.board = [[[EMPTY_SPOT for x in range(self.size)] for x in range(self.size)] for x in range(self.size)]
		self.peices = [[self.size - 1 for x in range(self.size)] for x in range(self.players)]

		self.stable = False
		self.simple = []

	def __hash__(self):
		total_hash = 0
		for x in range(self.size):
			for y in range(self.size):
				for peice in range(self.size):
					total_hash += hash(x) + hash(self.size*y) + hash(self.size*self.size*peice)
		return hash(total_hash)

	def _setBoard(self, board):
		self.board = [[[board[x][y][p] for p in range(self.size)] for y in range(self.size)] for x in range(self.size)]
		self.stable = False

	def _setPeices(self, peices):
		self.peices = [[peices[p][y] for y in range(self.size)]  for p in range(self.players)]
		self.stable = False

	def getBoard(self):
		return self.board

	def getSize(self):
		return self.size

	def getPlayers(self):
		return self.players

	def getPeices(self):
		return self.peices

	def generateSucessor(self, agentId, action):
		new_state = GobletState()
		new_state._setBoard(self.board)
		new_state._setPeices(self.peices)
		new_state.applyAction(agentId, action)
		return new_state

	def getLegalActions(self, agentId):
		boardOpen = []
		boardVisible = []
		
		simplifiedBoard = self._simplifyBoard()
		for x in range(self.size):
			for y in range(self.size):
				player, size = simplifiedBoard[x][y]
				if player is not agentId and size + 1 < self.size:
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

		self.board[endPos[0]][endPos[1]][size] = agentId
		self.stable = False

	def getNumAgents(self):
		return self.players

	def getSize(self):
		return self.size

	def _simplifyBoard(self):
		if self.stable:
			return self.simple

		simplifiedBoard = [[(EMPTY_SPOT, EMPTY_SPOT) for x in range(self.size)] for x in range(self.size)]
		for x in range(self.size):
			for y in range(self.size):
				size = EMPTY_SPOT
				player = EMPTY_SPOT
				for peice in range(self.size):
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
		simplifiedBoard = self._simplifyBoard()

		# Check rows and cols
		for x in range(self.size):
			row_win = True
			col_win = True
			for y in range(self.size):
				row_win = row_win and simplifiedBoard[x][y][0] is agentId
				col_win = col_win and simplifiedBoard[y][x][0] is agentId
			if row_win or col_win:
				return True

		# Check diagonals
		right_win = True
		left_win = True
		for i in range(self.size):
			right_win = right_win and simplifiedBoard[i][i][0] is agentId
			left_win = left_win and simplifiedBoard[i][self.size - i - 1][0] is agentId

		return right_win or left_win

	def isEndState(self):
		simplifiedBoard = self._simplifyBoard()

		# Check rows and cols
		for x in range(self.size):
			row_win = simplifiedBoard[x][0][0] is not EMPTY_SPOT
			col_win = simplifiedBoard[0][x][0] is not EMPTY_SPOT
			for y in range(self.size):
				row_win = row_win and simplifiedBoard[x][y][0] is simplifiedBoard[x][0][0] 
				col_win = col_win and simplifiedBoard[y][x][0] is simplifiedBoard[0][x][0]
			if row_win or col_win:
				return True

		# Check diagonals
		right_win = simplifiedBoard[0][0][0] is not EMPTY_SPOT
		left_win = simplifiedBoard[0][self.size - 1][0] is not EMPTY_SPOT
		for i in range(self.size):
			right_win = right_win and simplifiedBoard[i][i][0] is simplifiedBoard[0][0][0]
			left_win = left_win and simplifiedBoard[i][self.size - i - 1][0] is simplifiedBoard[0][self.size - 1][0]

		return right_win or left_win 

	def toString(self):
		out = ''

		simplifiedBoard = self._simplifyBoard()
		for x in range(self.size):
			line = ''
			for y in range(self.size):
				player, size = simplifiedBoard[x][y]
				if player is EMPTY_SPOT:
					line += '-(-) '
				else:
					line += str(player) + '(' + str(size) + ') '
			out += line + '\n'

		for player in range(self.players):
			out += 'Player ' + str(player) + ' ' + str(self.peices[player]) + '\n'

		return out + '\n'

	def printState(self):
		print self.toString()