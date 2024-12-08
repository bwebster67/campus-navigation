import folium
from graph import Node
import webbrowser
from pathlib import Path
MAP_CENTER = (44.93598, -123.03066)
LOCATION_COLOR = 'blue'
PATH_NODE_COLOR = 'transparent'

def create_path_map(start_node: Node, goal_node: Node, path: list[Node], file_location: str= "path_maps", open_map: bool = True, zoom: int = 18, map_center: tuple[int, int] = MAP_CENTER) -> None:
    """
    Creates an HTML file with the shortest path overlayed over a map of the Willamette University campus.
    """

    def make_location_marker(node: Node) -> folium.Marker:
        """
        Creates a folium Marker for a given node and adds it to the map. Returns the marker.
        """
        marker = folium.Marker(
            location= [node.latitude, node.longitude], 
            popup= node.name, 
            icon= folium.Icon(color= LOCATION_COLOR)
            )
        marker.add_to(campus_map)
        return marker
    

    def make_path_marker(node: Node) -> folium.CircleMarker:
        """
        Creates a folium CircleMarker for a given node and adds it to the map. Returns the marker.
        """
        marker = folium.CircleMarker(
            location= [node.latitude, node.longitude],
            radius= 1,
            color= PATH_NODE_COLOR,
            fill= False,
            fill_opacity= 0.7,
            )
        marker.add_to(campus_map)
        return marker

    # Create the map object
    campus_map = folium.Map(location= map_center, zoom_start= zoom)  # Start zoom level, adjust as needed

    markers = []

    # Add markers for start and goal to the map
    markers.append(make_location_marker(start_node))
    markers.append(make_location_marker(goal_node))

    # Add markers for the buildings along the path
    for node in path:
        markers.append(make_path_marker(node))

    # Add a polyline for the shortest path (connecting the buildings)
    path_coords = [(node.latitude, node.longitude) for node in path]
    folium.PolyLine(path_coords, color='red', weight=2.5, opacity=1).add_to(campus_map)

    # Save the map to an HTML file
    folder = file_location
    file_name = "map.html"
    file_path = Path(folder) / file_name  # Correct path joining

    # Convert to URI
    file_url = file_path.resolve().as_uri()

    # Save the map to the correct file
    campus_map.save(file_path)

    # Open in a new tab
    if open_map:
        webbrowser.open_new_tab(file_url)

