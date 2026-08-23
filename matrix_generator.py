import pandas as pd
import numpy as np

def generate_distance_matrix(csv_path):
    # Read CSV data
    df = pd.read_csv(csv_path)
    garage_rows = df[df['is_depot'] == 1]
    garage_node_by_district = dict(zip(garage_rows['district'], garage_rows.index))
    num_vehicles = 2
    starts = []
    ends = []
    for key, value in garage_node_by_district.items():
        for i in range(num_vehicles):
            starts.append(value)
    ends = starts.copy()
    coords = df[['lat', 'lng']].to_numpy()
    demands = df['student_demand'].tolist()
    district = df['district'].tolist()
    time_windows = list(zip(df['earliest_time'], df['latest_time']))
    # Calculate Euclidean distances scaled to a approximate meters (1 deg lat ~ 111,000 m)
    is_depot_list = df['is_depot'].tolist()
    num_points = len(coords)
    distance_matrix = []
    time_matrix = []

    meters_per_min = 600
    boarding_time = 3
    
    for i in range(num_points):
        dist_row = []
        time_row = []
        for j in range(num_points):
            if i == j:
                dist_row.append(0)
                time_row.append(0)
            else:
                # Euclidean distance converted roughly to meters for simulation
                lat_diff = (coords[i][0] - coords[j][0]) * 111000
                lng_diff = (coords[i][1] - coords[j][1]) * 111000
                dist = int(abs(lat_diff) + abs(lng_diff))
                travel_time = int(dist / meters_per_min) + boarding_time
                dist_row.append(dist)
                time_row.append(travel_time)
        distance_matrix.append(dist_row)
        time_matrix.append(time_row)
        
    return district, starts, ends, distance_matrix, time_matrix, demands, time_windows, is_depot_list

if __name__ == "__main__":
    district, starts, ends, distance_matrix, time_matrix, demands, time_windows, is_depot_list = generate_distance_matrix("locations.csv")
    print("Generated Distance Matrix (Meters):")
    for row in distance_matrix:
        print(row) 

    print()

    print("Generated Time matrix (Minutes):")
    for row in time_matrix:
        print(row)
