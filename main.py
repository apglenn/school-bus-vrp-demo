# Based on Google OR-Tools Vehicle Routing Problem (VRP) official documentation.
# Adapted for school transportation planning modeling.


from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# STEP 1: CREATE THE DATA
def create_data_model():
    """Stores the data for the problem."""
    data = {}
    # Distance matrix in meters between 4 locations (Location 0 is Depot)
    data["distance_matrix"] = [
        [0, 548, 776, 696],  # From Location 0 (Depot) to others
        [548, 0, 684, 308],  # From Location 1 to others
        [776, 684, 0, 993],  # From Location 2 to others
        [696, 308, 993, 0],  # From Location 3 to others
    ]
    data["num_vehicles"] = 2  # We have 2 buses
    data["depot"] = 0         # All buses start and end at Location 0
    return data

# Main Solver Function
def main():
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager: (number of locations, number of vehicles, depot index)
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Tell the solver how to calculate the distance between any two locations
    def distance_callback(from_index, to_index):
        # Convert from solver internal index to matrix node index
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc (distance traveled)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Set search strategy (first solution heuristic)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)

    # Print results
    if solution:
        print(f"Objective: {solution.ObjectiveValue()} meters total distance\n")
        for vehicle_id in range(data["num_vehicles"]):
            index = routing.Start(vehicle_id)
            plan_output = f"Route for Vehicle {vehicle_id}:\n"
            route_distance = 0
            while not routing.IsEnd(index):
                plan_output += f" Location {manager.IndexToNode(index)} -> "
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id
                )
            plan_output += f"Location {manager.IndexToNode(index)}\n"
            plan_output += f"Distance of route: {route_distance}m\n"
            print(plan_output)
    else:
        print("No solution found!")

if __name__ == "__main__":
    main()


