from helper_functions import *
import time
import subprocess
import os
import sys



if len(sys.argv) < 2:
    print("No upperbound(s) given")
    print("Usage: python test_runs.py [#seconds to run algorithm in total]", 
          "[#seconds allowed for each run of algorithm]")
    exit()

total_run_time = int(sys.argv[1])
time_for_each_exec = int(sys.argv[2])

# # create empty csv file
# with open('execution_times.csv', "w") as csvfile:
#     pass

csvfile = open('output/output.csv', 'w')
csvfile.write("Resultaten:")
csvfile.close()

n_runs = 1
execution_times = []
start_time = time.time()

# call the algorithm while time is under a certain limit
while time.time() - start_time < total_run_time:
    print(f"run: {n_runs}")
    subprocess.call(["timeout", str(time_for_each_exec), "python3", "BFS.py"])
    n_runs += 1



# open csv file 
with open('execution_times.csv') as f:
            new_line = f.readline().strip("\n")
            execution_times.append(float(new_line))


print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("Average execution time: ")
average_exec = average(execution_times)
print(average_exec)
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")

