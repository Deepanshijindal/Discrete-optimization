
import math
from collections import namedtuple

Customer = namedtuple('Customer', ['index', 'demand', 'x', 'y'])

def euclidean_distance(customer1, customer2):
    """Calculate the Euclidean distance between two customers."""
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def calculate_savings(customers, depot):
    """
    Calculate the savings for each pair of customers based on the distance
    between the depot and each customer, and the distance between two customers.
    """
    savings = {}
    for i in range(len(customers)):
        for j in range(i + 1, len(customers)):
            savings[(customers[i].index, customers[j].index)] = (
                euclidean_distance(depot, customers[i]) +
                euclidean_distance(depot, customers[j]) -
                euclidean_distance(customers[i], customers[j])
            )
    return savings

def merge_routes(route1, route2, depot, capacity):
    """
    Merge two routes by connecting the end of route1 with the start of route2.
    The merged route is checked to ensure it does not exceed the capacity constraint.
    """
    merged_route = [depot] + route1[::-1] + route2 + [depot]  # List of customer named tuples
    merged_demand = sum(customer.demand for customer in merged_route) 
    if merged_demand <= capacity: # Checking the constraint of vehicle capacity
        merged_route.pop(0) # removing depot from start and end
        merged_route.pop(-1)
        return merged_route
    return None

def clarke_wright(customers, vehicle_count, vehicle_capacity):
    depot = customers[0]

    # Calculate the savings for each pair of customers
    savings = calculate_savings(customers[1:], depot)
    savings_sorted = sorted(savings.items(), key=lambda item: item[1], reverse=True)

    # Create a route for each customer, initially with one customer in each route
    routes = [[customer] for customer in customers[1:]]

    merged = True
    while merged:
        merged = False
        savings_temp = savings_sorted.copy()

        while savings_temp:
            (customer_i, customer_j), _ = savings_temp[0]

            # Find the routes containing the customers in the max savings pair
            route_i = next(route for route in routes if customer_i in [c.index for c in route]) # next() is used to find the first route that 
            route_j = next(route for route in routes if customer_j in [c.index for c in route])             #contains a specific customer.

            if route_i != route_j:  # If the customers are in different routes
                new_route = merge_routes(route_i, route_j, depot, vehicle_capacity)
                if new_route:
                    routes.remove(route_i)
                    routes.remove(route_j)
                    routes.append(new_route)
                    merged = True

            savings_temp.pop(0)

    if vehicle_count >= len(routes):
        return routes, depot

    return [], -1

