from flask import Flask, render_template, request
from graph_building import build_graph
from pathfinding_algorithms import run_algorithm

app = Flask(__name__)

@app.route("/")
def home():
    # Build the graph
    graph, locations, location_nodes = build_graph(web_linked=False, file= "map.kml")
    
    if request.method == 'POST':
        start_location = request.form["start_location"]
        end_location = request.form["end_location"]
        run_algorithm(graph, locations[start_location], locations[end_location])

        return render_template("temp_home.html", distance=10, walking_time=10, map_html= None)
    return render_template('temp_home.html', distance = None, walking_time = None, map_html= None)
    

if __name__ == "__main__":
    app.run(debug=True)