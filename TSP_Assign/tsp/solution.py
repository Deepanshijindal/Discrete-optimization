import math, random
from itertools import product
import heapq, itertools 
from Two_opt import two_opt
from Two_opt import calculate_total_distance
from Nearest_neigbour import length,nearest_neighbor
from Multi_fragment import multi_fragment_heuristic

def solution2(points):
    distance_matrix = [[0 for _ in range(len(points))] for _ in range(len(points))]

    for i, j in product(range(len(points)), range(len(points))):
        distance_matrix[i][j] = length(points[i],points[j])
 
    # for first four cases using multi fragment heuristic and then two opt
    if len(points) <1800:
        current_tour = multi_fragment_heuristic(distance_matrix)
        current_distance = calculate_total_distance(current_tour, distance_matrix)
        return two_opt(current_tour, distance_matrix)
    
    # For 5th test case using only multi fragment heuristic
    elif len(points)> 1800 and len(points)<2000:
        current_tour = multi_fragment_heuristic(distance_matrix)
        current_distance = calculate_total_distance(current_tour, distance_matrix)
        return current_tour, current_distance 


    # For 6th test case, using nearest neighbour greedy approach only
    TOUR = nearest_neighbor(len(points),points)
    distance = calculate_total_distance(TOUR, distance_matrix)
    print(distance)
    return TOUR, distance
    # return random_two_opt(TOUR, distance_matrix)
