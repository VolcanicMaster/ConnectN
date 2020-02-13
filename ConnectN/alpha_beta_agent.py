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
def max_unstopped_line_in_direction(brd, target, x, y, dx, dy):
    """Return max in a row in given direction"""
    # Go through elements
    if (brd.board[y][x] != target):
        return 0
    enemy = (target % 2 + 1)
    i = 0
    count = 0
    while (((x + i * dx < brd.w) and
            (y + i * dy >= 0) and (y + i * dy < brd.h))
           and brd.board[y + i * dy][x + i * dx] != enemy and i <= brd.n):
        if brd.board[y + i * dy][x + i * dx] == target:
            count += 1
        i += 1
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
def max_unstopped_line_at(brd, target, x, y):
    """Return True if a line of identical tokens exists starting at (x,y) in any direction"""
    return max(max(max_unstopped_line_in_direction(brd, target, x, y, 1, 0),  # Horizontal
                   max_unstopped_line_in_direction(brd, target, x, y, 0, 1)),  # Vertical
               max(max_unstopped_line_in_direction(brd, target, x, y, 1, 1),  # Diagonal up
                   max_unstopped_line_in_direction(brd, target, x, y, 1, -1)))  # Diagonal down


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
    def evaluate(self, brd, player):
        """Evaluate a heuristic of the board state"""
        # Your code here
        max_in_a_row = 0
        total_in_a_row = 0
        opp_in_a_row = 0
        for x in range(brd.w):
            for y in range(brd.h):
                maxp = max_unstopped_line_at(brd, player, x, y)
                maxopp = max_unstopped_line_at(brd, (player % 2) + 1, x, y)
                max_in_a_row = max(max_in_a_row, maxp)
                opp_in_a_row = max(opp_in_a_row, maxopp)
                if maxp > 1:
                    total_in_a_row += maxp * maxp
                if maxp >= brd.n:
                    total_in_a_row += 1000000
                if maxopp > 1:
                    total_in_a_row -= maxopp * maxopp
                if maxopp >= brd.n:
                    total_in_a_row -= 1000000

        # outcome: int = brd.copy().get_outcome()
        # if outcome == player:
        #    print("Winning outcome for ", player)
        #    return 1000000

        return total_in_a_row  # - opp_in_a_row

    # Evaluate a Board State.
    #
    # PARAM [board.Board] brd: the current board state
    # PARAM [int]: the player number of this instance's agent
    # RETURN [int]: an estimation of the utility of the board
    def evaluate_dif(self, parent_brd, child_brd, player):
        return self.evaluate(child_brd, player) - self.evaluate(parent_brd, player)

    def choose_best_move(self, brd, distance_to_cut_off):
        bestmove = self.choose_max(brd, self.player, distance_to_cut_off - 1, -1000000, 1000000)[
            0]  # if (distance_to_cut_off % 2) else (self.player%2) + 1
        return bestmove

    def choose_max_orig(self, brd, player, is_min, distance_to_cut_off):
        argmax = 0  # random.choice(brd.free_cols())
        maxval = -1 if not is_min else -1000
        x = 0
        successors = self.get_successors(brd)
        for column in brd.free_cols():
            (argx, evaluate_x) = (column, self.evaluate(successors[x][0], player)) if distance_to_cut_off <= 0 \
                else self.choose_max(successors[x][0], (player % 2) + 1, not is_min, distance_to_cut_off - 1)
            if is_min:
                evaluate_x = -evaluate_x
            if evaluate_x > maxval and column in brd.free_cols():
                maxval = evaluate_x if not is_min else -evaluate_x
                argmax = column
            if maxval >= brd.n:
                # print("Win state found for ", player)
                return (argmax, maxval)
            x += 1
        #        depthstr[distance_to_cut_off] += str((argmax, maxval)) + ", "
        #        for i in range(0, distance_to_cut_off-1):
        #            depthstr[i] += "|"
        return (argmax, maxval)

    def choose_max(self, brd, player, distance_to_cut_off, parentalpha, parentbeta):
        alpha = -1000000
        beta = 1000000
        argmax = brd.free_cols()[0]  # random.choice(brd.free_cols())
        maxval = -1
        successors = self.get_successors(brd)
#        random.shuffle(successors)
        for successor in successors:
            (argx, evaluate_x) = (successor[1], self.evaluate(successor[0], player)) if distance_to_cut_off <= 0 \
                else self.choose_min(successor[0], player, distance_to_cut_off - 1, alpha, beta)
            if evaluate_x > maxval and successor[1] in brd.free_cols():
                maxval = evaluate_x
                argmax = successor[1]
            if successor[0].get_outcome() == player:
                return (successor[1], self.evaluate(successor[0], player))
            if maxval >= brd.n:
                # print("Win state found for ", player)
                return (argmax, maxval)
            if maxval > alpha:
                alpha = maxval
            #if (alpha > parentbeta):
            #    return (argmax, 0)
            #if (beta < parentalpha):
            #    return (argmax, 0)
            #        depthstr[distance_to_cut_off] += str((argmax, maxval)) + ", "
            #        for i in range(0, distance_to_cut_off-1):
            #            depthstr[i] += "|"
        return (argmax, maxval)

    def choose_min(self, brd, player, distance_to_cut_off, parentalpha, parentbeta):
        alpha = -1000000
        beta = 1000000
        argmin = brd.free_cols()[0]  # random.choice(brd.free_cols())
        minval = 1
        successors = self.get_successors(brd)
        for successor in successors:
            (argx, evaluate_x) = (successor[1], self.evaluate(successor[0], player)) if distance_to_cut_off <= 0 \
                else self.choose_max(successor[0], player, distance_to_cut_off - 1, alpha, beta)
            evaluate_x = -evaluate_x
            if evaluate_x < minval and successor[1] in brd.free_cols():
                maxmin = -evaluate_x
                argmin = successor[1]
            if successor[0].get_outcome() == (player % 2) + 1:
                return (successor[1], self.evaluate(successor[0], player))
            if minval >= brd.n:
                # print("Win state found for ", player)
                return (argmin, minval)
            if minval < beta:
                beta = minval
            #if (alpha > parentbeta):
            #    return (argmin, 0)
            #if (beta < parentalpha):
            #    return (argmin, 0)
        #        depthstr[distance_to_cut_off] += str((argmax, maxval)) + ", "
        #        for i in range(0, distance_to_cut_off-1):
        #            depthstr[i] += "|"
        return (argmin, minval)

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd: board.Board):
        """Search for the best move (choice of column for the token)"""
        # Your code here
#        argmax = 0  # random.choice(brd.free_cols())
#        maxval = -1
#        successors = self.get_successors(brd)
#        random.shuffle(successors)
#        for successor in successors:
#            (argx, evaluate_x) = (successor[1], self.evaluate(successor[0], self.player))
#            if evaluate_x > maxval and successor[1] in brd.free_cols():
#                maxval = evaluate_x
#                argmax = successor[1]
#        return argmax
        #        depthstr[0] = ""
        #        depthstr[1] = ""
        #        depthstr[2] = ""
        #        column = self.choose_max(brd, self.player, False, 2)[0]
        #        print(depthstr[2])
        #        print(depthstr[1])
        #        print(depthstr[0])
        return self.choose_best_move(brd, 3)

        # when countToCutoff reaches max_depth, stop the search and evaluate
        # print("reached go")
        countToCutoff = 0
        simBrd = brd.copy()  # brd.copy() ?

        thisAgent = simBrd.player
        bestmove = self.tryMoves(simBrd, countToCutoff, thisAgent)
        print(bestmove, " == ", self.choose_max(brd, self.player, False, 2)[0])
        return bestmove

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
