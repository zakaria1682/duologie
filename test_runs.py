from helper_functions import *
import time
import subprocess
import os
import sys



if len(sys.argv) != 5:
    print("One or more arguments missing")
    print("Usage: python test_runs.py", 
          "[Name of file containing algorithm]",
          "[Netlist# to solve]", 
          "[#seconds to run in total]", 
          "[#seconds allowed for each run]")
    exit()


algorithm = sys.argv[1]
netlist_num = int(sys.argv[2])
total_run_time = int(sys.argv[3])
time_for_each_exec = int(sys.argv[4])

if netlist_num < 4:
    chip_num = 0
elif netlist_num < 7:
    chip_num = 1
else:
    chip_num = 2


csvfile = open('output/output.csv', 'w')
csvfile.write("Resultaten:")
csvfile.close()

n_runs = 1
execution_times = []
start_time = time.time()

# call the algorithm while time is under a certain limit
while time.time() - start_time < total_run_time:
    print(f"run: {n_runs}")
    subprocess.call(["timeout", 
                     str(time_for_each_exec), 
                     "python3", 
                     algorithm, 
                     str(chip_num), 
                     str(netlist_num)]
                     )
    n_runs += 1


# open csv file 
with open('output/output.csv') as f:
    # Skip first line
    next(f)
    lines = f.readlines()

    for line in lines:
        execution_times.append(float(line.strip()))



print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("Average execution time: ")
average_exec = average(execution_times)
print(average_exec)
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")

