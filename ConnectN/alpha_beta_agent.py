import math
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
    # RETURN [int]: an estimation of the utility of the board
    def evaluate(self, brd):
        """Evaluate a heuristic of the board state"""
        # Your code here

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        # when countToCutoff reaches max_depth, stop the search and evaluate
        countToCutoff = 0
        simBrd = brd.copy()

        self.tryMoves(self, simBrd, countToCutoff)

    # return the board with the maximum evaluation
    def tryMoves(self, brd, count):
        for x in range(0, brd.w):
            # Recurse until cutoff(max_depth) is reached
            brdToEval = self.tryMove(self,brd,x,count,True)
            # Evaluate that boardstate

    # return the outcome of playing a move against another alpha-beta player, until the cutoff max_depth
    def tryMove(self, brd, x, count, isPlayer1):
        # Try a move (copy board, edit with add_token)
        brd.add_token(self, x)
        # check if cutoff has been reached
        count += 1
        if count == self.max_depth:
            return brd
        else:
            self.tryMove(self,brd,x,count,not(isPlayer1))

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
