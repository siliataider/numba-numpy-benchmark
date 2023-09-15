import subprocess
import csv
import statistics

thread_counts = [1, 2, 3, 4, 5, 6, 7, 8]
num_runs = 10

output_file = '/home/siliataider/Documents/silia-dev-root-project-folder/Benchmarking/numba_average_results.csv'

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Threads', 'Average Real Time (Loop)', 'Median Real Time (Loop)', 
                     'Average CPU Time (Loop)', 'Median CPU Time (Loop)', 
                     'Average Real Time (Numpy)', 'Median Real Time (Numpy)', 
                     'Average CPU Time (Numpy)', 'Median CPU Time (Numpy)'])

for threads in thread_counts:
    real_time_loop_values = []
    cpu_time_loop_values = []
    real_time_numpy_values = []
    cpu_time_numpy_values = []

    for i in range(num_runs):
        print("Run n: ", i)
        command = ['python', '/home/siliataider/Documents/silia-dev-root-project-folder/rootbuild/LiveVisualize_feature-default/tutorials/dataframe/repro_numba.py', str(threads)]
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        print("Run finished")

        output_lines = result.stdout.strip().split('\n')
        real_time_loop, cpu_time_loop = output_lines[0].split(', ')
        real_time_numpy, cpu_time_numpy = output_lines[1].split(', ')

        real_time_parts = real_time_loop.split(':')
        minutes = float(real_time_parts[-2])
        seconds = float(real_time_parts[-1])
        total_seconds = minutes * 60 + seconds
        real_time_loop_values.append(total_seconds)
        cpu_time_loop_values.append(float(cpu_time_loop.split(' ')[-1]))
        real_time_parts = real_time_numpy.split(':')
        minutes = float(real_time_parts[-2])
        seconds = float(real_time_parts[-1])
        total_seconds = minutes * 60 + seconds
        real_time_numpy_values.append(total_seconds)
        cpu_time_numpy_values.append(float(cpu_time_numpy.split(' ')[-1]))

        print("current real_time_loop_values: ", real_time_loop_values)
        print("current cpu_time_loop_values: ", cpu_time_loop_values)
        print("current real_time_numpy_values: ", real_time_numpy_values)
        print("current cpu_time_numpy_values: ", cpu_time_numpy_values)

    avg_real_time_loop = sum(real_time_loop_values) / num_runs
    median_real_time_loop = statistics.median(real_time_loop_values)
    avg_cpu_time_loop = sum(cpu_time_loop_values) / num_runs
    median_cpu_time_loop = statistics.median(cpu_time_loop_values)

    avg_real_time_numpy = sum(real_time_numpy_values) / num_runs
    median_real_time_numpy = statistics.median(real_time_numpy_values)
    avg_cpu_time_numpy = sum(cpu_time_numpy_values) / num_runs
    median_cpu_time_numpy = statistics.median(cpu_time_numpy_values)

    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([threads, avg_real_time_loop, median_real_time_loop, 
                         avg_cpu_time_loop, median_cpu_time_loop, 
                         avg_real_time_numpy, median_real_time_numpy, 
                         avg_cpu_time_numpy, median_cpu_time_numpy])
