import random
import game
import agent
import alpha_beta_agent as aba
import first_best_agent

# Set random seed for reproducibility

#seed = random.choice(range(1000))
#seed = 316 #solved
seed = 899 #TODO random wins in seed 899, resolve. Is it going deep instead of broad?,
#TODO we need to change the code to do a-b search, not DFS?
# we need to trace the steps of the search to see why it doesn't block random from winning
random.seed(seed)
print(seed)

#
# Random vs. Random
#
g = game.Game(7,  # width
              6,  # height
              4,  # tokens in a row to win
              agent.RandomAgent("random1"),  # player 1
              agent.RandomAgent("random2"))  # player 2

#
# Human vs. Random
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               agent.RandomAgent("random"))        # player 2


# Random vs. AlphaBeta

g = game.Game(7,  # width
              6,  # height
              4,  # tokens in a row to win
              agent.RandomAgent("random"),         # player 1
              aba.AlphaBetaAgent("alphabeta", 4))  # player 2

#
# Human vs. AlphaBeta
#
#g = game.Game(7,  # width
#              6,  # height
#              4,  # tokens in a row to win
#              agent.InteractiveAgent("human"),  # player 1
#              aba.AlphaBetaAgent("alphabeta", 4))  # player 2

#
# Human vs. Human
#
# g = game.Game(7,  # width
#              6,  # height
#              4,  # tokens in a row to win
#              agent.InteractiveAgent("human1"),  # player 1
#              agent.InteractiveAgent("human2"))  # player 2

# Execute the game
count = 0
for i in range(0, 99):
    g = game.Game(7,  # width
              6,  # height
              4,  # tokens in a row to win
              first_best_agent.FirstBestAgent("firstbest", 4),         # player 1
              aba.AlphaBetaAgent("alphabeta", 4))  # player 2
    outcome = g.go()
    if outcome == 2:
        count+=1

print("AlphaBeta won ", count, "/100 times")