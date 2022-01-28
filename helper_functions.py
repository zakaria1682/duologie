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
    for i in range(len(gates)):
        gates2.append(gates[i + 1])
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