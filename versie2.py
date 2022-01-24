from queue import Empty
from sys import getallocatedblocks
import random
import csv

# import helper_functions
from helper_functions import *

chip_number = 0
netlist_number = 1

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


# Find shortest path from start to goal.
# a* algorithm. Breadth first search to goal using manhattan/euclidian distance
# as a heuristic. Introduce nodes as a way to traverse spaces on the chip print
# so no entire paths have to be kept in memory.
def make_net(board, start, goal):
    print("\nFinding path from ", start, " to ", goal, "...\n#########################################################")
    gatelocations_except_goal = set()
    gatelocations_except_goal = (gatelocations - set([goal]))
    # print("Gatelocations without ", goal, ": ", gatelocations_except_goal)
    starting_node = node(start, None)

    # List containing all possible locations to be moved from.
    options = [starting_node]
    
    while options:
        # extract the most promising path (lowest f score)
        options.sort(key = lambda location: location.f, reverse = True)
        print("Sorted options")
        for opt in options:
            print(opt.location, opt.f)
        current = options.pop()


        # Check to see if goal is found.
        if current.location == goal:
            result = extract_path(current)
            
            return result

        # print("Walking ", current.location)
        # Get legal moves from current position.
        moves = get_moves(board, current, gatelocations_except_goal)

        # For each legal move make a new node and set its scores accordingly.
        # g = distance to node (distance to parent + 1)
        # h = heuristic, which is distance from node to goal
        # f = g + h
        for move in moves:
            if move != False:
                new_option = node(move[0], parent = current)
                new_option.g = current.g + move[1]
                new_option.h = abs(move[0][0] - goal[0]) + abs(move[0][1] - goal[1])
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
                    
                    if option.location == move:
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
def get_moves(board, current_node, gatelocations_except_goal):
    # print("")
    moves = []
    cur_location = current_node.location
    # print("Getting moves from location ", cur_location)


    north = ((cur_location[0], cur_location[1] + 1), 1)
    east = ((cur_location[0] + 1, cur_location[1]), 1)
    south = ((cur_location[0], cur_location[1] - 1), 1)
    west = ((cur_location[0] - 1, cur_location[1]), 1)

    if current_node.parent != None:
        if (cur_location[1] >= board.length 
            or north[0] == current_node.parent.location 
            or north[0] in gatelocations_except_goal):
            north = False
        # print("North: ", north)   

        if (cur_location[0] >= board.width 
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
    existing_wires = set()
    for net in board.nets:
        # [1:-1] so it can still visit its destination gate even if that gate
        # has been visited once before by another net.
        existing_net = set(board.nets[net][1:-1])
        existing_wires = existing_wires.union(existing_net)

    if north != False and north[0] in existing_wires:
        # print("Intersection ")
        if (current_node.parent != None
            and current_node.parent.intersection == True):
            print("overlap!")
            north = False
        else:
            north = (north[0], 300)
    if east != False and east[0] in existing_wires:
        # print("Intersection ")
        if (current_node.parent != None
            and current_node.parent.intersection == True):
            print("overlap!")
            east = False
        else:
            east = (east[0], 300)
    if south != False and south[0] in existing_wires:
        # print("Intersection ")
        if (current_node.parent != None
            and current_node.parent.intersection == True):
            print("overlap!")
            south = False
        else:
            south = (south[0], 300)
    if west != False and west[0] in existing_wires:
        # print("Intersection ")
        if (current_node.parent != None 
            and current_node.parent.intersection == True):
            print("overlap!")
            west = False
        else:
            west = (west[0], 300)

    return north, east, south, west



# Extract a path from a node to tree root by traversing parents until a node
# without parents is found. Wanted path is from root to node, so the path
# collected is in reverse. Reverse path before returning.
def extract_path(node):
    print("found path to ", node.location)
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
    for objective in netlist:
        # print("Start: ", gates[objective[0]])
        # print("Goal: ", gates[objective[1]])
        # print("")

        net = make_net(board, gates[objective[0]], gates[objective[1]])
        # print(net)
        # print("")
        board.nets[objective] = net

        i += 1
        # if i > 2:
        #     break


solve_board(bord1, netlist)

for solved_net in bord1.nets:

    print(bord1.nets[solved_net])

draw(bord1, bord1, gates, netlist)


