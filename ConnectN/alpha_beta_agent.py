import math
import copy
import board
import agent

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Evaluate a Board State.
    #
    # PARAM [board.Board] brd: the current board state
    # PARAM [int]: the player number of this instance's agent
    # RETURN [int]: an estimation of the utility of the board
    def evaluate(self, brd: board.Board, thisAgent: int):
        """Evaluate a heuristic of the board state"""
        # Your code here
        # check if someone won
        #print(type(brd))
        outcome: int = brd.copy().get_outcome()
        if outcome == thisAgent:
            return 1
        if outcome != 0:
            return -1

        return 0

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd: board.Board):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        # when countToCutoff reaches max_depth, stop the search and evaluate
        #print("reached go")
        countToCutoff = 0
        simBrd = brd.copy() #brd.copy() ?

        thisAgent = simBrd.player

        return self.tryMoves(simBrd, countToCutoff, thisAgent)

    # return the move that leads to the board with the best a-b evaluation
    def tryMoves(self, brd: board.Board, count, thisAgent):
        #print("reached tryMoves")
        thisPlayer = brd.player
        freecols = brd.free_cols()
        if not freecols:
            return 0
        bestMove = freecols[0]
        bestMoveEval = 0
        for x in freecols:
            # Recurse by simulating all possible moves and then playing the other agent up to cutoff max_depth
            brdToEval = self.tryMove(brd.copy(),copy.deepcopy(x),copy.deepcopy(count),thisAgent)
            # Evaluate that boardstate
            eval = self.evaluate(brdToEval,thisAgent)
            if eval > bestMoveEval:
                brd = brdToEval
                bestMoveEval = eval
                bestMove = x
        return bestMove

    # return the outcome of playing a move against another alpha-beta player, until the cutoff max_depth
    def tryMove(self, brd: board.Board, x, count: int, thisAgent: int):
        #print("reached tryMove")
        # Try a move (copy board, edit with add_token)

        brd.add_token(x)

        outcome = brd.get_outcome()
        if outcome != 0:
            #print("found winning path: ", outcome, " won!")
            # someone won, so stop this branch
            # if the person who won was this agent, stop and return a great evaluation
            # if the person who won was the opponent, stop and return a terrible evaluation
            #if outcome == thisAgent:
            #    print("return a great evaluation")
            #else:
            #    print("return a terrible evaluation")
            #brd.print_it()
            return brd

        # check if cutoff has been reached
        count += 1
        if count == self.max_depth:
            # if the cutoff has been reached, stop the search
            return brd
        else:
            newBrd = brd.copy()
            self.tryMoves(newBrd, copy.deepcopy(count), thisAgent)
            return newBrd

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ
