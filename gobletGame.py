import game
import gameAgents

NUM_GAMES = 5


player1 = gameAgents.ExpectimaxAgent(0)
# player2 = gameAgents.ExpectimaxAgent(1)
player2 = gameAgents.PerceptronAgent(1)

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

		state.applyAction(playerId, action)
		playerId = (playerId + 1) % playerCount

	for i in range(playerCount):
		win = state.isGoalState(i)
		if win:
			print 'Player ' + str(i) + ' wins.'
			playerWins[i] += 1
		
		if player.getType() is 'Perceptron':
			player.classifyActions(win)

	print '\nGAME', gameCount
	print state.printState()

	print '\n'
	# print player2.getWeights()

for i in range(playerCount):
	print 'Player ' + str(i) + '(' + players[i].getType() + ') Wins:', playerWins[i] 






