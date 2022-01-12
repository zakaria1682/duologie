import csv

# read data of csv file input
with open("gates&netlists/chip_0/print_0.csv") as input:
    data = [line for line in csv.reader(input)]

# Skip header first line
chips = data[1:]

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


# Create grid. Make row with 1 extra space at each end of row.
# Add these rows two grid, with 1 extra row at eacht vertical end of grid
grid = []

for i in range(0, max_y + 2):
    row = []
    for i in range(0, max_x + 2):
        row.append(0)

    grid.append(row)


for chip in chips:
    chip_x, chip_y = (int(chip[1]), int(chip[2]))
    print(chip_x, chip_y)

    grid[max_y - chip_y + 1][chip_x] = int(chip[0])


for row in grid:
    print(row)

