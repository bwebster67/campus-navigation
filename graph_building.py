# graph_building.py
# Builds a graph from a KML file.
from lxml import etree
from dataclasses import dataclass
from graph import Graph, Node
from geopy.distance import lonlat, distance
import requests

@dataclass
class Location:
    entrances: list[Node]

    def __hash__(self):
        """
        Necessary for flask stuff
        """
        coords = ""
        for node in self.entrances:
            coords += str(node.coords)
        return hash(coords)

def build_graph(web_linked = False, file: str = "doc.kml") -> tuple[Graph, dict[str, Location], dict[str, Node]]:
    """
    Returns a tuple containing the graph at index 0, 
    and a dictionary of all location nodes at index 1.
    """

    path_num = 0 # Used for naming paths
    def connect_path(path, i, prev_node: Node = None, name = "") -> Node:
        """
        Connects two nodes in a path with a weighted edge and returns the second.
        Calculates distance based on longitude and latitude.
        """

        # For the first node in the path
        if prev_node == None:
            lon1, lat1 = path[i]
            lon2, lat2 = path[i + 1]

            node1 = Node(f"Path: {i}.{path_num}", lon1, lat1)
            node2 = Node(name, lon2, lat2)

            dist = distance(lonlat(*(lon1, lat1)), lonlat(*(lon2, lat2))).feet

            path_nodes.append(node1)
            path_nodes.append(node2)
            graph.add_node(node1)
            graph.add_node(node2)
            graph.add_edge(node1, node2, dist)

        # For all other nodes in the path
        else:
            lon1, lat1 = prev_node.longitude, prev_node.latitude
            lon2, lat2 = path[i + 1]

            node2 = Node(name, lon2, lat2) 

            dist = distance(lonlat(*(lon1, lat1)), lonlat(*(lon2, lat2))).feet
            
            path_nodes.append(node2)
            graph.add_node(node2)
            graph.add_edge(prev_node, node2, dist)

        return node2
    

    graph = Graph()

    # If you're using a web-linked KML file.
    if web_linked:
        # Below not necessary anymore I think
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

        # Requests the web-linked KML file from the URL.
        response = requests.get(file)
        if response.status_code != 200:
            print(f"Failed to retrieve KML file. Status code: {response.status_code}")
            return
        
        kml_content = response.content
        root = etree.fromstring(kml_content)

    # If you're using a local file.
    elif not web_linked: 
        tree = etree.parse(f"{file}")
        root = tree.getroot()

    # KML Boilerplate
    namespace: dict = {"kml": "http://www.opengis.net/kml/2.2"}
    placemarks = root.xpath("//kml:Placemark", namespaces=namespace)

    # Trackers for location nodes and path nodes
    locations: dict[str: Location] = {}
    location_nodes: dict[str: Node] = {}
    path_nodes: list = []

    # Iterates through every object regardless of type (point, line, etc.)
    for placemark in placemarks:
        name: str = placemark.find("kml:name", namespaces=namespace).text
        
        # Points (locations)
        point = placemark.find(".//kml:Point/kml:coordinates", namespaces=namespace)
        if point is not None:  
            coords = point.text.strip().split(",")
            longitude, latitude = float(coords[0]), float(coords[1])

            # Check for multiple entrances
            name_list: list = name.split("_")
            node: Node = Node(name, longitude, latitude)
            
            # If there are no other entrances to this location added yet
            if name_list[0] not in locations:
                new_location = Location([node])
                locations[name_list[0]] = new_location
            else:
                locations[name_list[0]].entrances.append(node)
            location_nodes[name] = node
            graph.add_node(node) 
        
        # Lines (paths)
        line = placemark.find(".//kml:LineString/kml:coordinates", namespaces=namespace)
        if line is not None:  
            coords = line.text.strip().split()
            path = [tuple(list(map(float, coord.split(",")))[:2]) for coord in coords]  
            
            node2= None
            for i in range(len(path)-1):
                node2 = connect_path(path, i, node2, name=name)
            path_num += 1

    # Adds edges with a weight of 0 between nodes with the same coordinates
    for i1 in range(len(path_nodes)):
        for i2 in range(i1, len(path_nodes)):
            if path_nodes[i1].coords == path_nodes[i2].coords and path_nodes[i1] != path_nodes[i2]:
                graph.add_edge(path_nodes[i1], path_nodes[i2], 0)


    # I think the below code may be unnecessary, but I'm not sure.
    for location_node in location_nodes.values():

        for path_node in path_nodes:
            # Adds an edge between nodes with weight 0 if they have the exact same coordinates
            if location_node.coords == path_node.coords:
                graph.add_edge(location_node, path_node, 0)

            # Adds an edge between nodes if they are less than 5ft apart but not properly connected
            else:
                dist = dist = distance(lonlat(*location_node.coords), lonlat(*path_node.coords)).feet
                if dist < 5:
                    graph.add_edge(location_node, path_node, dist)

    return (graph, locations, location_nodes)