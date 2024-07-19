import math, random
from itertools import product
import heapq, itertools 

def multi_fragment_heuristic(distance_matrix):
    """
    Implements a multi-fragment heuristic to solve the Traveling Salesman Problem (TSP).

    Args:
    - distance_matrix (list of lists): Matrix representing distances between cities.

    Returns:
    - final_tour (list): List of city indices representing the final tour.
    """

    num_cities = len(distance_matrix)
    edges = []
    

    # Create a list of all edges with their distances
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            heapq.heappush(edges, (distance_matrix[i][j], i, j))
    
    # Union-Find data structure initialization
    parent = list(range(num_cities))
    rank = [0] * num_cities
    degree = [0] * num_cities
    tour = []

    # Find function for Union-Find
    def find(u): # it will show the parent of a node
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]

    # Union function for Union-Find
    def union(u, v):    # It will check wheather the parent of two nodes is same or not if not it will check the rank of the nodes and add 
                                 # the component having less rank in other component.
        root_u = find(u)
        root_v = find(v)
        if root_u != root_v:
            if rank[root_u] > rank[root_v]:
                parent[root_v] = root_u
            elif rank[root_u] < rank[root_v]:
                parent[root_u] = root_v
            else:
                parent[root_v] = root_u
                rank[root_u] += 1
    
    # Add edges to the tour
    while edges:
        weight, u, v = heapq.heappop(edges)
        if degree[u] < 2 and degree[v] < 2 and find(u) != find(v): # checking the degree of node to avoid unwanted cycles and parents.
            union(u, v)
            tour.append((u, v))
            degree[u] += 1
            degree[v] += 1

    # Convert edge list to tour list using adjacency list representation
    tour_dict = [[] for _ in range(len(distance_matrix[0]))] # kind of adjacency list that will keep track of the connected nodes, for example
                                                               # tour_dict[u] is the list of all the nodes connected with node u. 
    for u, v in tour:
        tour_dict[u].append(v)   #adding all the tuples in tour to tour_dict adjancency list.
        tour_dict[v].append(u)

    # Create the final tour starting from a city with degree 1
    for i in range(len(distance_matrix[0])):
        if degree[i] == 1:
            start = i
            break
    visited = [False] * num_cities # boolean list that will show the node is visited or not
    final_tour = []
    current = start
    while len(final_tour) < num_cities: 
        final_tour.append(current)
        visited[current] = True
        for neighbor in tour_dict[current]:
            if not visited[neighbor]:
                current = neighbor
                break

    return final_tour
