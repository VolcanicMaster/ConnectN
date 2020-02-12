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

    # PARAM [board.Board] brd: the current board state
    # PARAM [int]: the player number of this instance's agent
    # RETURN [int]: an estimation of the utility of the board

    # instancecheck
    # redo the is_line_at to check it there's a line of n-1 identical tokens
    def is_line_at_short(self, x, y, dx, dy):
        """Return True if a line of identical tokens exists starting at (x,y) in direction (dx,dy)"""
        # Avoid out-of-bounds errors
        if ((x + (self.n - 2) * dx >= self.w) or
                (y + (self.n - 2) * dy < 0) or (y + (self.n - 2) * dy >= self.h)):
            return False
        # Get token at (x,y)
        t = self.board[y][x]
        # Go through elements
        for i in range(1, self.n -1):
            if self.board[y + i * dy][x + i * dx] != t:
                return False
        return True

    def is_any_line_at_short(self, x, y):
        """Return True if a line of identical tokens exists starting at (x,y) in any direction"""
        return (self.is_line_at_short(x, y, 1, 0) or # Horizontal
                self.is_line_at_short(x, y, 0, 1) or # Vertical
                self.is_line_at_short(x, y, 1, 1) or # Diagonal up
                self.is_line_at_short(x, y, 1, -1)) # Diagonal down

    def get_outcome_short(self):
        """Returns the winner of the game: 1 for Player 1, 2 for Player 2, and 0 for no winner"""
        for x in range(self.w):
            for y in range(self.h):
                if (self.board[y][x] != 0) and self.is_line_at_short(x, y, 1, 0):
                    if ((self.board[y][x-1] == 0 and (self.board[y-1][x-1] == 1 or self.board[y-1][x-1] == 2)) or
                        (self.board[y][x+n-1] == 0 and (self.board[y - 1][x+n-1] == 1 or self.board[y - 1][x+n-1] == 2)))
                    return board[y][x]

                if (self.board[y][x] != 0) and self.is_line_at_short(x, y, 0, 1) and self.board[y+n-1][x] = 0:
                    return board[y][x]

                if (self.board[y][x] != 0) and self.is_line_at_short(x, y, 1, 1):
                    if ((self.board[y-1][x-1] == 0 and (self.board[y-2][x-1] == 1 or self.board[y-2][x-1] == 2)) or
                        (self.board[y+n-1][x+n-1] == 0 and (self.board[y +n-2][x+n-1] == 1 or self.board[y +n-2][x+n-1] == 2)))
                    return board[y][x]

                if (self.board[y][x] != 0) and self.is_line_at_short(x, y, 1, -1):
                    if ((self.board[y+1][x+1] == 0 and (self.board[y][x+1] == 1 or self.board[y][x+1] == 2)) or
                        (self.board[y-n+1][x-n+1] == 0 and (self.board[y-n][x-n+1] == 1 or self.board[y-n][x-n+1] == 2)))
                    return board[y][x]

        return 0

    def instancecheck(self, instance):
        #if next step player 1 will win
        if (get_outcome_short == 1):
            max_in_a_row = 999;

        if (get_outcome_short== 2):
            max_in_a_row = 0;

        return max_in_a_row;

    def evaluate(self, brd, player):
        """Evaluate a heuristic of the board state"""
        # Your code here
        max_in_a_row = 0
        total_in_a_row = 0
        opp_in_a_row = 0
        for x in range(brd.w):
            for y in range(brd.h):
                maxp = max_line_at(brd, player, x, y)
                maxopp = max_line_at(brd, (player%2)+1, x, y)
                max_in_a_row = max(max_in_a_row, maxp)
                opp_in_a_row = max(opp_in_a_row, maxopp)
                if maxp > 1:
                    total_in_a_row += maxp*maxp
                if maxopp > 1:
                    total_in_a_row -= maxopp*maxopp

        #outcome: int = brd.copy().get_outcome()
        #if outcome == player:
        #    print("Winning outcome for ", player)
        #    return 1000000

        return total_in_a_row# - opp_in_a_row

    def choose_best_move(self, brd, distance_to_cut_off):
        return self.choose_max(brd, self.player if (distance_to_cut_off % 2) else (self.player%2) + 1, False, distance_to_cut_off)[0]

    def choose_max(self, brd, player, is_min, distance_to_cut_off):
        argmax = 0#random.choice(brd.free_cols())
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
                #print("Win state found for ", player)
                return (argmax, maxval)
#        depthstr[distance_to_cut_off] += str((argmax, maxval)) + ", "
#        for i in range(0, distance_to_cut_off-1):
#            depthstr[i] += "|"
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
        return self.choose_best_move(brd, 4)

        # when countToCutoff reaches max_depth, stop the search and evaluate
        #print("reached go")
        countToCutoff = 0
        simBrd = brd.copy() #brd.copy() ?

        thisAgent = simBrd.player
        bestmove = self.tryMoves(simBrd, countToCutoff, thisAgent)
        print(bestmove, " == ", self.choose_max(brd, self.player, False, 2)[0])
        return bestmove

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
