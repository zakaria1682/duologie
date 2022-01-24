import matplotlib
import numpy as np
from matplotlib import pyplot as plt

# function that scores possible moves manhattan style
def manhattan_score(starting_point, possible_move, destination):

    g = abs((possible_move[0] - starting_point[0])) + abs((possible_move[1] - starting_point[1]))
    h = abs(destination[0] - possible_move[0]) + abs(destination[1] - possible_move[1])

    successor_g = g + 1
    successor_h = h

    successor_f = successor_h + successor_g 

    return successor_g, succssor_h, successor_f


# function that scores possible moves euclidian style
def euclidian_score(starting_point, possible_move, destination):
    g = (abs((possible_move[0] - starting_point[0]))**2 + abs((possible_move[1] - starting_point[1]))**2)**0.5
    h = (abs(destination[0] - possible_move[0])**2 + abs(destination[1] - possible_move[1])**2)**0.5

    successor_g = g + 1
    successor_h = h

    successor_f = successor_h + successor_g 

    return successor_g, succssor_h, successor_f


# function that graphically displays the steps and saves the graphs to the move directory
def draw(board, test, gates, netlist):
    route = []
    net_dict = test.nets
    print("net_dict", net_dict)
    for i in range(len(netlist)):
        route2 = []
        for j in range(len(net_dict[netlist[i]])):
            route2.append(list(net_dict[netlist[i]][j]))
        route.append(route2)
    
     
    # plot gates
    gates2 = []
    for i in range(len(gates)):
        gates2.append(gates[i + 1])
        plt.text(list(gates2[i])[0], list(gates2[i])[1], str(i + 1), color="red", fontsize=14)
    gates2 = np.array(gates2)
    plt.xlim(0, board.width)
    plt.ylim(-1, board.length)
    plt.scatter(gates2[:, 0], gates2[:, 1], marker = 's')


    # plot grid and routes 
    plt.grid()
   

    print("route: ", route)
    for i in range(len(net_dict)):
        route[i] = np.array(route[i])
        plt.plot(route[i][0:len(route[i]), 0], route[i][0:len(route[i]), 1], marker = ' ') 
    

    # save file
    plt.savefig("output.png")