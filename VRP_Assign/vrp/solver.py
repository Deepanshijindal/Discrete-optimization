import math
from collections import namedtuple
from clarke_wright import clarke_wright, Customer
from two_opt import apply_2opt
from rand_order import randOrder, length


def calculate_total_distance(tour, distance_matrix):
    return sum(distance_matrix[tour[i]][tour[i+1]] for i in range(len(tour)-1))


def solve_it(input_data):
    # Parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
   
    customers = []
    for i in range(1, customer_count + 1):
        parts = lines[i].split()
        customers.append(Customer(i - 1, int(parts[0]), float(parts[1]), float(parts[2])))
 
    # Solve the VRP using Clarke-Wright Savings algorithm
    routes, depot = clarke_wright(customers, vehicle_count, vehicle_capacity)

    if not routes:
        # If Clarke-Wright fails, use the randomized heuristic approach
        routes, tour_sum = randOrder(customers, customer_count, vehicle_count, vehicle_capacity)
        if not routes:
            return '0.00 -1\n'

    # Prepare distance matrix
    distance_matrix = [[length(c1, c2) for c1 in customers] for c2 in customers]

    # Apply 2-opt optimization to each route
    optimized_routes = apply_2opt(routes, customers, distance_matrix)
    # optimized_routes = routes

    # Ensure all customers are included in the solution
    all_customers_in_routes = set()
    for route in optimized_routes:
        for customer in route:
            all_customers_in_routes.add(customer.index)

    if len(all_customers_in_routes) != customer_count - 1:
        return '0.00 -1\n'

    # If there are fewer routes than vehicles, add empty routes
    while len(optimized_routes) < vehicle_count:
        optimized_routes.append([])

    total_distance = 0
    for route in optimized_routes:
        tour = [customers[0].index] + [customer.index for customer in route] + [customers[0].index] # add depot at the start and end
        total_distance += calculate_total_distance(tour, distance_matrix)

    # Prepare the solution in the specified output format for terminal
    terminal_output = f'{total_distance:.2f} 0\n'
    for route in optimized_routes:
        terminal_output += '0 ' + ' '.join(str(customer.index) for customer in route) + ' 0\n'

    # Write output to file named "output.txt" with additional descriptive lines
    output_data = f'Optimal total route distance: {total_distance:.2f}\n'
    output_data += 'Vehicle routes:\n'
    for route in optimized_routes:
        output_data += '0 ' + ' '.join(str(customer.index) for customer in route) + ' 0\n'

    with open('output.txt', 'w') as output_file:
        output_file.write(output_data)

    return terminal_output

import sys
if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file. Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')
