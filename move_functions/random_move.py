import random
from move_functions.move_helper_functions import *
import time



# Returns possible moves that can be taken from end of path.
# For each cardinal direction, refuse to generate move if that direction is
# the source of the last move taken (to prevent moving back), and refuse to
# generate move if that move steps outside of the boundarys of the board.
def get_random_move(board, path, goal, objective, impassable_terrain):
    # print("")
    cur_location = path[-1]
    moves = return_directions(cur_location, board)

    # Return early if adjacent to goal
    for move in moves:
        if move == goal:
            return move

    # Prevent path from moving to coordinates
    # it has already visited,
    # that belong to gates and their neigbours,
    # that are occupied by nets already present on board
    illegal = set(path).union(impassable_terrain)
    
    # prevent path from visiting non-legal coordinates
    for i in range(0, len(moves)):
        if moves[i] in illegal:
            moves[i] = False
    
    leftover_moves = [x for x in moves if x != False]

    # Randomly select one of the found legal moves
    if leftover_moves:
        return random.choice(leftover_moves)
    else:
        return False

    