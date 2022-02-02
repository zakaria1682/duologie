# from audioop import avg
# from queue import Empty
# from sys import getallocatedblocks
import time

from helper_functions import *
from move_functions.move_nodes import *
from classes import *



chip_number = 1
netlist_number = 5


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
    print("Finding path from ", start, " to ", goal, "...")
    print("************************8")
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



def solve_board(board, netlist):
    i = 0
    for objective in netlist:
        # print("\nObjective: ", objective)
        # print("#################################")
        # print("Start: ", gates[objective[0]])
        # print("Goal: ", gates[objective[1]])
        # print("")

        net = make_net(board, gates[objective[0]], gates[objective[1]])
        # print("Gevonden net: ")
        # print(net)
        # print("")
        board.nets[objective] = net

        # draw3d(board, gates, netlist)
        # time.sleep(0.3)  

        i += 1
        # if i > 2:
        #     break







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
print(new_netlist)

solve_board(bord1, new_netlist)
print("Gemaakte nets: ")
for net in bord1.nets:
    print("\n", net, "\n########################")
    print(bord1.nets[net])
draw3d(bord1)
