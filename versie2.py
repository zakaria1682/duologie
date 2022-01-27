from queue import Empty
from sys import getallocatedblocks
import random
import csv

import time

# import helper_functions
from helper_functions import *

chip_number = 0
netlist_number = 3

# class net:
#     def __init__(self, start, destination):
#         self.wires = []
#         self.start = start
#         self.destination = destination
#         cost = 0

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
    def __init__(self, nodes, score):
        self.nodes = nodes
        self.score = score

class node:
    def __init__(self, location, parent):
        self.location = location
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
        self.intersection = False

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

    netlist = [tuple(map(int, net)) for net in netlist_data[1:] if net != []]

    return gates, gatelocations, netlist


gates, gatelocations, netlist = read_data(chip_number, netlist_number)

print("Netlist: ", netlist)
print("Gates: ", gates)
print("Gate locations: ", gatelocations)

bord1 = board(gates)

print("Bord breedte: ", bord1.width)
print("Bord lengte: ", bord1.length)
print("")

# Netlist sorteren....
netlist = sort_netlist(netlist, gates)
print("\nNetlist na sorteren: ")
print(netlist)


# Find shortest path from start to goal.
# a* algorithm. Breadth first search to goal using manhattan/euclidian distance
# as a heuristic. Introduce nodes as a way to traverse spaces on the chip print
# so no entire paths have to be kept in memory.
def make_net(board, start, goal):
    print("Finding path from ", start, " to ", goal, "...")
    gatelocations_except_goal = set()
    gatelocations_except_goal = (gatelocations - set([goal]))
    starting_node = node(start, None)

    # List containing all possible locations to be moved from.
    options = [starting_node]
    seen = []
    
    while options:
        # extract the most promising path (lowest f score)
        options.sort(key = lambda location: location.f, reverse = True)

        # if start == (1, 5) and goal == (6, 2):
        #     time.sleep(0.5)
        #     print("Sorted options")
        #     for opt in options:
        #         print(opt.location, opt.f)
        current = options.pop()
        seen.append(current.location)

        # Check to see if goal is found.
        if current.location == goal:
            result = extract_path(current)
            
            return result

        # print("Walking ", current.location)
        # Get legal moves from current position.
        moves = get_moves(board, current, gatelocations_except_goal, goal)

        # For each legal move make a new node and set its scores accordingly.
        # g = distance to node (distance to parent + 1)
        # h = heuristic, which is distance from node to goal
        # f = g + h
        for move in moves:
            if move != False :
                if move[0] not in seen:
                    new_option = node(move[0], parent = current)
                    new_option.g = current.g + move[1]
                    new_option.h = euclidian_distance(move[0], goal)
                    new_option.f = new_option.g + new_option.h
                    if move[1] == 300:
                        new_option.intersection = True

                    # print("Adding node ", new_option.location)
                    # print("    parent = ", new_option.parent.location)

                    # Check if this option is already in in options.
                    # If it is already in options, a path to the coordinate already
                    # exists. Compare the two and accept shortest path (smallest g).
                    already_added = False
                    for option in options:
                        
                        if option.location == move[0]:
                            already_added = True

                            if option.g < new_option.g:
                                option = new_option

                    if already_added == False:
                        options.append(new_option)

    print("options ran out....")
    return False



# Returns possible moves that can be taken from end of path.
# Illegal moves are: 
#   Moves that exceed the boundaries of the board (length and width).
#   Moves that result in the location of the parent of the node moved from (
#       moves backward).
#   Moves that result in the location of a gate that is not the goal gate
# Also, if a move results in an already visited location by other nets on board,
# give that move a higher cost to reduce it's priority.
def get_moves(board, current_node, gatelocations_except_goal, goal):
    # print("")
    moves = []
    cur_location = current_node.location
    # print("Getting moves from location ", cur_location)


    north = ((cur_location[0], cur_location[1] + 1), 1)
    east = ((cur_location[0] + 1, cur_location[1]), 1)
    south = ((cur_location[0], cur_location[1] - 1), 1)
    west = ((cur_location[0] - 1, cur_location[1]), 1)

    if current_node.parent != None:
        if (cur_location[1] >= (board.length - 1)
            or north[0] == current_node.parent.location 
            or north[0] in gatelocations_except_goal):
            north = False 
        # print("North: ", north)   

        if (cur_location[0] >= (board.width - 1)
            or east[0] == current_node.parent.location 
            or east[0] in gatelocations_except_goal):
            east = False
        # print("East: ", east)

        if (cur_location[1] <= 0 
            or south[0] == current_node.parent.location 
            or south[0] in gatelocations_except_goal):
            south = False
        # print("South: ", south)

        if (cur_location[0] <= 0 
            or west[0] == current_node.parent.location 
            or west[0] in gatelocations_except_goal):
            west = False
        # print("West: ", west)

    # Prevent moves from entering coordinates already used by other nets in 
    # board. Collect all present wires on board. If wire is already in use,
    # current move is making an intersection. Set cost to 300.
    # If parent is also already an intersection, move has overlap. Overlap is
    # not allowed so set move to false.
    # Checking for overlap when moving to, or from a gate is different from
    # Normal overlap checking, since the starting node is never an intersection.
    # Overlap can still occur however.
    # To prevent overlap, compare the ends of nets on board to current move.
    for net in board.nets:
        if board.nets[net] != False:
            # [1:-1] so it can still visit its destination gate even if that gate
            # has been visited once before by another net.

            existing_net = board.nets[net]
            wire_set = set(existing_net)
            ends_of_net = set((existing_net[:2] + existing_net[-2:]))
            
            a_is_gate = gate(current_node.location, gatelocations)

            if north != False and north[0] in wire_set:
                b_is_gate = gate(north[0], gatelocations)
                if a_is_gate or b_is_gate:
                    # Check for overlap with start or end of existing net                    
                    if (current_node.location in ends_of_net 
                        and north[0] in ends_of_net):
                        north = False
                    elif not b_is_gate:
                        north = (north[0], 300)
                elif current_node.intersection == True:
                    # overlap
                    north = False
                else:
                    north = (north[0], 300)

            if east != False and east[0] in wire_set:
                b_is_gate = gate(east[0], gatelocations)
                if a_is_gate or b_is_gate:
                    # Check for overlap with start or end of existing net
                    if (current_node.location in ends_of_net 
                        and east[0] in ends_of_net):
                        east = False
                    elif not b_is_gate:
                        east = (east[0], 300)
                elif current_node.intersection == True:
                    # overlap
                    east = False
                else:
                    east = (east[0], 300)

            if south != False and south[0] in wire_set:
                b_is_gate = gate(south[0], gatelocations)
                if a_is_gate or b_is_gate:
                    # Check for overlap with start or end of existing net
                    if (current_node.location in ends_of_net 
                        and south[0] in ends_of_net):
                        south = False
                    elif not b_is_gate:
                        south = (south[0], 300)
                elif current_node.intersection == True:
                    # overlap
                    south = False
                else:
                    south = (south[0], 300)

            if west != False and west[0] in wire_set:
                b_is_gate = gate(west[0], gatelocations)
                if a_is_gate or b_is_gate:
                    # Check for overlap with start or end of existing net
                    if (current_node.location in ends_of_net 
                        and west[0] in ends_of_net):
                        west = False
                    elif not b_is_gate:
                        west = (west[0], 300)
                elif current_node.intersection == True:
                    # overlap
                    west = False
                else:
                    west = (west[0], 300)


        

    return north, east, south, west



# Extract a path from a node to tree root by traversing parents until a node
# without parents is found. Wanted path is from root to node, so the path
# collected is in reverse. Reverse path before returning.
def extract_path(node):
    # print("found path to ", node.location)
    result_path = [node.location]

    while node.parent != None:
        result_path.append(node.parent.location)
        node = node.parent
    result_path.reverse()

    return result_path



# test = make_net(bord1, gates[netlist[0][0]], gates[netlist[0][1]])
# print(test)



def solve_board(board, netlist):

    i = 0
    print("netlist: ", netlist)
    for objective in netlist:
        print("\nObjective: ", objective)
        print("#################################")
        # print("Start: ", gates[objective[0]])
        # print("Goal: ", gates[objective[1]])
        # print("")

        net = make_net(board, gates[objective[0]], gates[objective[1]])
        print("Gevonden net: ")
        print(net)
        print("")
        board.nets[objective] = net
        draw(board, board, gates, netlist)
        # time.sleep(1)   




        i += 1
        # if i > 2:
        #     break


# draw(bord1, bord1, gates, netlist)

solve_board(bord1, netlist)

for solved_net in bord1.nets:

    print(bord1.nets[solved_net])

print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")


