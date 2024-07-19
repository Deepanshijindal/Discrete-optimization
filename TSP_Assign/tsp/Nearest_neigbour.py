import math, random

def length(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def nearest_neighbor(nodeCount, points):
    """
    Implement the nearest neighbor heuristic to find an initial tour for the TSP.

    Args:
    - nodeCount (int): Number of nodes (cities).
    - points (list of namedtuples): List of points (coordinates of cities).

    Returns:
    - tour (list): List representing the initial tour based on the nearest neighbor heuristic.
    """

    unvisited = set(range(nodeCount))  # Set of all unvisited cities
    tour = [unvisited.pop()]  # Start tour with a random city and remove it from unvisited

    while unvisited:
        last = tour[-1]  # Last visited city in the tour
        # Find the nearest unvisited city to the last visited city
        next_city = min(unvisited, key=lambda city: length(points[last], points[city]))
        tour.append(next_city)  # Add the nearest city to the tour
        unvisited.remove(next_city)  # Remove the city from unvisited set

    return tour  # Return the initial tour based on nearest neighbor heuristic
