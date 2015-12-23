import game
import gameAgents

NUM_GAMES = 1000
PRINT_GAMES = False
PRINT_PRECEPT = True

# player1 = gameAgents.ExpectimaxAgent(0)
player1 = gameAgents.GameAgent(0)
# player1 = gameAgents.InputAgent(0)
# player2 = gameAgents.ExpectimaxAgent(1)
player2 = gameAgents.PerceptronAgent(1, False)
# player2.printWeights()

# player3 = gameAgents.RandomAgent(0)
# player3 = gameAgents.ExpectimaxAgent(0)

players = [ player1, player2 ]
playerCount = len(players)

playerWins = [0 for i in range(playerCount)]


for gameCount in range(1, 1 + NUM_GAMES):
	state = game.GobletState()
	playerId = 0

	while not state.isEndState():
		# print '\nTURN', playerId 
		# print state.printState()

		player = players[playerId]
		action = player.getAction(state)

		# print "Player", playerId, ":", action

		state.applyAction(playerId, action)
		playerId = (playerId + 1) % playerCount


	print '\nGAME', gameCount

	for i in range(playerCount):
		win = state.isGoalState(i)
		player = players[i]
		if win:
			print 'Player ' + str(i) + ' wins.'
			playerWins[i] += 1
		
		if player.getType() is 'Perceptron':
			# print 'UPDATING PERCEPTRON ' + str(i)
			player.classifyActions(win)

	if PRINT_GAMES:
		print state.toString()
		print '\n'
	
	"""
	weights = player2.getWeights()
	for action in weights.keys():
		if weights[action].totalCount() is not 0:
			print action, ":", weights[action]
	"""
if player2.getType() is 'Perceptron' and PRINT_PRECEPT:
	player2.printWeights()

for i in range(playerCount):
	print 'Player ' + str(i) + '(' + players[i].getType() + ') Wins:', playerWins[i] 






