from sys import getallocatedblocks
import numpy as np
import random
import csv

from helper_functions import *


chip_number = 0
netlist_number = 3


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
        self.height = 7
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

    gates = dict([(int(gatenum), (int(gate_x), int(gate_y), 0)) 
            for gatenum, gate_x, gate_y in gate_data[1:]])

    gatelocations = set()

    for gate in gates:
        gatelocations.add(gates[gate])

    netlist_filepath = "gates&netlists/chip_" + ch + "/netlist_" + nn + ".csv"
    with open(netlist_filepath) as input:
        netlist_data = [line for line in csv.reader(input)]

    netlist = [tuple(map(int, net)) for net in netlist_data[1:] if net != []]

    return gates, gatelocations, netlist


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
        north = (cur_location[0], cur_location[1] + 1, cur_location[2])
    else:
        north = False
    # print("North: ", north)

    if origin != "W" and cur_location[0] < board.width - 1:
        east = (cur_location[0] + 1, cur_location[1], cur_location[2])
    else:
        east = False
    # print("East: ", east)

    if origin != "N" and cur_location[1] > 0:
        south = (cur_location[0], cur_location[1] - 1, cur_location[2])
    else:
        south = False
    # print("South: ", south)

    if origin != "E" and cur_location[0] > 0:
        west = (cur_location[0] - 1, cur_location[1], cur_location[2])
    else:
        west = False
    # print("West: ", west)

    if origin != "u" and cur_location[0] > 0:
        up = ((cur_location[0], cur_location[1], cur_location[2] + 1))
    else:
        up = False

    if origin != "d" and cur_location[0] > 0:
        down = ((cur_location[0], cur_location[1], cur_location[2] - 1))
    else:
        down = False

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
        if coord == up:
            # print("coord ", coord, "already visited")
            up = False
        if coord == down:
            # print("coord ", coord, "already visited")
            down = False

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
        if up in existing_net:
            up = False
        if down in existing_net:
            down = False

    return north, east, south, west, up, down


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



gates, gatelocations, netlist = read_data(chip_number, netlist_number)
random.shuffle(netlist)
bord1 = board(gates)
make_net(bord1, gates[netlist[0][0]], gates[netlist[0][1]], netlist)
draw3d(bord1, gates, netlist)


