from sys import getallocatedblocks
import numpy as np
import random
import csv

from helper_functions import draw, score


chip_number = 0
netlist_number = 1

class net:
    def __init__(self, start, destination):
        self.wires = []
        self.start = start
        self.destination = destination
        cost = 0

class board:
    def __init__(self, gates):
        # Get max x and y values of outermost chips
        max_x, max_y = (0, 0)
        for gate in gates:
            x = gates[gate][0]
            y = gates[gate][1]
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
        
        # set board dimensions according to max x & y
        # x & y + 2 to create extra ring of space around chip print
        self.width = max_x + 2
        self.length = max_y + 2
        self.gates = gates
        self.nets = {}
        self.cost = 0


# read chip data of csv file input
# Function reads the coordinates of the gates on the print, and the netlist
# for which a viable net configuration has to be found.
def read_data(chip_number, netlist_number):
    ch = str(chip_number)
    nn = str(netlist_number)

    print_filepath = "gates&netlists/chip_" + ch + "/print_" + ch + ".csv"
    with open(print_filepath) as input:
        gate_data = [line for line in csv.reader(input)]

    gates = dict([(int(gatenum), (int(gate_x), int(gate_y))) 
            for gatenum, gate_x, gate_y in gate_data[1:]])

    gatelocations = set()

    for gate in gates:
        gatelocations.add(gates[gate])

    netlist_filepath = "gates&netlists/chip_" + ch + "/netlist_" + nn + ".csv"
    with open(netlist_filepath) as input:
        netlist_data = [line for line in csv.reader(input)]
    
    print("Netlist data: ")
    print(netlist_data)

    netlist = [tuple(map(int, net)) for net in netlist_data[1:]]

    return gates, gatelocations, netlist


gates, gatelocations, netlist = read_data(chip_number, netlist_number)

print("Netlist: ", netlist)
print("Gates: ", gates)
print("Gate locations: ", gatelocations)

random.shuffle(netlist)
print("Netlist na shuffelen: ")
print(netlist)

bord1 = board(gates)

print("Bord breedte: ", bord1.width)
print("Bord lengte: ", bord1.length)
print("")



# Niet echt meer nodig als we een betere draw hebben
# # Basic printing function to visualize board configuration
# def print_board(board):
#     for y in range(board.length - 1, -1, -1):
#         row = []

#         for x in range(0, board.width):
#             al_geprint = False

#             for gate in board.gates:
                
#                 if (gate[1], gate[2]) == (x, y):
#                     print("", gate[0], "", end = '')
#                     al_geprint = True
            
#             if al_geprint == False:            
#                 print(" + ", end = '')

#         print("\n")

# print_board(bord1)


# Create a path on board from loc to dest
# Branch from starting location and continue to branch to find paths to dest
def make_net(board, loc, dest, objectives):
    print("Objective = moving from gate ", objectives[0][0], " to ", objectives[0][1])
    print("Finding path from ", loc, " to ", dest, "...")
    hypothetical_paths = [[loc]]
    result_boards = []

    moving_possible = True
    while moving_possible == True:

        new_paths = []
        for path in hypothetical_paths:
            # Check the cardinal direction of last move from path to avoid
            # backtracking and getting stuck in a loop.
            origin = get_origin(path)
            moves = get_moves(board, path, origin)

            # For each spot found that can be moved to, add a new 
            # path (= old path + spot) to the collection of paths
            for move in moves:
                if move != False:
                    new_path = path + [move]
                    
                    # Check if path is a path to destination
                    # If more than one objective is left, start making net for
                    # next objective. If not, the final path for current
                    # configuration is found, so return the board.
                    if move == dest:
                        board.nets[objectives[0]] = new_path
                        print("found path: ")
                        print(new_path)
                        print("")

                        if len(objectives) > 1:
                            new_objective = objectives[1]
                            new_location = board.gates[new_objective[0]]
                            new_destination = board.gates[new_objective[1]]

                            new_board = make_net(board, new_location, new_destination, objectives[1:])

                            if new_board != False:
                                return new_board
                        else:
                            return board
                    # If path has not yet reached dest, continue moving.
                    # Except if move is about to pass a gate
                    elif move not in gatelocations:
                        new_paths.append(new_path)

        if new_paths == hypothetical_paths:
            print("Found no new paths")
            moving_possible = False

        # update hypothetical paths
        hypothetical_paths = [] + new_paths

    # Moving is no longer possible
    return False


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

    # prevent path from visiting already visted coordinates
    for coord in path:
        if coord == north:
            # print("coord ", coord, "already visited")
            north = False
        if coord == east:
            # print("coord ", coord, "already visited")
            east = False
        if coord == south:
            # print("coord ", coord, "already visited")
            south = False
        if coord == west:
            # print("coord ", coord, "already visited")
            west = False

    # Prevent moves from entering coordinates already used by other nets in board
    for net in board.nets:
        # [1:-1] so it can still visit its destination gate even if that gate
        # has been visited once before by another net.
        existing_net = board.nets[net][1:-1]

        if north in existing_net:
            north = False
        if east in existing_net:
            east = False
        if south in existing_net:
            south = False
        if west in existing_net:
            west = False

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


print(netlist)
test = make_net(bord1, gates[netlist[0][0]], gates[netlist[0][1]], netlist)
print(test.nets)


# Hardcode voorbeeld om te kijken of de onderstaande functie wel goed nets van
# een bord kan printen.
# bord1.nets[(1, 2)] = [(1,5),(2,5),(3,5),(4,5),(5,5),(6,5)]

# Function that gives a text output of a solution (board) as prescribed in
# the assignment. 
def output_board(board, netlist, chip_number, netlist_number):
    print("net,wires")
    for net in netlist:

        net_as_string = str(net).replace(" ", "")
        print("\"" + net_as_string + "\",\"", end = "")

        if net in board.nets:
            print(str(board.nets[net]).replace(" ", ""), end = '')
        print("\"")

    print("chip_" + str(chip_number) + "_net_" + str(netlist_number) + ","
        + str(board.cost))


# function that graphically displays the steps and saves the graphs to the move directory
def draw(moves, gates):
    route = []
    print(moves)
    # make array of arrays
    for i in range(len(moves)):
        for j in range(len(moves[0])):
            route.append([moves[i][j][0], moves[i][j][1]])
    
    # plot gates
    gates = np.array(gates)
    plt.scatter(gates[:, 1], gates[:, 2], marker = 's')
    for i in range(0,5):
        plt.text(gates[i, 1], gates[i, 2], str(i + 1), color="red", fontsize=14)

    # plot grid and routes 
    route = np.array(route)
    plt.grid()
    for i in range(len(route)):
        if i%3 == 0:
            plt.plot(route[i:3 + i, 0], route[i:3 + i, 1], marker = ' ') 
            # plt.savefig("moves/" + f"output{i}.png")
    

    # save file
    plt.savefig("moves/" + f"output.png")

draw(bord1, test, gates, netlist)

score([1,1], [1,2], [3,2])
score([1,1], [2,1], [3,2])


# print("\nVoorgeschreven output")
# output_board(bord1, netlist, chip_number, netlist_number)