import pandas as pd
import numpy as np

def generate_distance_matrix(csv_path):
    # Read CSV data
    df = pd.read_csv(csv_path)
    coords = df[['lat', 'lng']].to_numpy()
    
    # Calculate Euclidean distances scaled to a approximate meters (1 deg lat ~ 111,000 m)
    num_points = len(coords)
    matrix = []
    
    for i in range(num_points):
        row = []
        for j in range(num_points):
            if i == j:
                row.append(0)
            else:
                # Euclidean distance converted roughly to meters for simulation
                lat_diff = (coords[i][0] - coords[j][0]) * 111000
                lng_diff = (coords[i][1] - coords[j][1]) * 111000
                dist = int(np.sqrt(lat_diff**2 + lng_diff**2))
                row.append(dist)
        matrix.append(row)
        
    return matrix, df

if __name__ == "__main__":
    matrix, df = generate_distance_matrix("locations.csv")
    print("Generated Distance Matrix (Meters):")
    for row in matrix:
        print(row) 

