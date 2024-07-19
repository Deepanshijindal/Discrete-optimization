from collections import namedtuple
import math

# Define Point, Facility, and Customer namedtuples
Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def parse_input(input_data):
    """Parse input data to extract facilities and customers."""
    lines = input_data.split('\n')

    # Read the number of facilities and customers
    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    # Read facility data
    facilities = []
    for i in range(1, facility_count + 1):
        parts = lines[i].split()
        facilities.append(Facility(i - 1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3]))))

    # Read customer data
    customers = []
    for i in range(facility_count + 1, facility_count + 1 + customer_count):
        parts = lines[i].split()
        customers.append(Customer(i - 1 - facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    return facilities, customers
