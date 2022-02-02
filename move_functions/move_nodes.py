from helper_functions import gate
from move_functions.move_helper_functions import *


# Returns possible moves that can be taken from end of path.
# Illegal moves are: 
#   Moves that exceed the boundaries of the board (length and width).
#   Moves that result in the location of the parent of the node moved from (
#       moves backward).
#   Moves that result in the location of a gate that is not the goal gate
# Also, if a move results in an already visited location by other nets on board,
# give that move a higher cost to reduce it's priority.
def get_moves(board, current_node, gatelocations_except_goal, goal, start):
    cur_location = current_node.location    
        
    moves = return_directions(cur_location, board)
    # Add basic cost of 1 to moves
    moves = [(x, 1) if x != False else x for x in moves]

    # Prevent move from going towards a gate that is not its objective
    for i in range(0, len(moves)):
        if moves[i] != False:
            if moves[i][0] in gatelocations_except_goal:
                moves[i] = False
                
    # Prevent moves from going backwards (towards their parent)
    if current_node.parent != None:
        for i in range(0, len(moves)):
            if moves[i] != False:
                if moves[i][0] == current_node.parent.location:
                    moves[i] = False

    # Prevent moves from entering coordinates already used by other nets in 
    # board. Collect all present wires on board. If wire is already in use,
    # current move is making an intersection. Set cost to 300.
    # If parent is also already an intersection, move has overlap. Overlap is
    # not allowed so set move to false.
    # Checking for overlap when moving to, or from a gate is different from
    # Normal overlap checking, since the starting node is never an intersection.
    # Overlap can still occur however. To prevent compare the end & start of 
    # nets on board to current move.
    for net in board.nets:
        if board.nets[net] != False:
            existing_net = board.nets[net]
            wire_set = set(existing_net)
            ends_of_net = set((existing_net[:2] + existing_net[-2:]))
            
            a_is_gate = gate(current_node.location, board.gatelocations)

            for i in range(0, len(moves)):
                if moves[i] != False and moves[i][0] in wire_set:
                    b_is_gate = gate(moves[i][0], board.gatelocations)
                    
                    if a_is_gate or b_is_gate:
                        # Check for overlap with start or end of existing net                    
                        if (current_node.location in ends_of_net 
                            and moves[i][0] in ends_of_net):
                            moves[i] = False
                        elif not b_is_gate:
                            # update move cost to 300, since intersection
                            moves[i] = (moves[i][0], 300)
                    elif current_node.intersection == True:
                        # overlap
                        moves[i] = False
                    else:
                        moves[i] = (moves[i][0], 300)

    return moves