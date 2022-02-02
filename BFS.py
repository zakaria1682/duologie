from sys import getallocatedblocks
import numpy as np
import random
import csv
import time

from helper_functions import *
from classes import *
from move_functions.random_move import *
from move_functions.move_BFS import *


chip_number = 0
netlist_number = 1


# Create a path on board from loc to dest
# Branch from starting location and continue to branch to find paths to dest
def make_net(board, loc, dest, objectives):
    # print("Objective = moving from gate ", objectives[0][0], " to ", objectives[0][1])
    # print("Finding path from ", loc, " to ", dest, "...")
    hypothetical_paths = [[loc]]
    result_boards = []
    occupied = impassable_terrain(board, objectives[0])
    moving_possible = True
    while moving_possible == True:

        new_paths = []
        for path in hypothetical_paths:
            # Check the cardinal direction of last move from path to avoid
            # backtracking and getting stuck in a loop.
            origin = get_origin(path)
            moves = get_moves(board, path, origin, occupied)
            # print(moves[0])
        

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
                        # draw3d(bord1)
                        # print("found path: ")
                        # print(new_path)
                        # print("")

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
            # print("Found no new paths")
            moving_possible = False

        # update hypothetical paths
        hypothetical_paths = [] + new_paths

    
    # Moving is no longer possible
    return False


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
    elif path[-1][2] > path[-2][2]:
        return "U"
    elif path[-1][2] < path[-2][2]:
        return "D"
    else:
        return False


# Function that gives a text output of a solution (board) as prescribed in
# the assignment. 
def output_board(board, netlist, chip_number, netlist_number):
    # print("net,wires")
    for net in netlist:

        net_as_string = str(net).replace(" ", "")
        # print("\"" + net_as_string + "\",\"", end = "")

        # if net in board.nets:
            # print(str(board.nets[net]).replace(" ", ""), end = '')
        # print("\"")

    # print("chip_" + str(chip_number) + "_net_" + str(netlist_number) + ","
        # + str(board.cost))


execution_times = []
gates, gatelocations, netlist = read_data(chip_number, netlist_number)
for i in range(0, 100):
    print(i, "%")
    start_time = time.time()
    bord = board(gates, gatelocations)
    make_net(bord, bord.gates[netlist[0][0]], bord.gates[netlist[0][1]], netlist)
    exec_time = (time.time() - start_time)
    execution_times.append(exec_time)


print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("Average execution time: ")
average_exec = average(execution_times)
print(average_exec)
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")




# bord1 = board(gates, gatelocations)
# random.shuffle(netlist)
# start_time = time.time()
# make_net(bord1, gates[netlist[0][0]], gates[netlist[0][1]], netlist)
# draw3d(bord1)



