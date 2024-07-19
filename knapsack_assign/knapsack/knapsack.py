from collections import namedtuple

Item = namedtuple("Item", ['index', 'value', 'weight'])

def greedy_knapsack(items, capacity):
    # Sort items by their value to weight ratio in descending order
    items = sorted(items, key=lambda x: x.value / x.weight, reverse=True)
    
    total_value = 0
    total_weight = 0
    taken = [0] * len(items)
    
    for item in items:
        if total_weight + item.weight <= capacity:
            taken[item.index] = 1
            total_value += item.value
            total_weight += item.weight
    
    return total_value, taken

def parse_input(input_data):
    lines = input_data.split('\n')
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []
    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))

    return items, capacity
