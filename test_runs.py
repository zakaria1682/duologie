from helper_functions import *
import time
import subprocess
import os
import pandas as pd


df = pd.DataFrame(list())
df.to_csv('execution_times.csv')

n_runs = 0
execution_times = []
start_time = time.time()
while time.time() - start_time < 20:
    print(f"run: {n_runs}")
    
    start_time = time.time()
    subprocess.call(["timeout", "1", "python3", "BFS.py"])
    n_runs += 1

with open('execution_times.csv') as f:
            new_line = f.readline().strip("\n")
            execution_times.append(float(new_line))


print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("Average execution time: ")
average_exec = average(execution_times)
print(average_exec)
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")

os.remove('execution_times.csv')