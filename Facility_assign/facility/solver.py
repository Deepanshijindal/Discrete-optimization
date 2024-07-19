from ortools.linear_solver import pywraplp
from parse_input import length, parse_input
from excel_workbook import write_to_excel

def solve_it(input_data):
    """Solve the facility location problem."""
    facilities, customers = parse_input(input_data)

    # Create the solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return 'Solver not created.'

    # Variables
    x = {} #Initialize dictionaries to hold decision variables.
    y = {}
    for f in facilities:
        y[f.index] = solver.BoolVar(f'y[{f.index}]') #Creates a binary variable y[f.index] indicating if facility f is used.
        for c in customers:
            x[f.index, c.index] = solver.BoolVar(f'x[{f.index},{c.index}]') #Creates a binary variable x[f.index, c.index] indicating if
                                                                               #customer c is assigned to facility f.

    # Objective function
    solver.Minimize(solver.Sum(f.setup_cost * y[f.index] for f in facilities) + 
                    solver.Sum(length(f.location, c.location) * x[f.index, c.index] for f in facilities for c in customers))

    # Constraints
    #Ensures each customer is assigned to exactly one facility.
    for c in customers:
        solver.Add(solver.Sum(x[f.index, c.index] for f in facilities) == 1) 

    #Ensures the total demand assigned to a facility does not exceed its capacity.
    for f in facilities: 
        solver.Add(solver.Sum(c.demand * x[f.index, c.index] for c in customers) <= f.capacity * y[f.index]) 

    #Ensures a customer can only be assigned to a facility if the facility is used.
    for f in facilities:
        for c in customers:
            solver.Add(x[f.index, c.index] <= y[f.index])

    # Solve the problem with a time limit
    solver.set_time_limit(900 * 1000)  # 900 seconds = 15 minutes
    status = solver.Solve()

    # Check if the problem has an optimal solution
    if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
        print('No feasible solution found within the time limit.')
        return 'No solution found.'

    # Extract the solution
    solution = [-1] * len(customers) #Initializes a list to store the facility assigned to each customer.
    used = [0] * len(facilities) #Initializes a list to store whether each facility is used.
    for f in facilities:
        if y[f.index].solution_value() > 0.5:
            used[f.index] = 1
            for c in customers:
                if x[f.index, c.index].solution_value() > 0.5:
                    solution[c.index] = f.index

    # Validate the solution
    for c in customers:
        if solution[c.index] == -1:
            print(f"Warning: Customer {c.index} is not assigned to any facility.")
        # else:
        #     print(f"Customer {c.index} assigned to Facility {solution[c.index]}")

    # Calculate the cost of the solution
    obj = sum(f.setup_cost * used[f.index] for f in facilities)
    for c in customers:
        if solution[c.index] != -1:
            obj += length(c.location, facilities[solution[c.index]].location)

    # Write the detailed solution to an Excel workbook
    write_to_excel(customers, facilities, solution, obj)

    # Prepare the solution in the specified output format
    submission_output = '%.2f' % obj + ' ' + str(0) + '\n'
    submission_output += ' '.join(map(str, solution))

    # Return submission output
    return submission_output

import sys
if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')
