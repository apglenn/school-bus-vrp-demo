import pandas as pd
import numpy as np
import requests
import json

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
    coordString = ""

    demands = df['student_demand'].tolist()
    district = df['district'].tolist()
    time_windows = list(zip(df['earliest_time'], df['latest_time']))
    # Calculate Euclidean distances scaled to a approximate meters (1 deg lat ~ 111,000 m)
    is_depot_list = df['is_depot'].tolist()
 
    boarding_time = 3

    for lat, lng in coords:
        coordString += str(lng) +',' +str(lat) + ';' 
    coordString = coordString[0:-1]
    url = f"http://router.project-osrm.org/table/v1/driving/{coordString}"
    try:
        response = requests.get(url, params={"annotations": "distance,duration"}, timeout=10)
        print("status:", response.status_code)
        response.raise_for_status()
        data = response.json()
        print("OSRM code:", data.get("code"))
        response.raise_for_status()  # raises an error if OSRM returns a bad status code (e.g. 500)
        data = response.json()
        distance_matrix = data["distances"]
        time_matrix = [[(t / 60) + boarding_time for t in row] for row in data["durations"]]
        distance_matrix = [[int(d) for d in row] for row in data["distances"]]
    except requests.exceptions.RequestException as e:
        print(f"OSRM request failed: {e}")
        distance_matrix, time_matrix = None, None




    
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
