# Helper functions that are exclusively used by the move functions
###############################################################################

# Return destinations of moves with length one in directions (in 3d):
# North, East, South, West, Up, Down
# respectively. If a move exceeds board dimensions, set it to False.
def return_directions(point, board):
    north = (point[0], point[1] + 1, point[2])
    east = (point[0] + 1, point[1], point[2])
    south = (point[0], point[1] - 1, point[2])
    west = (point[0] - 1, point[1], point[2])
    up = (point[0], point[1], point[2] + 1)
    down = (point[0], point[1], point[2] - 1)

    if point[1] >= board.length - 1:
        north = False

    if point[0] >= (board.width - 1):
        east = False 
    
    if point[1] <= 0:
        south = False

    if point[0] <= 0:
        west = False

    if point[2] >= (board.height - 1):
        up = False

    if point[2] <= 0:
        down = False

    return [north, east, south, west, up, down]


# Collect location of gates (EXCEPT gates in objective) and their direct
# surroundings and return them as a set.
def gates_and_surroundings(board, objective):
    locations = set()

    for gate in board.gates:
        if gate != objective[0] and gate != objective[1]:
            # The gate itself
            gate_coordinates = board.gates[gate]
            locations.add(gate_coordinates)

            # Its surroundings
            gate_surroundings = return_directions(gate_coordinates, board)

            locations = locations.union(set([x for x in gate_surroundings 
                                             if x != False]))

    return locations


# Return a set of locations in use by other nets on the board, except the final
# coordinates of those nets, since they are locations of gates and gates
# should still be accessable if they are for example a goal.
def used_locations(board):
    occupied = set()

    for net in board.nets:
        # print("Adding net ", net, " with coordinates ", board.nets[net][1:-1])
        occupied = occupied.union(set(board.nets[net][1:-1]))

    # print("Locations in use by other nets: ")
    # print(occupied)

    return occupied


# Function that bundles above helper functions and returns locations on board
# in use by other nets or occupied by the surroundings of 
def impassable_terrain(board, objective):
    return used_locations(board).union(gates_and_surroundings(board, objective))



