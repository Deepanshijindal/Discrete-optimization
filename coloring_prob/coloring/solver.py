#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict
import heapq

class Graph:
    def __init__(self, V):
        self.V = V
        self.graph = defaultdict(list)
    
    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

class VertexInfo:
    def __init__(self, sat, deg, vertex):
        self.sat = sat
        self.deg = deg
        self.vertex = vertex
    
    def __lt__(self, other):
        return (self.sat, self.deg, self.vertex) > (other.sat, other.deg, other.vertex)

def dsatur(graph):
    V = graph.V
    color = [-1] * V
    d = [len(graph.graph[i]) for i in range(V)]
    adj_cols = [set() for _ in range(V)]
    pq = []
    
    for u in range(V):
        heapq.heappush(pq, VertexInfo(0, d[u], u))
    
    while pq:
        u = heapq.heappop(pq).vertex

        # Find the first available color
        used = [False] * V
        for v in graph.graph[u]:
            if color[v] != -1:
                used[color[v]] = True

        cr = 0
        while cr < V and used[cr]:
            cr += 1

        color[u] = cr

        # Update the saturation degree of the neighbors
        for v in graph.graph[u]:
            if color[v] == -1:
                if cr not in adj_cols[v]:
                    adj_cols[v].add(cr)
                    new_info = VertexInfo(len(adj_cols[v]), d[v], v)
                    heapq.heappush(pq, new_info)

    return color


def solve_it(input_data):
    # Parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # Create graph and add edges
    graph = Graph(node_count)
    for u, v in edges:
        graph.add_edge(u, v)

    # Get the color assignment using DSATUR algorithm
    colors = dsatur(graph)

    # Prepare the solution in the specified output format
    max_color = max(colors) + 1
    output_data = str(max_color) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, colors))

    return output_data
# !/usr/bin/python
# -*- coding: utf-8 -*-

# def is_valid(node, color, colors, graph):
#     for neighbor in graph.edges[node]:
#         if colors[neighbor] == color:
#             return False
#     return True

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file. Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

