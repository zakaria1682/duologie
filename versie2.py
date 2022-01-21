from queue import Empty
from sys import getallocatedblocks
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import random
import csv

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

class path:
    def __init__(self, coordinates):
        self.wires = coordinates
        self.score = 0

class node:
    def __init__(self, location, parent):
        self.location = location
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

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

bord1 = board(gates)

print("Bord breedte: ", bord1.width)
print("Bord lengte: ", bord1.length)
print("")


# Create a path on board from loc to dest
# Branch from starting location and continue to branch to find paths to dest
def make_net(board, start, goal):
    print("Finding path from ", start, " to ", goal, "...")
    starting_node = node(start, None)

    # open list
    options = [starting_node]
    # closed list
    seen = []

    # moving_possible = True
    # while moving_possible == True:

    # While the collection of paths is not empty, extend the path with the
    # lowest score (which represents the shortest distance to goal)
    # 
    # while options are left:
    #   pop lowest cost option
    #   add to closed list (seen)
    #   get possible moves from option
    #   for each of these moves:
    #       If it is not in the open list, add it to the open list.
    #           current becomes the parent of this option
    #           Save the f, g, and h of this current option
    #       If it is in the open list already
    #           Check to see if the path already existing in the options is
    #           cheaper (by g cost). 
    #           If so:
    #               change the parent of that option already in options to the
    #               be the current node, and update its g and f score
    #   
    #   Stop when you:
    #       add the target to the closed list (seen). Then a path is found.
    #       fail to find the target square and the open list is empty.
    #       In this case no path is found...
    #   when you find a path, trace back the parents of the found goal node
    #   to obtain its path.
    # 
    # g = dist from start to current node
    # h = heuristic, distance from current node to goal
    # f = g + h
    while options:
        # extract the most promising path (lowest score)
        options.sort(key = lambda location: location.f, reverse = True)

        print("Sorted options")
        for opt in options:
            print(opt.location, opt.f)

        current = options.pop()
        # Check to see if goal is found
        if current.location == goal:
            print("found path to ", goal)
            check = current
            result = [check.location]

            while check.parent != None:
                result.append(check.parent.location)
                check = check.parent
            result.reverse()
            
            return result

        seen.append(current)

        print("Walking ", current.location)

        # Check the cardinal direction of last move from path to avoid
        # backtracking and getting stuck in a loop.
        origin = get_origin(current)
        moves = get_moves(board, current.location, origin)

        # For each spot found that can be moved to, add a new 
        # path (= old path + spot) to the collection of paths
        for move in moves:
            if move != False:
                new_option = node(move, parent = current)
                new_option.g = current.g + 1
                # calculate heuristic
                new_option.h = abs(move[0] - goal[0]) + abs(move[1] - goal[1])
                new_option.f = new_option.g + new_option.h

                print("Adding node ", move)
                print("    parent = ", new_option.parent.location)

                # check if this option is not already in in options
                already_added = False
                for option in options:
                    # if it is already in options, compare it to the new_option
                    if option.location == move:
                        already_added = True

                        if option.g < new_option.g:
                            option = new_option

                if already_added == False:
                    options.append(new_option)

    print("options ran out....")
    return False





# Returns possible moves that can be taken from end of path.
# For each cardinal direction, refuse to generate move if that direction is
# the source of the last move taken (to prevent moving back), and refuse to
# generate move if that move steps outside of the boundarys of the board.
def get_moves(board, cur_location, origin):
    # print("")
    moves = []
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
def get_origin(node):
    if node.parent == None:
        return "None"
    current_location = node.location
    parent_location = node.parent.location
    
    if current_location[0] > parent_location[0]:
        return "E"
    elif current_location[0] < parent_location[0]:
        return "W"
    elif current_location[1] > parent_location[1]:
        return "N"
    elif current_location[1] < parent_location[1]:
        return "S"
    else:
        return False


test = make_net(bord1, gates[netlist[0][0]], gates[netlist[0][1]])
print(test)

# Hardcode voorbeeld om te kijken of de onderstaande functie wel goed nets van
# een bord kan printen.
bord1.nets[(1, 2)] = [(1,5),(2,5),(3,5),(4,5),(5,5),(6,5)]

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


# draw(make_net(bord1, (gates[0][1], gates[0][2]), (6, 5)), gates)


# print("\nVoorgeschreven output")
# output_board(bord1, netlist, chip_number, netlist_number)