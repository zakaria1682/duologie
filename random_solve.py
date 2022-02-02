from helper_functions import *
from move_functions.random_move import *
from classes import *

import time



chip_number = 0
netlist_number = 1

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




# This function attemps to make a random path from a gate to another gate
# (objective[0] to objective[1]) by repeatedly making random moves until the
# goal is reached.
# If the function has not made a path after "tries" attempts, return False.
def make_random_net(board, objective, tries):
    start = board.gates[objective[0]]
    goal = board.gates[objective[1]]

    path = [start]
    # impassable terrain represents positions of nets already present on the
    # board and neighbors of gates to prevent nets from moving close to gates
    # that are not their objective.
    occupied = impassable_terrain(board, objective)
    
    net_made = False
    i = 0
    while net_made == False and i < tries:
        move = get_random_move(board, path, goal, objective, occupied)

        if move != False:
            path = path + [move]
        else:
            path = [start]

        if move == goal:
            return path

        i += 1

    return False



# Solve a board by repeatedly making random nets for the required gate
# connections. The algorithm allows the net making function "tries" attemps to
# make a net.
# If the net fails to be made, erase the nets from the board and try again.
def solve_board_random(board, netlist, tries):
    netlist_counter = 0
    while netlist_counter < len(netlist):
        
        made_net = False
        while made_net == False:
            net = make_random_net(board, netlist[netlist_counter], tries)
            # print(netlist_counter)
            
            if net != False:
                board.nets[netlist[netlist_counter]] = net
                made_net = True
                netlist_counter += 1
            else:
                board.nets = dict()
                netlist_counter = 0




solve_board_random(bord1, netlist, 16000)

print("\nBoard nets: \n", bord1.nets)

print("")
occ = used_locations(bord1)



draw3d(bord1)