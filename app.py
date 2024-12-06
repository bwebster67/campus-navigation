from flask import Flask, render_template, request
from graph_building import build_graph
from pathfinding_algorithms import calculate_optimal_entrances
from path_visualization import create_path_map

app = Flask(__name__)

# Build the graph
graph_data = {
    "graph": None,
    "locations": None,
    "location_nodes": None
}
graph_data["graph"], graph_data["locations"], graph_data["location_nodes"] = build_graph(web_linked=False, file= "map.kml")

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
        

        # Calculating path
        cost, path, start, goal = calculate_optimal_entrances(graph_data["graph"], graph_data["locations"][start_location], graph_data["locations"][end_location], algorithm= "dijkstra")
        
        # Creating map
        create_path_map(start, goal, path, "static", open_map= False)

        return render_template("home.html", 
                                distance= round(cost), 
                                walking_time= round(cost/260), 
                                map_html= "/static/map.html", 
                                options= options, 
                                )
    
    return render_template('home.html', 
                            distance = None, 
                            walking_time = None, 
                            map_html= None, 
                            options= options, 
                            )
    

if __name__ == "__main__":
    app.run(debug=True)