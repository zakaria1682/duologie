import time
import sys

from helper_functions import *
from move_functions.move_nodes import *
from classes import *

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))


chip_number = sys.argv[1]
netlist_number = sys.argv[2]

print("Reading chip ", chip_number, " and netlist ", netlist_number)


# Preprocessing
# Collect input data and create required structures.
# Also the ordering of the netlist is decided.
gates, gatelocations, netlist = read_data(chip_number, netlist_number)

print("Netlist: ", netlist)
print("Gates: ", gates)
print("Gate locations: ", gatelocations)

bord1 = board(gates, gatelocations)

print("Bord breedte: ", bord1.width)
print("Bord lengte: ", bord1.length)
print("")

# Netlist sorteren....
netlist = sort_netlist_euc_dist(netlist, gates)
print("\nNetlist na sorteren: ")
print(netlist)


# Find shortest path from start to goal.
# a* algorithm. Breadth first search to goal using manhattan/euclidian distance
# as a heuristic. Introduce nodes as a way to traverse spaces on the chip print
# so no entire paths have to be kept in memory.
def make_net(board, start, goal):
    gatelocations_except_goal = set()
    gatelocations_except_goal = (board.gatelocations - set([goal]))
    # gatelocations_except_goal = ((board.gatelocations).difference(set([goal])))

    starting_node = node(start, None)

    # List containing all possible locations to be moved from.
    options = [starting_node]
    seen = []
    
    while options:
        # extract the most promising path (lowest f score)
        options.sort(key = lambda location: location.f, reverse = True)
        current = options.pop()

        seen.append(current.location)

        # Check to see if goal is found. If true, trace path back to start.
        if current.location == goal:
            result = extract_path(current)
            
            return result

        # Get legal moves from current position.
        moves = get_moves(board, current, gatelocations_except_goal, goal, start)

        # For each legal move make a new node and set its scores accordingly.
        # g = distance to node (distance to parent + 1)
        # h = heuristic, which is distance from node to goal
        # f = g + h
        for move in moves:
            if move != False :
                if move[0] not in seen:
                    
                    new_option = node(move[0], parent = current)
                    new_option.g = current.g + move[1]
                    new_option.h = euc_3d(move[0], goal)
                    # new_option.h = manhattan_distance3d(move[0], goal)
                    new_option.f = new_option.g + new_option.h

                    if move[1] == 300:
                        new_option.intersection = True

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



# Function that solves given board by making a net for each requested connection
# in netlist, and saves made nets in the nets dictionary of the board.
def solve_board(board, netlist):
    for objective in netlist:
        net = make_net(board, gates[objective[0]], gates[objective[1]])
        board.nets[objective] = net



# execution_times = []

# for i in range(0, 100):
#     print(i, "%")
#     start_time = time.time()

#     bord = board(gates, gatelocations)
#     solve_board(bord, netlist)

#     exec_time = (time.time() - start_time)

#     execution_times.append(exec_time)


# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
# print("Average execution time: ")
# average_exec = average(execution_times)
# print(average_exec)
# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")



new_netlist = sort_netlist_center(bord1, netlist, gates)
# print(new_netlist)

solve_board(bord1, new_netlist)
# print("Gemaakte nets: ")
# for net in bord1.nets:
#     print("\n", net, "\n########################")
#     print(bord1.nets[net])
draw3d(bord1)


get_board_statistics(bord1, new_netlist)

