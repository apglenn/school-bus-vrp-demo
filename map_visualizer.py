# map_visualizer.py
import folium
import pandas as pd

def generate_route_map(csv_path, routes_dict, output_html="route_map.html"):
    df = pd.read_csv(csv_path)
    
    depot_lat, depot_lng = df.loc[0, 'lat'], df.loc[0, 'lng']
    m = folium.Map(location=[depot_lat, depot_lng], zoom_start=11)
    colors = ['blue', 'red', 'green', 'purple', 'orange']
    
    # Place markers for stops
    for idx, row in df.iterrows():
        is_depot = row['is_depot'] == 1
        icon_color = 'red' if is_depot else 'blue'
        icon_type = 'home' if is_depot else 'info-sign'
        
        folium.Marker(
            location=[row['lat'], row['lng']],
            popup=f"<b>{row['name']}</b><br>Demand: {row['student_demand']}",
            tooltip=row['name'],
            icon=folium.Icon(color=icon_color, icon=icon_type)
        ).add_to(m)
        
    # Draw routes directly from list of node indices
    for vehicle_id, node_sequence in routes_dict.items():
        route_coords = [[df.loc[node, 'lat'], df.loc[node, 'lng']] for node in node_sequence]
        color = colors[vehicle_id % len(colors)]
        
        folium.PolyLine(
            route_coords,
            color=color,
            weight=4,
            opacity=0.8,
            tooltip=f"Vehicle {vehicle_id} Route"
        ).add_to(m)
        
    m.save(output_html)
    print(f"Map successfully generated: {output_html}")