import csv

# read data of csv file input
with open("gates&netlists/chip_0/print_0.csv") as input:
    data = [line for line in csv.reader(input)]

# Skip header first line for chips data, and turn chip data into ints
chips = [list(map(int, chip)) for chip in data[1:]]

max_x = 0
max_y = 0

# Get max x and y values of outermost chips
for coordinates in chips:
    x = int(coordinates[1])
    y = int(coordinates[2])
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y

class bord:
    def __init__(self, chips, nets, width, length):
        self.length = length
        self.width = width
        self.chips = chips
        self.nets = nets
        self.cost = 0

bord1 = bord(chips, [], 8, 7)

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
