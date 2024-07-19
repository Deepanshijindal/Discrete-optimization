import itertools
import math
import time
from collections import namedtuple
import pandas as pd
from solution import solution2

Point = namedtuple("Point", ['x', 'y'])

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount + 1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    obj = 0

    # optimize the solution using 2-opt with a time limit of 30 minutes
    start_time = time.time()
    optimized_solution, obj = solution2(points)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, optimized_solution))

    # Create a structured output in an Excel file
    summary_data = {
        'Description': ['Optimal Solution Total Distance of Tour'],
        'Value': [obj]
    }
    summary_df = pd.DataFrame(summary_data)
    tour_df = pd.DataFrame({
        'Tour': optimized_solution
    })

    # Save to Excel
    with pd.ExcelWriter('output.xlsx') as writer:
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        tour_df.to_excel(writer, sheet_name='Tour', index=False)

    return output_data

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file. Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
