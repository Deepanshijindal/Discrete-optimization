import math, random
from itertools import product
import time
import heapq, itertools

def calculate_total_distance(tour, distance_matrix):
    """Calculate the total distance of the given tour based on the distance matrix."""
    a = sum(distance_matrix[tour[i]][tour[i+1]] for i in range(len(tour) - 1))
    return a + distance_matrix[tour[0]][tour[-1]]  # Adding the distance to return to the starting city

def two_opt_swap(tour, i, k):
    """Perform a 2-opt swap by reversing the tour segment between indices i and k."""
    new_tour = tour[:i] + tour[i:k+1][::-1] + tour[k+1:]
    return new_tour

def two_opt(tour, distance_matrix):
    """Perform the 2-opt optimization algorithm to improve the given tour."""
    time_limit = 60 * 60 * 2  # Set a time limit of 2 hours
    num_cities = len(tour)
    best_tour = tour
    best_distance = calculate_total_distance(tour, distance_matrix)
    improved = True
    start_time = time.time()  # Record the start time
    
    while improved:
        improved = False
        if time.time() - start_time > time_limit:  # Check if time limit is reached
            break
        for i in range(1, num_cities - 1):
            for k in range(i + 1, num_cities):
                new_tour = two_opt_swap(best_tour, i, k)  # Perform 2-opt swap
                new_distance = calculate_total_distance(new_tour, distance_matrix)
                if new_distance < best_distance:  # If the new tour is better, update the best tour and distance
                    best_tour = new_tour[:]
                    best_distance = new_distance
                    improved = True
                    break
            if improved:
                break

    return best_tour, best_distance  # Return the best tour and its distance

