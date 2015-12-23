Two AIs to play each other in the tic-tac-toe game of Goblet: an expectimax agent
that relies on a heuristic and a perceptron that is initialized with weights of 0.
The two are set up to play repeated games against each other. Every time the perceptron
loses its weights for all the actions taken in that round are reduced, while if it
wins then all of its weights are increased.

The expectimax agent is used to train the other agent.
