from collections import namedtuple

Item = namedtuple("Item", ['index', 'value', 'weight'])

def dynamic_programming_knapsack(items, capacity):
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Fill dp table
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if items[i-1].weight <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - items[i-1].weight] + items[i-1].value)
            else:
                dp[i][w] = dp[i-1][w]

    # Traceback to find the items to include in the knapsack
    w = capacity
    taken = [0] * n
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            taken[items[i-1].index] = 1
            w -= items[i-1].weight

    total_value = dp[n][capacity]
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
