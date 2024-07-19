# from openpyxl import Workbook
# from parse_input import length

# def write_to_excel(customers, facilities, solution, total_cost):
#     """
#     Write the detailed solution to an Excel workbook.

#     Args:
#     customers: List of Customer namedtuples.
#     facilities: List of Facility namedtuples.
#     solution: List indicating the facility assigned to each customer.
#     total_cost: The total cost of the solution.
#     """
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Solution"

#     # Add headers
#     ws.append(['Customer', 'Assigned Facility', 'Distance Cost'])

#     # Add customer assignments
#     for c in customers:
#         assigned_facility = solution[c.index]
#         if assigned_facility != -1:
#             distance_cost = length(c.location, facilities[assigned_facility].location)
#             ws.append([c.index, assigned_facility, distance_cost])
#         else:
#             ws.append([c.index, 'Not assigned', 'N/A'])

#     # Add total cost
#     ws.append([])
#     ws.append(['Total Cost', total_cost])

#     # Save the workbook
#     wb.save("facility_location_solution.xlsx")

from openpyxl import Workbook
from parse_input import length

def write_to_excel(customers, facilities, solution, total_cost):
    """
    Write the detailed solution to an Excel workbook.

    Args:
    customers: List of Customer namedtuples.
    facilities: List of Facility namedtuples.
    solution: List indicating the facility assigned to each customer.
    total_cost: The total cost of the solution.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Solution"

    # Add headers
    ws.append(['Customer', 'Assigned Facility', 'Distance Cost'])

    # Add customer assignments
    for c in customers:
        assigned_facility = solution[c.index]
        if assigned_facility != -1:
            distance_cost = length(c.location, facilities[assigned_facility].location)
            ws.append([c.index, assigned_facility, distance_cost])
        else:
            ws.append([c.index, 'Not assigned', 'N/A'])

    # Add total cost
    ws.append([])
    ws.append(['Total Cost', total_cost])

    # Save the workbook
    try:
        wb.save("facility_location_solution.xlsx")
        print("Excel file created successfully.")
    except Exception as e:
        print(f"An error occurred while saving the Excel file: {e}")
