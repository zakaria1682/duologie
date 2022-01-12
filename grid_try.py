import csv

# read file
file = open('gates&netlists/chip_0/print_0.csv')
# make header 
csvreader = csv.reader(file)
header = []
header = next(csvreader)

# make rows
rows = []
for row in csvreader:
    rows.append(row[1: ])
print(rows)


# Initialize matrix 
matrix = [] 
  
# For user input 
for i in range(8):          # row entries 
    a =[] 
    for j in range(8):      # column entries 
        a.append(0) 
          
    matrix.append(a) 


n = 1
for i in range(8):         
    a =[] 
    for j in range(8):      
        for q in range(len(rows)):
            # print([i,j])
            # print(rows[q])
            if rows[q] == [str(i),str(j)]:
                print(rows[q])
                print([i,j])
                matrix[7-j][i] = n
                n += 1
        


for row in matrix:
    print(row)
   


            
