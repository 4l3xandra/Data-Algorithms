import csv
import random
import re
from collections import defaultdict
import networkx as nx
import folium
import difflib

class MRTGraph:
    def __init__(self):
        self.graph = nx.Graph() #initializes a new undirected graph (networkx)
        self.station_data = {} #station_data holds metadata for each node

    def load_csv(self, file_path): #loads the csv file and builds the graph
        line_stations = defaultdict(list) #groups stations by MRT line to sort them
        name_to_ids = defaultdict(list) #groups stations by name for building interchanges

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # reads each station's row from the csv
            for row in reader:
                name = row['STN_NAME'].replace(' MRT STATION', '').strip() #extracts station name, codes, coordinates
                codes = row['STN_NO'].split('/') #handles cases where a station has multiple codes
                lat = float(row['Latitude'])
                lon = float(row['Longitude'])

                # extracts line (NS, EW, DT, etc.) and station number
                for code in codes:
                    line = ''.join(re.findall(r'[A-Z]+', code))
                    digits = ''.join(re.findall(r'[0-9]+', code))
                    if not line or not digits:
                        continue
                    node_id = f"{name} ({line})" #creates a unique ID
                    self.graph.add_node(node_id, name=name, line=line, lat=lat, lon=lon)
                    self.station_data[node_id] = (name, line, lat, lon)
                    line_stations[line].append((int(digits), node_id))
                    name_to_ids[name.upper()].append(node_id)

        for stations in line_stations.values():
            stations.sort() #sorts by station number (e.g. EW1)
            for i in range(len(stations) - 1):
                self.graph.add_edge(stations[i][1], stations[i + 1][1], weight=random.randint(2, 8), type='same_line') #adds edges with random travel time between 2–8 minutes

        # if multiple nodes share a name (e.g. PAYA LEBAR (EW) and PAYA LEBAR (CC)), connect them with a 5-minute interchange edge
        for ids in name_to_ids.values():
            if len(ids) > 1:
                for i in range(len(ids)):
                    for j in range(i + 1, len(ids)):
                        self.graph.add_edge(ids[i], ids[j], weight=5, type='interchange')

    # suggests station names based on approximate string matching with user input
    def suggest_station(self, input_name, top_n=3):
        all_names = [data['name'] for _, data in self.graph.nodes(data=True)]
        unique_names = sorted(set(all_names))
        input_name = input_name.strip().lower()
        # match lowercase versions for better comparison
        matches = difflib.get_close_matches(input_name, [name.lower() for name in unique_names], n=top_n)
        # return original casing of matched names
        return [name for name in unique_names if name.lower() in matches]

    def find_fastest_path(self, start, end):
        # removes extra whitespaces from start/end and converts lowercase chars into uppercase ("Bugis" and " bugis " are treated the same)
        start = start.strip().upper()
        end = end.strip().upper()
        # finds all nodes matching the start and end names
        start_nodes = [node for node, data in self.graph.nodes(data=True) if data['name'].upper() == start]
        end_nodes = [node for node, data in self.graph.nodes(data=True) if data['name'].upper() == end]
        # returns none if invalid names
        if not start_nodes or not end_nodes:
            return None

        min_path = None
        min_cost = float('inf')
        # try all combinations of start/end variants
        for s in start_nodes:
            for e in end_nodes:
                try:
                    # finds fastest route using edge weights
                    path = nx.dijkstra_path(self.graph, source=s, target=e, weight='weight')
                    cost = nx.dijkstra_path_length(self.graph, source=s, target=e, weight='weight')
                    # keeps track of best lowest-cost path
                    if cost < min_cost:
                        min_cost = cost
                        min_path = path
                except nx.NetworkXNoPath:
                    continue
        return min_path

    def find_fewest_stops_path(self, start, end):
        start = start.strip().upper()
        end = end.strip().upper()
        start_nodes = [node for node, data in self.graph.nodes(data=True) if data['name'].upper() == start]
        end_nodes = [node for node, data in self.graph.nodes(data=True) if data['name'].upper() == end]

        if not start_nodes or not end_nodes:
            return None

        min_path = None
        min_length = float('inf')
        for s in start_nodes:
            for e in end_nodes:
                try:
                    path = nx.shortest_path(self.graph, source=s, target=e) #no weights so all edges are equal
                    if len(path) < min_length: #picks path with fewest nodes
                        min_length = len(path)
                        min_path = path
                except nx.NetworkXNoPath:
                    continue
        return min_path

    def path_with_time(self, path):
        if not path:
            return 0, [] #if no path is given return with 0 time
        segments = []
        total_time = 0
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            w = self.graph[a][b]['weight']
            #build a list of (from, to, time)
            segments.append((a, b, w))
            #accumulate total time
            total_time += w
        return total_time, segments

    '''Uses Folium to draw a map with the route'''
    def visualize_path(self, path, filename='mrt_route.html', color='blue'):
        if not path:
            print("No path to visualize.")
            return
        # convert each station name to latitude, longitude
        latlon = [(self.graph.nodes[n]['lat'], self.graph.nodes[n]['lon']) for n in path]
        # center map at the start of the station
        fmap = folium.Map(location=latlon[0], zoom_start=13)
        # draw the path line
        folium.PolyLine(latlon, color=color, weight=5).add_to(fmap)
        for i, (lat, lon) in enumerate(latlon):
            # add a marker at each station
            folium.Marker([lat, lon], tooltip=path[i]).add_to(fmap)
        # save as 'fastest_route.html' or 'fewest_stops.html'
        fmap.save(filename)
        print(f"Map saved as {filename}")

'''app entry point'''
if __name__ == "__main__":
    # load csv
    file_path = "MRT Stations.csv"
    mrt = MRTGraph()
    mrt.load_csv(file_path)

    #print all available stations
    print("\nAvailable stations:")
    names = sorted({data['name'] for _, data in mrt.graph.nodes(data=True)})
    for name in names:
        print("-", name)


    # prompt user for station input, validate it, and suggest corrections if invalid
    def get_valid_station(prompt):
        while True:
            user_input = input(prompt).strip()
            # find nodes that exactly match the input station name
            match = [node for node, data in mrt.graph.nodes(data=True) if data['name'].upper() == user_input.upper()]
            if match:
                return user_input
            # get closest matching station names for user guidance
            suggestions = mrt.suggest_station(user_input)
            print(f"\nStation '{user_input}' not found.")
            if suggestions:
                print("Did you mean:")
                for s in suggestions:
                    print(f"  - {s}")
            else:
                print("No similar station names found.")

    # take user input
    start = get_valid_station("\nEnter start station name: ")
    end = get_valid_station("Enter end station name: ")

    # calculate both paths
    fastest_path = mrt.find_fastest_path(start, end)
    fewest_stops_path = mrt.find_fewest_stops_path(start, end)

    # show results
    print("\nFastest Route:", fastest_path if fastest_path else "No path found")
    if fastest_path:
        total_time, segments = mrt.path_with_time(fastest_path)
        print(f"Total Travel Time: {total_time} min")
        print("Segment Timings:")
        for a, b, t in segments:
            print(f"{a} → {b} = {t} min")

    print("\nFewest Stops Route:", fewest_stops_path if fewest_stops_path else "No path found")
    if fastest_path == fewest_stops_path:
        print("\nFastest and fewest-stops routes are identical.")
    else:
        print("\nRoutes differ.")

    # visualize both paths in map files
    mrt.visualize_path(fastest_path, "fastest_route.html", color="green")
    mrt.visualize_path(fewest_stops_path, "fewest_stops_route.html", color="red")
