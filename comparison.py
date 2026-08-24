from main import main
from map_visualizer import generate_route_map


def getNumRoutes(Data, Routing, Manager, Solution):
    numRoutes = 0
    routes_dict = {}
    for vehicle_id in range(Data["num_vehicles"]):
        index = Routing.Start(vehicle_id)
        route_nodes = []
        route_distance = 0
        while not Routing.IsEnd(index):
            node = Manager.IndexToNode(index)
            route_nodes.append(node)
            previous_index = index
            index = Solution.Value(Routing.NextVar(index))
            route_distance += Routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        node = Manager.IndexToNode(index)
        route_nodes.append(node)
        routes_dict[vehicle_id] = route_nodes
        if route_distance != 0:
            numRoutes+=1
    return Data, routes_dict, numRoutes




def computeDiff():
    trueSol, trueData, trueManager, trueRouting, true_time_dimension = main(True)
    falseSol, falseData, falseManager, falseRouting, false_time_dimension = main(False)

    if not (trueSol and falseSol):
        with open("output.txt", "w", encoding = "utf-8") as file:
            file.write("No Solution Found")
        return
    
    #find the distance for colaborative and independent versions and caclulate the percent difference
    trueVal = float(trueSol.ObjectiveValue())
    falseVal = float(falseSol.ObjectiveValue())
    dist_diff = (falseVal - trueVal) / falseVal * 100
    dist_diff = round(dist_diff, 2)
    
    #find active routes for collaborative version
    Data, routes_dict, trueRoutes = getNumRoutes(trueData, trueRouting, trueManager, trueSol)
    generate_route_map(Data["csv_path"], routes_dict, "collaborative_map.html")

    #find active routes for independent version
    Data, routes_dict, falseRoutes = getNumRoutes(falseData, falseRouting, falseManager, falseSol)
    generate_route_map(Data["csv_path"], routes_dict, "independent_map.html")


    # write to output file
    with open("output.txt", "w", encoding = "utf-8") as file:
        file.write(f"Difference in distance: {dist_diff}% decrease\n")
        file.write(f"The collaborative version had {falseRoutes-trueRoutes} less routes than the Independent verion\n")



if __name__ == "__main__":
    computeDiff()





