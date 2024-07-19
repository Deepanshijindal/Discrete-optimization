import time

def calculate_total_distance(tour, distance_matrix):
    return sum(distance_matrix[tour[i]][tour[i+1]] for i in range(len(tour)-1))

def two_opt_swap(tour, i, k):
    """Perform a 2-opt swap by reversing the tour segment between indices i and k."""
    new_tour = tour[:i] + tour[i:k+1][::-1] + tour[k+1:]
    return new_tour

def calculate_improvement(tour, new_tour, distance_matrix):
    old_distance = calculate_total_distance(tour, distance_matrix)
    new_distance = calculate_total_distance(new_tour, distance_matrix)
    return old_distance - new_distance

def apply_2opt(vehicle_tours, customers, distance_matrix):
    """
    Applies the 2-opt algorithm to improve the vehicle tours by iteratively swapping edges.

    Args:
        vehicle_tours (list): A list of vehicle tours, where each tour is a list of customer indices.
        customers (list): A list of customer nodes, including the depot.
        distance_matrix (list of list): Distance matrix representing the distances between all customer pairs.

    Returns:
        list: The updated vehicle tours after applying 2-opt.
    """
    for vehicle_num, tour in enumerate(vehicle_tours):
        tour = [0] + [customer.index for customer in tour]  # Add the depot to the beginning of the tour
        num_cities = len(tour)
        improved = True

        while improved:
            improved = False
            for i in range(1, num_cities - 2):
                for k in range(i + 1, num_cities - 1):
                    new_tour = two_opt_swap(tour, i, k)
                    improvement = calculate_improvement(tour, new_tour, distance_matrix)
                    if improvement > 0:
                        tour = new_tour[:]
                        improved = True
                        break
                if improved:
                    break

        vehicle_tours[vehicle_num] = [customers[idx] for idx in tour[1:]]  # Remove the depot from the tour

    return vehicle_tours

