import math
import agent


###########################
# Alpha-Beta Search Agent #
###########################


# Check if a line of identical tokens exists starting at (x,y) in direction (dx,dy)
#
# PARAM [int] x:  the x coordinate of the starting cell
# PARAM [int] y:  the y coordinate of the starting cell
# PARAM [int] dx: the step in the x direction
# PARAM [int] dy: the step in the y direction
# RETURN [int]: return the number in a row
def max_line_in_direction(brd, target, x, y, dx, dy):
    """Return max in a row in given direction"""
    # Go through elements
    i = 0
    while (((x + i * dx < brd.w) and
            (y + i * dy >= 0) and (y + i * dy < brd.h))
           and brd.board[y + i * dy][x + i * dx] == target):
        i += 1
    return i


# Check if a line of identical tokens exists starting at (x,y) in any direction
#
# PARAM [int] x:  the x coordinate of the starting cell
# PARAM [int] y:  the y coordinate of the starting cell
# RETURN [int]: max number in a row
def max_line_at(brd, target, x, y):
    """Return True if a line of identical tokens exists starting at (x,y) in any direction"""
    return max(max(max_line_in_direction(brd, target, x, y, 1, 0),  # Horizontal
                   max_line_in_direction(brd, target, x, y, 0, 1)),  # Vertical
               max(max_line_in_direction(brd, target, x, y, 1, 1),  # Diagonal up
                   max_line_in_direction(brd, target, x, y, 1, -1)))  # Diagonal down


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
        max_in_a_row = 0
        for x in range(brd.w):
            for y in range(brd.h):
                max_in_a_row = max(max_in_a_row, max_line_at(brd, self.player, x, y))
        return max_in_a_row

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        argmax = 0
        maxval = -1
        successors = self.get_successors(brd)
        print(successors)
        print(successors[1])
        print(successors[1][0])
        for x in range(len(successors)):
            evaluate_x = self.evaluate(successors[x][0])
            if evaluate_x > maxval:
                maxval = evaluate_x
                argmax = x
                print("(argmax, maxval) = (" + str(argmax) + ", " + str(maxval) + ")\n")
        return argmax

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
            succ.append((nb, col))
        return succ
