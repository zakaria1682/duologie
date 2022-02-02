from move_functions.random_move import *

# Returns possible moves that can be taken from end of path.
# For each cardinal direction, refuse to generate move if that direction is
# the source of the last move taken (to prevent moving back), and refuse to
# generate move if that move steps outsi
def get_moves(board, path, origin, occupied):
    cur_location = path[-1]    
    moves = return_directions(cur_location, board)
    
    # prevent path from visiting already visted coordinates
    for i in range(0, len(moves)):
        if moves[i] != False:
            if moves[i] in path or moves[i] in occupied:
                moves[i] = False
    
    return moves