import folium
import pandas as pd

def generate_route_map(csv_path, routes, output_html="route_map.html"):
    """
    Reads location coordinates and plots OR-Tools routes on an interactive Folium map.
    
    :param csv_path: Path to locations.csv
    :param routes: Dictionary mapping vehicle_id to list of node indices, e.g., {0: [0, 4, 2, 0], 1: [0, 1, 3, 0]}
    :param output_html: File name for output HTML map
    """
    df = pd.read_csv(csv_path)
    
    # 1. Center map around Depot (Location 0)
    depot_lat = df.loc[0, 'lat']
    depot_lng = df.loc[0, 'lng']
    m = folium.Map(location=[depot_lat, depot_lng], zoom_start=11)
    
    # 2. Define route colors for distinct vehicles
    colors = ['blue', 'red', 'green', 'purple', 'orange']
    
    # 3. Add markers for each location node
    for idx, row in df.iterrows():
        is_depot = row['is_depot'] == 1
        icon_color = 'red' if is_depot else 'blue'
        icon_type = 'home' if is_depot else 'info-sign'
        
        popup_content = (
            f"<b>{row['name']}</b><br>"
            f"Demand: {row['student_demand']} students<br>"
            f"Window: {row['earliest_time']}-{row['latest_time']} mins"
        )
        
        folium.Marker(
            location=[row['lat'], row['lng']],
            popup=popup_content,
            tooltip=row['name'],
            icon=folium.Icon(color=icon_color, icon=icon_type)
        ).add_to(m)
        
    # 4. Draw Polylines for each vehicle route
    for vehicle_id, node_sequence in routes.items():
        route_coords = []
        for node in node_sequence:
            lat = df.loc[node, 'lat']
            lng = df.loc[node, 'lng']
            route_coords.append([lat, lng])
            
        color = colors[vehicle_id % len(colors)]
        
        folium.PolyLine(
            route_coords,
            color=color,
            weight=4,
            opacity=0.8,
            tooltip=f"Vehicle {vehicle_id} Route"
        ).add_to(m)
        
    # 5. Save output map to disk
    m.save(output_html)
    print(f"Successfully generated interactive map: {output_html}")

if __name__ == "__main__":
    # Test visualization using solved routes: Vehicle 0 (0 -> 4 -> 2 -> 0), Vehicle 1 (0 -> 1 -> 3 -> 0)
    sample_routes = {
        0: [0, 4, 2, 0],
        1: [0, 1, 3, 0]
    }
    generate_route_map("locations.csv", sample_routes)