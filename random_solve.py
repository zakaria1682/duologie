from helper_functions import *
from move_functions.random_move import *
from classes import *
import sys

import time



chip_number = sys.argv[1]
netlist_number = sys.argv[2]



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





# The execution of the solve
# First read data of chip-print and netlist
# Then start timing and execute solve
# Then write execution time to output.csv
gates, gatelocations, netlist = read_data(chip_number, netlist_number)

chip_board = board(gates, gatelocations)
# sort netlist
netlist = sort_netlist_center(chip_board, netlist)

start_time = time.time()
solve_board_random(chip_board, netlist, 10000)
execution_time = (time.time() - start_time)

statistics = get_board_statistics(chip_board)


csvfile = open('output/output_random_solve.csv', 'a')
csvfile.write("\n")
string = str(statistics[0]) + "/" + str(len(netlist))
csvfile.write(f"{execution_time},{string},{statistics[1]}")
 
csvfile.close()