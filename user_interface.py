# user_interface.py
from graph_building import Location, build_graph
from pathfinding_algorithms import euclidean_heuristic, calculate_optimal_entrances
from path_visualization import create_path_map
from graph import Graph, Node


algorithms = ["dijkstra", "greedy_bfs", "a_star"]
heuristics = ["euclidean"]

FEET_PER_MINUTE = 260

def ui_introduction(file: str) -> tuple[Graph, dict[str, Location], dict[str: Node]]:
    """
    Introduces the user to the program and generates the graph.
    Returns the graph and nodes.
    """
    print("Loading...")
    graph, locations, location_nodes = build_graph(web_linked= True, file= file)
    print("Welcome to the Willamette University Campus Navigation System!")
    return graph, locations, location_nodes


def ui_get_start_location(locations) -> tuple[Location, str]:
    """
    Prompts the user to enter the name of the starting location.
    Returns the starting location node.
    """
    print("Please enter the name of the location you wish to start in.")
    start_input = input("Start: ")
    while start_input not in locations:
        print("Invalid location name. Please enter a valid location.")
        start_input = input("Start: ")
    return locations[start_input], start_input


def ui_get_goal_location(locations: dict[str: Location], start_input: str) -> Location:
    """
    Prompts the user to enter the name of the goal location.
    Returns the goal location node.
    """
    print("Please enter the name of the building you would like to navigate to.")
    goal_input = input("Goal: ")
    while goal_input not in locations or goal_input == start_input:
        if goal_input == start_input:
            print("You may not navigate to the starting location. Please enter a valid location.")
        else:
            print("Invalid location name. Please enter a valid location.")
        goal_input = input("Goal: ")
    return locations[goal_input]


def ui_get_algorithm() -> tuple[str, callable]:
    """
    Prompts the user to enter the algorithm and heuristic they would like to use.
    Returns the algorithm and heuristic.
    """
    print("Please enter the algorithm you would like to use.")
    print(f"Options: {algorithms}")
    algorithm = input("Algorithm: ")
    while algorithm not in algorithms:
        print("Invalid algorithm. Please enter a valid algorithm.")
        algorithm = input("Algorithm: ")

    if algorithm == "greedy_bfs" or algorithm == "a_star":
        print("Please enter the heuristic you would like to use.")
        print(f"Options: ['euclidean']")
        heuristic = input("Heuristic: ")
        while heuristic not in heuristics:
            print("Invalid heuristic. Please enter a valid heuristic.")
            heuristic = input("Heuristic: ")
        if heuristic == "euclidean":
            heuristic = euclidean_heuristic
    else:
        heuristic = None
    return algorithm, heuristic


def ui_output_distance_and_time(cost) -> None:
    """
    Outputs the distance and estimated walking time from the start ocation to the goal location.
    """
    print(f"Distance: {round(cost)} feet")
    walk_time = round(cost / FEET_PER_MINUTE)
    if walk_time == 0:
        print("Estimated Walking Time: Less than 1 minute")
    elif walk_time == 1:
        print("Estimated Walking Time: 1 minute")
    else:
        print(f"Estimated Walking Time: {walk_time} minutes")


def ui_path_map(start, goal, path) -> None:
    """
    Prompts the user as to whether or not to visualize the path on a map.
    If yes, creates the path map as an html and opens it in the default web browser.
    """
    print("Would you like to visualize the path on a map? (Y/N)")
    visualize = input("Visualize: ")
    while visualize not in ["Y", "N"]:
        print("Invalid input. Please enter 'Y' or 'N'.")
        visualize = input("Visualize: ")
    if visualize == "Y":
        create_path_map(start, goal, path)  


def ui_start_over() -> bool:
    """
    Prompts the user as to whether or not to start over.
    If yes, runs the program again.
    """
    print("\nWould you like to generate another path? (Y/N)")
    start_over = input("Start Over: ")
    while start_over not in ["Y", "N"]:
        print("Invalid input. Please enter 'Y' or 'N'.")
        start_over = input("Start Over: ")
    if start_over == "Y":
        print()
        return True
    return False


def run(file: str = "https://www.google.com/maps/d/u/0/kml?forcekml=1&mid=1O_JqDQIKP5n6X-zYpz5eD82XSd32ips") -> None:
    """
    Main function for starting the user interface.
    """
    graph, locations, location_nodes = ui_introduction(file)
    running = True
    while running == True:
        start_location, start_input = ui_get_start_location(locations)
        goal_location = ui_get_goal_location(locations, start_input)
        algorithm, heuristic = ui_get_algorithm()
        print("Calculating path...")
        # Calculate path from every entrance for start to every entrance of goal
        cost, path, start, goal = calculate_optimal_entrances(graph, start_location, goal_location, algorithm, heuristic)

        ui_output_distance_and_time(cost)
        ui_path_map(start, goal, path)
        running = ui_start_over()
    print("Thank you for using the Willamette University Campus Navigation System!")
