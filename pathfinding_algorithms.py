# pathfinding_algorithms.py
# File defining the pathfinding algorithms.
from graph import Graph, Node
from geopy.distance import lonlat, distance
from graph_building import Location
import heapq


def euclidean_heuristic(current: Node, goal: Node) -> float:
    """
    Returns the Euclidean distance between the current node and the goal node.
    """
    return distance(lonlat(*current.coords), lonlat(*goal.coords)).feet


def run_algorithm(graph: Graph, start: Node, goal: Node, algorithm: str, heuristic= euclidean_heuristic) -> tuple[int, list[Node]]:
    """
    Runs the specified algorithm on the graph.
    "dijksta", "greedy_bfs", "a_star"
    """
    if algorithm == "dijkstra":
        return dijkstra(graph, start, goal)
    elif algorithm == "greedy_bfs":
        return greedy_bfs(graph, start, goal, heuristic)
    elif algorithm == "a_star":
        return a_star(graph, start, goal, heuristic)
    else:
        raise ValueError("Invalid algorithm.")


def trace_path(start: Node, goal: Node, came_from: dict) -> list[Node]:
    """
    Traces the path from the start node to the goal node.
    """
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path


def calculate_optimal_entrances(graph: Graph, start_location: Location, goal_location: Location, algorithm: str, heuristic: callable= None):
    paths = []
    for start_entrance in start_location.entrances:
        for goal_entrance in goal_location.entrances:
            cost, path = run_algorithm(graph, start_entrance, goal_entrance, algorithm, heuristic)
            paths.append((cost,path, start_entrance, goal_entrance))
    shortest = paths[0]
    for i in range(1, len(paths)):
        path = paths[i]
        if path[0] < shortest[0]:
            shortest = path
    cost, path, start, goal = shortest
    return (cost, path, start, goal)


def dijkstra(graph: Graph, start: Node, goal: Node) -> tuple[int, list[Node]]:
    """
    Executes Dijkstra's algorithm and returns a tuple containing the cost of the path and the path itself.
    """
    # Trackers for the frontier, the path, and the cost so far
    # frontier uses heapq to function like a faster PriorityQueue 
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    # While there are nodes in the frontier
    while frontier:
        _, current = heapq.heappop(frontier)

        # If we've found the goal, return the cost and the path
        if current == goal:
            return (cost_so_far[goal], trace_path(start, goal, came_from))

        # Otherwise, iterate through the neighbors of the current node
        for next in graph.get_neighbors(current):
            next_node = next[0]
            new_cost = cost_so_far[current] + graph.get_weight(current, next_node)
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost # Calculates priority based only on the cost
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current

    print("Goal node was not found.")
    return


def greedy_bfs(graph: Graph, start: Node, goal: Node, heuristic = euclidean_heuristic) -> tuple[int, list[Node]]:
    """
    Executes the Greedy Best-First Search algorithm and returns a tuple containing the cost of the path and the path itself.
    """
    # Trackers for the frontier, the path, and the cost so far
    # frontier uses heapq to function like a faster PriorityQueue 
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    # While there are nodes in the frontier
    while frontier:
        _, current = heapq.heappop(frontier)

        # If we've found the goal, return the cost and the path
        if current == goal:
            return (cost_so_far[goal], trace_path(start, goal, came_from))
        
        # Otherwise, iterate through the neighbors of the current node
        for next in graph.get_neighbors(current):
            next_node = next[0]
            new_cost = cost_so_far[current] + graph.get_weight(current, next_node)
            if next_node not in came_from:
                cost_so_far[next_node] = new_cost
                priority = heuristic(next_node, goal) # Calculates priority based only on the heuristic
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current
    
    print("Goal node was not found.")
    return


def a_star(graph: Graph, start: Node, goal: Node, heuristic = euclidean_heuristic) -> tuple[int, list[Node]]:
    """
    Executes the A* algorithm and returns a list of 
    nodes representing the path from start to goal.
    """
    # Trackers for the frontier, the path, and the cost so far
    # frontier uses heapq to function like a faster PriorityQueue 
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    # While there are nodes in the frontier
    while frontier:
        _, current = heapq.heappop(frontier)

        # If we've found the goal, return the cost and the path
        if current == goal:
            return (cost_so_far[goal], trace_path(start, goal, came_from))

        # Otherwise, iterate through the neighbors of the current node
        for next in graph.get_neighbors(current):
            next_node = next[0]
            new_cost = cost_so_far[current] + graph.get_weight(current, next_node)
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(next_node, goal) # Calculates priority based on the cost and the heuristic
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current
    
    print("Goal node was not found.")
    return
