# experimental_comparison.py
# Compares the performance of the pathfinding algorithms.
from graph_building import build_graph
from pathfinding_algorithms import euclidean_heuristic, run_algorithm
from tqdm import tqdm
from timeit import timeit


def experimental_comparison(iterations: int = 5) -> None:
    """
    Compares the performance of the pathfinding algorithms.
    """
    graph, locations, location_nodes = build_graph(web_linked= True, file= "https://www.google.com/maps/d/u/0/kml?forcekml=1&mid=1O_JqDQIKP5n6X-zYpz5eD82XSd32ips")
    
    # For every node in the graph
    for node in tqdm(location_nodes.items()):
        # For every other node in the graph
        for other_node in location_nodes.items():
            # If the nodes are not the same
            if node != other_node:
                # Run the algorithms
                dijkstra_time = timeit(lambda: run_algorithm(graph, node[1], other_node[1], "dijkstra"), number= iterations)
                greedy_bfs = timeit(lambda: run_algorithm(graph, node[1], other_node[1], "greedy_bfs"), number= iterations)
                a_star = timeit(lambda: run_algorithm(graph, node[1], other_node[1], "a_star"), number= iterations)

    dijkstra_time /= iterations * len(location_nodes)
    greedy_bfs /= iterations * len(location_nodes)
    a_star /= iterations * len(location_nodes)

    print(f"\nDijkstra: {dijkstra_time} seconds")
    print(f"Greedy BFS: {greedy_bfs} seconds")
    print(f"A*: {a_star} seconds")