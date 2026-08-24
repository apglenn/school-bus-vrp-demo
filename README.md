# School Bus Vehicle Routing Model

A Python-based optimization project using Google OR-Tools to model and solve Capacitated Vehicle Routing Problems (CVRP) for school districts.

## Features
- Distance matrix generation for multi-district school stops.
- Route optimization using Google OR-Tools.
- Interactive map visualization using Folium.

## How to Run
1. Clone this repository.
2. Activate virtual environment and install requirements:
   `pip install "ortools==9.11.4210" pandas numpy matplotlib folium`
3. Run `python main.py` 

## Known Issues
- OR-Tools versions 9.15 and higher currently have a broken Python binding for 'SetAllowedVehiclesForIndex'. Confirmed Via isolated reproduction against multiple OR-Tools versions.
