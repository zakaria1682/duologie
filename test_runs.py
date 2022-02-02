import time
import subprocess


start = time.time()
n_runs = 0
execution_times = []
start = time.time()
while time.time() - start < 60:
    print(f"run: {n_runs}")
    subprocess.call(["timeout", "1", "python3", "BFS.py"])
    n_runs += 1

    exec_time = (time.time() - start_time)
    execution_times.append(exec_time)

    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("Average execution time: ")
    average_exec = average(execution_times)
    print(average_exec)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")