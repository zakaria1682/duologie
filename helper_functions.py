import matplotlib
import numpy as np
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d

# function that scores possible moves manhattan style
def manhattan_distance(starting_point, possible_move, destination):

    g = (abs((possible_move[0] - starting_point[0]))
         + abs((possible_move[1] - starting_point[1])))
    h = (abs(destination[0] - possible_move[0]) 
        + abs(destination[1] - possible_move[1]))

    successor_g = g + 1
    successor_h = h

    successor_f = successor_h + successor_g 

    return successor_g, successor_h, successor_f




def euclidian_distance(point_a, point_b):
    result = (abs((point_a[0] - point_b[0]))**2 
        + abs((point_a[1] - point_b[1]))**2)**0.5

    return result

test = euclidian_distance((0, 0), (2, 2))
print(test)

def euc_3d(point_a, point_b):
    result = (abs((point_a[0] - point_b[0]))**2 
        + abs((point_a[1] - point_b[1])) 
        + abs((point_a[2] - point_b[2]))**2)**0.5

    return result


def sort_netlist(netlist, gates):
    netlist.sort(key = lambda net: euclidian_distance(gates[net[0]], gates[net[1]]))
    return netlist




# function that graphically displays the steps and saves the graphs to the move 
# directory.
def draw(board, gates, netlist):
    route = []
    net_dict = board.nets
    # print("net_dict", net_dict)
    for i in range(len(net_dict)):
        route2 = []
        # print(net_dict[netlist[i]])
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

def gate(coord, gatelocations):
    return (coord in gatelocations)


# function that graphically displays the steps and saves the graphs to the move 
# directory in 3d.
def draw3d(board, gates, netlist):
    route = []

    # LET OP! dict is nu hardcoded
    net_dict = {(1, 3): [(1, 5, 0), (1, 5, 1), (3, 5, 1), (3, 5, 0), (4, 5, 0), (4, 4, 0)], (1, 2): [(1, 5, 0), (1, 6, 0), (2, 6, 0), (2, 6, 1), (3, 6, 1), (3, 6, 5), (4, 6, 5), (5, 6, 5), (5, 6, 0), (6, 6, 0), (6, 5, 0)], (3, 5): [(4, 4, 0), (4, 3, 0), (4, 2, 0), (4, 1, 0), (3, 1, 0)], (4, 2): [(6, 2, 0), (6, 3, 0), (6, 4, 0), (6, 5, 0)], (4, 5): [(6, 2, 0), (6, 2, 1), (6, 1, 1), (6, 0, 1), (6, 0, 0), (5, 0, 0), (4, 0, 0), (3, 0, 0), (3, 1, 0)]}
    # net_dict = board.nets

    for i in range(len(netlist)):
        route2 = []
        for j in range(len(net_dict[netlist[i]])):
            route2.append(list(net_dict[netlist[i]][j]))
        route.append(route2)
    

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect((1,1,1))

    # plot gates
    gates2 = []
    for i in range(len(gates)):
        gates2.append(gates[i + 1])
        ax.text(list(gates2[i])[0], list(gates2[i])[1], 0,  str(i + 1), 
        color="red", fontsize=14)
    gates2 = np.array(gates2)

    # lis = [i for i in range(-1, board.length + 1)]
    # ax.set_xlim(-1, board.width)
    # ax.set_xticks(lis, minor=False)
    # ax.set_ylim(-1, board.length)
    # ax.set_yticks(lis, minor=False)
    # ax.set_zlim(0, board.length)
    ax.scatter(gates2[:, 0], gates2[:, 1], 0, marker = 's')

    # plot grid and routes 
    # plt.grid()
   
    
    # print("route: ", route)
    for i in range(len(net_dict)):
        route[i] = np.array(route[i])
        
        line = art3d.Line3D(route[i][0:len(route[i]), 0], route[i][0:len(route[i]), 1], route[i][0:len(route[i]), 2], 
            marker = ' ')
        ax.add_line(line)
    
    # plt.axis('off')
    lis = [i for i in range(0, board.length + 1)]
    # ax.set_xlim(0, board.width)
    ax.set_xticks(lis, minor=False)
    # ax.set_ylim(0, board.length)
    ax.set_yticks(lis, minor=False)
    # ax.set_zlim(0, board.length)
    ax.set_zticks(lis, minor=False)

    # save file
    plt.savefig("output_3d.png")