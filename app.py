from flask import Flask, render_template, request
from waitress import serve
from graph_building import build_graph
from pathfinding_algorithms import calculate_optimal_entrances
from path_visualization import create_path_map
from geopy.distance import lonlat, distance

app = Flask(__name__)

# Build the graph
graph_data = {
    "graph": None,
    "locations": None,
    "location_nodes": None
}
graph_data["graph"], graph_data["locations"], graph_data["location_nodes"] = build_graph(web_linked=False, file= "static/Willamette Map.kml")

# Get location options
options = sorted(graph_data["locations"].keys())

@app.route("/", methods=["GET", "POST"])
def home():

    # If form is submitted
    if request.method == 'POST':
        # Getting the info from the form
        start_location = request.form["start_location"]
        end_location = request.form["end_location"]

        # Check if locations are valid
        if start_location not in graph_data["locations"]:
            return render_template('home.html', 
                                    distance = None, 
                                    walking_time = None, 
                                    map_html= None, 
                                    options= options,
                                    start_invalid= True, 
                                    )
        if end_location not in graph_data["locations"]:
            return render_template('home.html', 
                                    distance = None, 
                                    walking_time = None, 
                                    map_html= None, 
                                    options= options,
                                    end_invalid= True,
                                    )

        # Calculating path
        cost, path, start, end = calculate_optimal_entrances(graph_data["graph"], graph_data["locations"][start_location], graph_data["locations"][end_location], algorithm= "dijkstra")
        
        # Creating map
        lon1, lat1 = start.coords
        lon2, lat2 = end.coords 
        path_centerpoint = ((lat1 + lat2)/2, (lon1 + lon2)/2)

        zoom = 18
        if cost > 1000:
            zoom = 17
        create_path_map(start, end, path, "static", open_map= False, zoom= zoom, map_center= path_centerpoint)

        return render_template("home.html", 
                                distance= round(cost), 
                                walking_time= round(cost/260), 
                                map_html= "/static/map.html", 
                                options= options,
                                start_location = start_location,
                                end_location = end_location 
                                )
    
    return render_template('home.html', 
                            distance = None, 
                            walking_time = None, 
                            map_html= None, 
                            options= options, 
                            )
    

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)
    # waitress-serve --host 127.0.0.1 hello:app
    # flask --app app run