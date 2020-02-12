import math
import copy
import board
import agent
import random


###########################
# Alpha-Beta Search Agent #
###########################

depthstr = [
    "",
    "",
    ""
]

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

# Check if a line of identical tokens exists starting at (x,y) in direction (dx,dy)
#
# PARAM [int] x:  the x coordinate of the starting cell
# PARAM [int] y:  the y coordinate of the starting cell
# PARAM [int] dx: the step in the x direction
# PARAM [int] dy: the step in the y direction
# RETURN [int]: return the number in a row
def max_line_in_direction_with_potential(brd, target, x, y, dx, dy):
    """Return max in a row in given direction"""
    # Go through elements
    i = 0
    count = 0
    while (((x + i * dx < brd.w) and
            (y + i * dy >= 0) and (y + i * dy < brd.h))
           and (brd.board[y + i * dy][x + i * dx] == target or brd.board[y + i * dy][x + i * dx] == 0)):
        if (brd.board[y + i * dy][x + i * dx] == target):
            count+=1
        i += 1
    if i < brd.n:
        return 0
    return count


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


# Check if a line of identical tokens exists starting at (x,y) in any direction
#
# PARAM [int] x:  the x coordinate of the starting cell
# PARAM [int] y:  the y coordinate of the starting cell
# RETURN [int]: max number in a row
def max_line_at_with_potential(brd, target, x, y):
    """Return True if a line of identical tokens exists starting at (x,y) in any direction"""
    return max(max(max_line_in_direction_with_potential(brd, target, x, y, 1, 0),  # Horizontal
                   max_line_in_direction_with_potential(brd, target, x, y, 0, 1)),  # Vertical
               max(max_line_in_direction_with_potential(brd, target, x, y, 1, 1),  # Diagonal up
                   max_line_in_direction_with_potential(brd, target, x, y, 1, -1)))  # Diagonal down


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
    def instancecheck(self, instance):
        #if next step player 1 will win
        if (get_outcome()==1):
            max_in_a_row = 999;

        #if next step player 2 will win
        if (get_outcome() == 2):
            max_in_a_row = 0;
        return max_in_a_row;

    def evaluate(self, brd, player):
        """Evaluate a heuristic of the board state"""
        # Your code here
        max_in_a_row = 0
        for x in range(brd.w):
            for y in range(brd.h):
                max_in_a_row = max(max_in_a_row, max_line_at(brd, player, x, y))

        #outcome: int = brd.copy().get_outcome()
        #if outcome == player:
        #    print("Winning outcome for ", player)
        #    return 1000000

        return max_in_a_row

    def choose_max(self, brd, player, is_min, distance_to_cut_off):
        argmax = random.choice(brd.free_cols())
        maxval = -1 if not is_min else -1000
        successors = self.get_successors(brd)
        for x in range(len(successors)):
            (argx, evaluate_x) = (x, self.evaluate(successors[x][0], player)) if distance_to_cut_off == 0 \
                else self.choose_max(successors[x][0], (player%2) + 1, not is_min, distance_to_cut_off - 1)
            if is_min:
                evaluate_x = -evaluate_x
            if evaluate_x > maxval and x in brd.free_cols():
                maxval = evaluate_x if not is_min else -evaluate_x
                argmax = x
            if maxval >= brd.n:
                return (argmax, maxval)
        depthstr[distance_to_cut_off] += str((argmax, maxval)) + ", "
        for i in range(0, distance_to_cut_off-1):
            depthstr[i] += "|"
        return (argmax, maxval)

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd: board.Board):
        """Search for the best move (choice of column for the token)"""
        # Your code here
#        depthstr[0] = ""
#        depthstr[1] = ""
#        depthstr[2] = ""
#        column = self.choose_max(brd, self.player, False, 2)[0]
#        print(depthstr[2])
#        print(depthstr[1])
#        print(depthstr[0])
#        return column

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

    # return the outcome of playing a move against another alpha-beta player by using the cutoff max_depth
    def cutMove(self,brd,count):
        bestMove = Value()
        


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
