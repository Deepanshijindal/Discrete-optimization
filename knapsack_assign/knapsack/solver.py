
# -*- coding: utf-8 -*-

from collections import namedtuple
from knapsack import greedy_knapsack, parse_input
from Dynamic_pro import dynamic_programming_knapsack, parse_input

Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):
    # Parse the input
    items, capacity = parse_input(input_data)
    if len(items) <= 50:
        value, taken = dynamic_programming_knapsack(items, capacity)
    else:
        # Run the greedy knapsack algorithm
        value, taken = greedy_knapsack(items, capacity)
    
    # Prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
