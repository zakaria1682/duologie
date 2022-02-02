from helper_functions import *
import time
import subprocess


n_runs = 0
execution_times = []
while time.time() - start_time < 60:
    print(f"run: {n_runs}")
    
    start_time = time.time()
    subprocess.call(["timeout", "1", "python3", "BFS.py"])
    exec_time = (time.time() - start_time)

    execution_times.append(exec_time)
    n_runs += 1

print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("Average execution time: ")
average_exec = average(execution_times)
print(average_exec)
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")