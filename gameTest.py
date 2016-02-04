import game
import gameAgents

print 'Empty Board Tests'
state = game.GobletState()
state.printState()

legalActions1 = state.getLegalActions(0)
legalActions2 = state.getLegalActions(1)
if legalActions2 != legalActions1:
	print 'PROBLEM: LEGAL ACTIONS EMPTY STATE'
if len(legalActions1) is not game.SIZE**2:
	print 'PROBLEM: TOO MANY LEGAL ACTIONS'
	print len(legalActions1), 'legal actions', legalActions1

size = state.getSize()
players = state.getPlayers()

player2 = gameAgents.PerceptronAgent(1, False)


print 'Diagonal Board Tests'
diagBoard = [[[0 if y is x else game.EMPTY_SPOT for p in range(size)] for y in range(size)] for x in range(size)]
state._setBoard(diagBoard)
state._setPeices([[size - 1 if p is 0 else size - 2 for x in range(game.PEICE_COUNT)] for p in range(players)])
state.printState()


print 'Horizonatal Board Tests'
horBoard = [[[0 if x is 0 else game.EMPTY_SPOT for p in range(size)] for y in range(size)] for x in range(size)]
state._setBoard(horBoard)
state.printState()


print 'Vertical Board Tests'
vertBoard = [[[0 if y is 0 else game.EMPTY_SPOT for p in range(size)] for y in range(size)] for x in range(size)]
state._setBoard(vertBoard)
state.printState()

print 'Perceptrons Tests'
diagBoard = [[[(y % 2) if y is x else game.EMPTY_SPOT for p in range(size)] for y in range(size)] for x in range(size)]
state._setBoard(diagBoard)
state._setPeices([[size - 1 if x % 2 is 0 else size - 2 for x in range(size)] for p in range(players)])
state.printState()

allActions = state.getLegalActions(1)
features = player2._findFeatures(state)
actions = player2.classify([(features, allActions)])
print actions



