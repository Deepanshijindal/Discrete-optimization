import numpy as np
import random
from collections import namedtuple
# from Utils_general import length, tourSum
from two_opt import apply_2opt  # Importing additional function for local optimization

# Define a named tuple 'Customer' to represent customer attributes
Customer = namedtuple('Customer', ['index', 'demand', 'x', 'y'])

def length(customer1, customer2):
    """
    Parameters:
    - customer1: First customer (namedtuple with attributes 'x' and 'y').
    - customer2: Second customer (namedtuple with attributes 'x' and 'y').
    """
    return np.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def distMatrix(customers, customer_count):
    """
    Parameters:
    - customers: List of Customer namedtuples.
    - customer_count: Total number of customers including the depot.
    """
    dist = [np.array([float(0) for _ in range(0, customer_count)]) for _ in range(0, customer_count)]
    for i in range(0, customer_count):
        for j in range(0, customer_count):
            if i != j:
                dist[i][j] = length(customers[i], customers[j])
                dist[j][i] = dist[i][j]
            else:
                dist[i][j] = float(0)
    return dist

def tourSum(vehicle_tours, depot):
    """
    Parameters:
    - vehicle_tours: List of lists where each sublist represents a vehicle's tour (list of Customer namedtuples).
    - depot: Depot location (Customer namedtuple representing the depot).
    """
    total_sum = 0
    for tour in vehicle_tours:
        if tour:
            tour_distance = length(depot, tour[0])  # Distance from depot to the first customer
            for i in range(len(tour) - 1):
                tour_distance += length(tour[i], tour[i + 1])
            tour_distance += length(tour[-1], depot)  # Distance from last customer back to the depot
            total_sum += tour_distance
    return total_sum

def randOrder(customers, customer_count, vehicle_count, vehicle_capacity):
    """
    Randomized heuristic approach to solve the Vehicle Routing Problem (VRP).

    Parameters:
    - customers: List of Customer namedtuples representing each customer's attributes.
    - customer_count: Total number of customers including the depot.
    - vehicle_count: Number of vehicles available for routing.
    - vehicle_capacity: Maximum capacity of each vehicle.

    Algorithm Details:
    - Initializes with random coefficients (a, b, c) and fixed exponents (d, e, f) for the heuristic function.
    - Iterates up to 10,000 times to find a better solution.
    - Each iteration assigns customers to vehicles based on a heuristic score combining distance, index, and demand factors.
    - Ensures each vehicle does not exceed its capacity.
    - Checks if all customers (except the depot) are visited exactly once.
    - Updates the best solution if a shorter tour distance and feasible assignment are found.
    """

    depot = customers[0]  # Depot is the first customer in the list
    vehicle_tour_best = []  # Initialize variable to store the best vehicle tours found
    dist = distMatrix(customers, customer_count)  # Calculate distance matrix between all customers
    min_tour_sum = float('inf')  # Initialize minimum total tour distance to infinity

    itr = 1
    while itr <= 10000:
        remaining_customers = set(customers)  # Set of remaining customers to be assigned to vehicles
        remaining_customers.remove(depot)  # Remove the depot from the set of remaining customers
        vehicle_tours = []  # List to store tours for each vehicle in current iteration
        itr += 1

        # Random coefficients for the heuristic function
        a = random.randrange(-1000, 1000)
        b = random.randrange(-1000, 1000)
        c = random.randrange(-1000, 1000)
        d = 2
        e = 1
        f = 1

        # Iterate through each vehicle
        for v in range(0, vehicle_count):
            vehicle_tours.append([])  # Initialize an empty tour for the current vehicle
            capacity_remaining = vehicle_capacity  # Initialize remaining capacity for the current vehicle

            # Assign customers to the current vehicle until capacity is reached
            while sum([capacity_remaining >= customer.demand for customer in remaining_customers]) > 0:
                used = set()  # Set to store customers added to the current vehicle's tour

                # Sort remaining customers based on the heuristic function
                order = sorted(remaining_customers,
                               key=lambda customer: a * dist[customer.index][customers[0].index] ** d +
                                                   b * customer.index ** e +
                                                   c * customer.demand ** f,
                               reverse=True)

                # Add customers to the current vehicle's tour while respecting capacity
                for customer in order:
                    if capacity_remaining >= customer.demand:
                        capacity_remaining -= customer.demand
                        vehicle_tours[v].append(customer)
                        used.add(customer)

                remaining_customers -= used  # Remove assigned customers from the set of remaining customers

        # Check if all customers (except depot) are visited exactly once
        condition1 = (sum([len(v) for v in vehicle_tours]) == (len(customers) - 1))

        # Calculate the total tour distance of the current solution
        curr_tour_sum = tourSum(vehicle_tours, depot)

        # Update the best solution if a shorter tour distance and feasible assignment are found
        if min_tour_sum > curr_tour_sum and condition1:
            vehicle_tour_best = vehicle_tours.copy()
            min_tour_sum = curr_tour_sum

    return vehicle_tour_best, min_tour_sum
