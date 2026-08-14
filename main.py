# Based on Google OR-Tools Vehicle Routing Problem (VRP) official documentation.
# Adapted for school transportation planning modeling.


from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from matrix_generator import generate_distance_matrix
from map_visualizer import generate_route_map

# STEP 1: CREATE THE DATA       
def create_data_model():
    data = {}
    starts, ends, distance_matrix, time_matrix, demands, time_windows = generate_distance_matrix("locations.csv")

    data["distance_matrix"] = distance_matrix
    data["time_matrix"] = time_matrix
    data["demands"] = demands
    data["vehicle_capacities"] = [30]*len(starts)
    data["num_vehicles"] = len(starts)
    data["vehicle_starts"] = starts
    data["vehicle_ends"] = ends
    data["max_wait_time"] = 15
    data["max_route_time"] = 120
    data["time_windows"] = time_windows

    return data

# Main Solver Function
def main():
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager: (number of locations, number of vehicles, depot index)
    manager = pywrapcp.RoutingIndexManager(len(data["distance_matrix"]), data["num_vehicles"], data["vehicle_starts"], data["vehicle_ends"])
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)
    for v in range(data["num_vehicles"]):
       print(f"Vehicle {v}: start_index={routing.Start(v)}, end_index={routing.End(v)}")
    print(manager.NodeToIndex(0))

    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

    routing.AddDimensionWithVehicleCapacity(demand_callback_index, 0, data["vehicle_capacities"], True, "Capacity")
    capacity_dimension = routing.GetDimensionOrDie("Capacity")
 
    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["time_matrix"][from_node][to_node]

    twoStop_index = routing.RegisterTransitCallback(time_callback)
    routing.AddDimension(twoStop_index, data["max_wait_time"], data["max_route_time"], True, "Time")

    time_dimension = routing.GetDimensionOrDie("Time")

    for node_index in range(len(data["distance_matrix"])):
        index = manager.NodeToIndex(node_index)

        earliest_time = data["time_windows"][node_index][0]
        latest_time = data["time_windows"][node_index][1]
        time_dimension.CumulVar(index).SetRange(earliest_time, latest_time)


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
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)

    # Print results
    if solution:
        print(f"Objective: {solution.ObjectiveValue()} meters total distance\n")
        routes_dict = {}
        for vehicle_id in range(data["num_vehicles"]):
            index = routing.Start(vehicle_id)
            route_nodes = []
            plan_output = f"Route for Vehicle {vehicle_id}:\n"
            route_distance = 0
            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route_nodes.append(node)
                load = solution.Value(capacity_dimension.CumulVar(index))
                time_var = solution.Value(time_dimension.CumulVar(index))
                plan_output += f" Location {manager.IndexToNode(index)} -> "
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
            node = manager.IndexToNode(index)
            route_nodes.append(node)
            routes_dict[vehicle_id] = route_nodes

            time_val = solution.Value(time_dimension.CumulVar(index))
            plan_output += f"Location {manager.IndexToNode(index)}\n"
            plan_output += f"Distance of route: {route_distance}m\n"
            print(plan_output)
        generate_route_map("locations.csv", routes_dict)
    else:
        status_code = routing.status()
        status_names = {
            0: "ROUTING_NOT_SOLVED (Problem not solved yet)",
            1: "ROUTING_SUCCESS (Found a solution)",
            2: "ROUTING_FAIL (No solution exists that satisfies all constraints)",
            3: "ROUTING_FAIL_TIMEOUT (Timed out before finding a solution)",
            4: "ROUTING_INVALID (Model or constraints are invalid/contradictory)"
        }
        reason = status_names.get(status_code, f"Unknown Status Code: {status_code}")
        print(f"No solution found! Reason: {reason}")

if __name__ == "__main__":
    main()



