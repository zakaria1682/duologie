import csv

class net:
    def __init__(self, start, destination):
        self.wires = []
        self.start = start
        self.destination = destination
        cost = 0

class board:
    def __init__(self, chips):
        # Get max x and y values of outermost chips
        max_x, max_y = (0, 0)
        for coordinates in chips:
            x = coordinates[1]
            y = coordinates[2]
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
        
        # set board dimensions according to max x & y
        # x & y + 2 to create extra ring of space around chip configuration
        self.width = max_x + 2
        self.length = max_y + 2
        self.chips = chips
        self.nets = []
        self.cost = 0


# read data of csv file input
with open("gates&netlists/chip_0/print_0.csv") as input:
    data = [line for line in csv.reader(input)]

# Skip header first line for chips data, and turn chip data into ints
chips = [list(map(int, chip)) for chip in data[1:]]


bord1 = board(chips)

print("Bord breedte: ", bord1.width)
print("Bord lengte: ", bord1.length)
print("")


def print_board(board):
    for y in range(board.length - 1, -1, -1):
        row = []

        for x in range(0, board.width):
            al_geprint = False

            for chip in board.chips:
                
                if (chip[1], chip[2]) == (x, y):
                    print("", chip[0], "", end = '')
                    al_geprint = True
            
            if al_geprint == False:            
                print(" + ", end = '')

        print("\n")


print_board(bord1)


