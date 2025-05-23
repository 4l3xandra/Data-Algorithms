# 🚇 Singapore MRT Route Planner

This Python project models the Singapore MRT network as a graph to compute routes between stations.

## Features

- Find the **fastest route** (based on travel time)
- Find the **fewest stops route** (minimum number of stations)
- Visualize both routes on an interactive map using Folium

## Files

SWE5002-Singapore Metro/
├── MRT Stations.csv # Required data file
├── SingaporeMetro.py # Main program
├── fastest_route.html # Map showing fastest route
└── fewest_stops_route.html # Map showing fewest stops


## Installation

Make sure you have Python 3.7+ installed. Then install dependencies:

```bash
pip install -r requirements.txt


## Running the Program

    1. Clone or download this repo.
    2. Ensure MRT Stations.csv is in the same folder as SingaporeMetro.py.
    3. Run: python SingaporeMetro.py
    4. Enter a start and end station name when prompted.

## Output

    Console shows:
        Fastest route & total travel time
        Fewest stops route
        Whether both paths are identical
    HTML files (fastest_route.html, fewest_stops_route.html) are saved with interactive maps.

📎 Data Source

MRT/LRT Stations Dataset (Kaggle)