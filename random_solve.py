from helper_functions import *
from move_functions.random_move import *
from classes import *

import time



chip_number = 0
netlist_number = 2

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





def make_random_net(board, objective):
    start = board.gates[objective[0]]
    goal = board.gates[objective[1]]
    # print("Objective: ", objective)
    # print("Make net from ", start, " to ", goal, "...")
    # time.sleep(2)

    path = [start]
    impassable_terrain = gates_and_surroundings(board, objective)
    
    net_made = False
    # i = 0
    while net_made == False:
        # print(path)

        move = get_random_move(board, path, goal, objective, impassable_terrain)

        if move != False:
            path = path + [move]
        else:
            path = [start]

        if move == goal:
            # print("\nFound path to ", goal)
            # print(" : ", path)
            return path

        # Amount of tries allowed. If function has not found net before,
        # return False.
        # i+=1
        # if i > 120:
        #     return False




test_net = [(1, 2, 0), (2, 2, 0), (2, 3, 0), (2, 4, 0)]
bord1.nets[(1, 2)] = test_net
test_net2 = [(4, 4, 1), (4, 4, 2), (4, 4, 3), (4, 4, 4)]
bord1.nets[(3, 5)] = test_net2



def solve_board_random(board, netlist, tries):
    for i in range(0, len(netlist)):
        print(netlist[i])

        j = 0
        made_net = False
        while made_net == False and j < tries:
            net = make_random_net(board, netlist[i])

            if net != False:
                print("Found path ", net)
                # time.sleep(0.3)
                board.nets[netlist[i]] = net
                made_net = True
            
            j += 1

        # If function fails after "tries" tries, remove last made net (if it
        # it exists) and try to make last net again
        if j >= tries:
            if i > 0 and netlist[i - 1] in board.nets:
                del board.nets[netlist[i - 1]]
            i -= 1





# solve_board_random(bord1, netlist, 60)

print("\nBoard nets: \n", bord1.nets)

print("")
occ = used_locations(bord1)



# draw3d(bord1)