import numpy as np
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
import csv



# Helper_functions.py contain functions that serve the move functions and the
# main .py files of the used algorithm
################################################################################



# Read chip data of csv file input
# Function reads the coordinates of the gates on the print, and the netlist
# for which a viable net configuration has to be found. Returns a set of 
# locations for the board that are occupied by gates, and a dictionary linking
# those coordinates to gate numbers, and a list containing the netlist.
def read_data(chip_number, netlist_number):
    cn = str(chip_number)
    nn = str(netlist_number)

    print_filepath = "gates&netlists/chip_" + cn + "/print_" + cn + ".csv"
    with open(print_filepath) as input:
        gate_data = [line for line in csv.reader(input)]

    # Gates are always at bottom layer of print, so their z is always 0.
    gates = dict([(int(gatenum), (int(gate_x), int(gate_y), 0)) 
            for gatenum, gate_x, gate_y in gate_data[1:]])

    gatelocations = set()

    for gate in gates:
        gatelocations.add(gates[gate])

    netlist_filepath = "gates&netlists/chip_" + cn + "/netlist_" + nn + ".csv"
    with open(netlist_filepath) as input:
        netlist_data = [line for line in csv.reader(input)]

    # Create tuples of requested connections in netlist data and prevent
    # empty read lines from being added to result netlist.
    netlist = [tuple(map(int, net)) for net in netlist_data[1:] if net != []]

    return gates, gatelocations, netlist



# Return the manhattan distance between 2 coördinates in 2d space
def manhattan_distance(point_a, point_b):
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])



# Return the manhattan distance between 2 coördinates in 3d space
def manhattan_distance3d(point_a, point_b):
    return (abs(point_a[0] - point_b[0]) 
        + abs(point_a[1] - point_b[1])
        + abs(point_a[2] - point_b[2]))



# Function that calculates the euclidian between 2 coördinates in 2d space.
def euclidian_distance(point_a, point_b):
    result = (abs((point_a[0] - point_b[0]))**2 
        + abs((point_a[1] - point_b[1]))**2)**0.5

    return result

# Function that calculates the euclidian between 2 coördinates in 3d space.
def euc_3d(point_a, point_b):
    result = (abs((point_a[0] - point_b[0]))**2 
        + abs((point_a[1] - point_b[1])) 
        + abs((point_a[2] - point_b[2]))**2)**0.5

    return result



# Function that sorts the requested gate-connections of a netlist based on the
# euclidian distance between the gates per connection.
def sort_netlist_euc_dist(netlist, gates):
    netlist.sort(key = lambda net: euclidian_distance(gates[net[0]], gates[net[1]]))
    return netlist



# Function returns coordinates of actual center of the bottom layer of board
# The coordinate does not have to contain just integers
def calc_board_middle(board):
    x = (board.length - 1)/2
    y = (board.width - 1)/2
    return (x, y, 0)



# Sort the netlist based on distance of gates to center of board
def sort_netlist_center(board, netlist):
    M = calc_board_middle(board)

    netlist.sort(key = lambda net: 
          euclidian_distance(board.gates[net[0]], M)
        + euclidian_distance(board.gates[net[1]], M)
        + euclidian_distance(board.gates[net[0]], board.gates[net[1]])
        )

    return netlist



# Return the average value of a list
def average(lst):
    return sum(lst) / len(lst)



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



# Return true if coord is a gate (if coord is in the set gatelocations)
def gate(coord, gatelocations):
    return (coord in gatelocations)



# Function that returns the amount of made wires on a given board and counts
# those wires to determine a cost of the board.
# Wires (that are not on a gate) that make an intersection increase the cost
# by 300.
def get_board_statistics(board):
    wire_dict = dict()
    amount_of_nets = 0
    cost = 0

    for net in board.nets:
        if board.nets[net] != False:
            amount_of_nets += 1
            cost += (len(board.nets[net]) - 1)
            net_coordinates = board.nets[net]

            for wire in net_coordinates:
                if wire not in board.gatelocations:
                    if wire in wire_dict:
                        wire_dict[wire] += 1
                    else:
                        wire_dict[wire] = 1

    # Account for intersections. Increase cost by 300 for each intersection
    for item in wire_dict:
        if wire_dict[item] > 1:
            cost += (wire_dict[item] - 1) * 300

    # print("Amount of nets: ", amount_of_nets, "/", len(netlist))
    # print("Cost of this board configuration: ", cost)
    return amount_of_nets, cost



# function that graphically displays the nets of a solved chip-print
def draw(board, gates, netlist):
    route = []
    net_dict = board.nets
    for i in range(len(net_dict)):
        route2 = []
        if net_dict[netlist[i]] != False:
            for j in range(len(net_dict[netlist[i]])):
                route2.append(list(net_dict[netlist[i]][j]))
            route.append(route2)
    
    # plot gates
    gates2 = []
    for i in range(len(gates)):
        gates2.append(gates[i + 1])
        plt.text(list(gates2[i])[0], list(gates2[i])[1], str(i + 1), 
        color="red", fontsize=14)
    gates2 = np.array(gates2)
    plt.xlim(-1, board.width)
    plt.ylim(-1, board.length)
    plt.scatter(gates2[:, 0], gates2[:, 1], marker = 's')

    # plot grid and routes 
    plt.grid()
   
    # print("route: ", route)
    for i in range(len(route)):
        route[i] = np.array(route[i])
        plt.plot(route[i][0:len(route[i]), 0], route[i][0:len(route[i]), 1], 
            marker = ' ') 
    
    # save file
    plt.savefig("output_2d.png")





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






# function that graphically displays the steps and saves the graphs to the move 
# directory in 3d.
def draw3d(board):
    route = []
    net_dict = board.nets

    # print(netlist)
    # print(net_dict)

    tupleroute = [net_dict[obj] for obj in net_dict if net_dict[obj] != False]

    route = []
    for net in tupleroute:
        route.append([list(point) for point in net])

    # print("ROUTES BUT IN LIST")
    # print(route)
    
    fig = plt.figure(figsize = (15, 15))
    ax = plt.axes()
    plt.axis('off')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect((1,1,1))

    # plot gates
    gates2 = []
    for i in range(len(board.gates)):
        gates2.append(board.gates[i + 1])
        ax.text(list(gates2[i])[0], list(gates2[i])[1], 0,  str(i + 1), 
        color="red", fontsize=14)
    gates2 = np.array(gates2)
    ax.scatter(gates2[:, 0], gates2[:, 1], 0, marker = 's')

    # plot grid and routes 
    cmap = plt.get_cmap('gnuplot')
    colors = [cmap(i) for i in np.linspace(0, 1, len(route))]
    for i, color in enumerate(colors, start=0):
        route[i] = np.array(route[i])
        
        line = art3d.Line3D(route[i][0:len(route[i]), 0], route[i][0:len(route[i]), 1], route[i][0:len(route[i]), 2], 
            marker = ' ', color= color)
        ax.add_line(line)
    
    
    y_axis = [i for i in range(0, board.length + 1)]
    x_axis = [i for i in range(0, board.width + 1)]
    z_axis = [i for i in range(0, board.height + 1)]
    ax.set_xticks(x_axis, minor = False)
    ax.set_yticks(y_axis, minor = False)
    ax.set_zticks(z_axis, minor = False)
    # ax.tight_layout()

    # save file
    plt.savefig("output_3d.png")