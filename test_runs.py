from helper_functions import *
import time
import subprocess
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


csvfile = open(f"output/output_{algorithm[:-3]}.csv", 'w')
csvfile.write("Resultaten:" " Nets/Total nets:" " Total cost:")
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

runs = []
cost = []
# open csv file 
with open(f"output/output_{algorithm[:-3]}.csv") as f:
    # Skip first line
    next(f)
    lines = f.readlines()
    i = 1
    j = 1
    # check several parameters like execution times, net completions and cost
    for line in lines:
        line2 = line.split(",")
        execution_times.append(float(line2[0].strip()))
        cost.append(line2[2])

        line3 = line2[1].split("/")
        runs.append(line3[0].strip())
        # check how many runs of the total are completed
        if line3[0] == line3[1]:
            i+=1 
        j+=1
    

print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("Average execution time: ")
average_exec = average(execution_times)
print(average_exec)
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")


runs = list(map(int, runs))
runs.sort()
execution_times = list(map(float, execution_times))
execution_times.sort()
cost = list(map(int, cost))
cost.sort()


csvfile = open(f"output/output_{algorithm[:-3]}.csv", 'a')
csvfile.write("\n")
csvfile.write("\n")
csvfile.write(f"Algorithm has completed {n_runs} runs  ")
csvfile.write("\n")
csvfile.write("Average execution time: ")
csvfile.write(str(average_exec))
csvfile.write("\n")
csvfile.write("total net completions ")
csvfile.write(str(i) + ("/") + str(j) + (" ") + ("(") + str((i/j)*100) + " %)")
csvfile.write("\n")
csvfile.write("best net completion: ")
csvfile.write(str(runs[0]) + ("/") + (line3[1]))
csvfile.write("\n")
csvfile.write("best execution time: ")
csvfile.write(str(execution_times[0]))
csvfile.write("\n")
csvfile.write("best cost: ")
csvfile.write(str(cost[0]))


