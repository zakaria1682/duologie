from helper_functions import *
import time
import subprocess
import os
import pandas as pd

# remove existing test csv file
os.remove('execution_times.csv')

# create empty csv file
with open('execution_times.csv', "w") as csvfile:
    pass
    

n_runs = 0
execution_times = []
start_time = time.time()
# call the algoritme while time is under a certain limit
while time.time() - start_time < 20:
    print(f"run: {n_runs}")
    subprocess.call(["timeout", "1", "python3", "BFS.py"])
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

