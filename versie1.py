import csv

class net:
    def __init__(self, start, destination):
        self.wires = []
        self.start = start
        self.destination = destination
        cost = 0

class board:
    def __init__(self, chips):
        # Get max x and y values of outermost chips
        max_x, max_y = (0, 0)
        for coordinates in chips:
            x = coordinates[1]
            y = coordinates[2]
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
        
        # set board dimensions according to max x & y
        # x & y + 2 to create extra ring of space around chip configuration
        self.width = max_x + 2
        self.length = max_y + 2
        self.chips = chips
        self.nets = []
        self.cost = 0


# read chip data of csv file input
with open("gates&netlists/chip_0/print_0.csv") as input:
    chip_data = [line for line in csv.reader(input)]

# Skip header first line for chips data, and turn chip data into ints
chips = [list(map(int, chip)) for chip in chip_data[1:]]


# read net data of csv file input
with open("gates&netlists/chip_0/netlist_1.csv") as input:
    netlist_data = [line for line in csv.reader(input)]

# Skip header first line for chips data, and turn chip data into ints
nets = [list(map(int, net)) for net in netlist_data[1:]]

bord1 = board(chips)

print("Bord breedte: ", bord1.width)
print("Bord lengte: ", bord1.length)
print("")


# Basic printing function to visualize board configuration
def print_board(board):
    for y in range(board.length - 1, -1, -1):
        row = []

        for x in range(0, board.width):
            al_geprint = False

            for chip in board.chips:
                
                if (chip[1], chip[2]) == (x, y):
                    print("", chip[0], "", end = '')
                    al_geprint = True
            
            if al_geprint == False:            
                print(" + ", end = '')

        print("\n")


print_board(bord1)

# loc = (1, 5)
# dest = (6, 5)

# Create a path on board from loc to dest
# Branch from starting location and continue to branch to find paths to dest
def make_net(board, loc, dest):
    print("Starting location")
    print(loc)
    hypothetical_paths = [[loc]]
    # print(hypothetical_paths)

    moving_possible = True
    i = 0
    while moving_possible == True:
        if i > 3:
            break

        new_paths = []
        for path in hypothetical_paths:
            # Check the cardinal direction of last move from path to avoid
            # backtracking and getting stuck in a loop.
            origin = get_origin(path)
            moves = get_moves(board, path, origin)
            moves[0]

            # For each spot found that can be moved to, add a new 
            # path (= old path + spot) to the collection of paths
            for move in moves:
                if move != False:
                    new_path = path + [move]
                    new_paths.append(new_path)

        if new_paths == hypothetical_paths:
            moving_possible = False

        print(new_paths)

        hypothetical_paths = [] + new_paths

        i += 1


# Returns possible moves that can be taken from end of path.
# For each cardinal direction, refuse to generate move if that direction is
# the source of the last move taken (to prevent moving back), and refuse to
# generate move if that move steps outside of the boundarys of the board.
def get_moves(board, path, origin):
    # print("")
    moves = []
    cur_location = path[-1]
    # print("Getting moves from location ", cur_location)

    if origin != "S" and cur_location[1] < board.length - 1:
        north = (cur_location[0], cur_location[1] + 1)
    else:
        north = False
    # print("North: ", north)

    if origin != "W" and cur_location[0] < board.width - 1:
        east = (cur_location[0] + 1, cur_location[1])
    else:
        east = False
    # print("East: ", east)

    if origin != "N" and cur_location[1] > 0:
        south = (cur_location[0], cur_location[1] - 1)
    else:
        south = False
    # print("South: ", south)

    if origin != "E" and cur_location[0] > 0:
        west = (cur_location[0] - 1, cur_location[1])
    else:
        west = False
    # print("West: ", west)

    return north, east, south, west


# Check what the last direction the path has taken is.
def get_origin(path):
    if len(path) == 1:
        return "None"
    elif path[-1][0] > path[-2][0]:
        return "E"
    elif path[-1][0] < path[-2][0]:
        return "W"
    elif path[-1][1] > path[-2][1]:
        return "N"
    elif path[-1][1] < path[-2][1]:
        return "S"
    else:
        return False



make_net(bord1, (chips[0][1], chips[0][2]), (6, 5))

# [(1, 5), (0, 5), (0, 4), (0, 3), (1, 3)]