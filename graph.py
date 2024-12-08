# graph.py
# File defining the Node and Graph classes.
from __future__ import annotations


class Node:

    def __init__(self, name: str = None, longitude: float = -1, latitude: float = -1):
        """
        Initializes a Node object.
        """
        self._neighbors = []
        self._longitude = longitude
        self._latitude = latitude
        self._name = name 


    def add_neighbor(self, node: Node, weight) -> None:
        """
        Appends the passed node to self's adjacency list.   
        """
        self._neighbors.append((node, weight))


    @property
    def name(self) -> str:
        """
        Returns the name of the node.
        """
        return self._name


    @property
    def longitude(self) -> float:
        """
        Returns the longitude of the node.
        """
        return self._longitude
    

    @property
    def latitude(self) -> float:
        """
        Returns the latitude of the node.
        """
        return self._latitude
    

    @property
    def coords(self) -> tuple:
        """
        Returns the coordinates of the node as (longitude, latitude)
        """
        return (self._longitude, self._latitude)
    

    @property
    def neighbors(self) -> list:
        """
        Returns the neighbors of the node.
        """
        return self._neighbors


    def __str__(self) -> str:
        return f"Node: {self._name}"
    

    def __repr__(self) -> str:
        return self.__str__()
    

    def __lt__(self, other: Node) -> bool:
        """
        Necessary to avoid errors with heapq comparison when priority is equal
        """
        return self.name < other.name



class Graph:

    def __init__(self):
        """
        Initializes a Graph object.
        """
        self._adjacency_list: dict[Node: list[(Node, int)]] = {}
        self._nodes_by_name: dict[str: Node]


    def add_node(self, node: Node, neighbors: list[(Node, int)] = []) -> None:
        """
        Adds a node to the graph.
        """
        self._adjacency_list[node] = []

        # If neighbors are passed
        for neighbor in neighbors:
            neighbor, weight = neighbor[0], neighbor[1]
            node.add_neighbor(neighbor, weight)
            self._adjacency_list[node].append((neighbor, weight))


    def add_edge(self, node1: Node, node2: Node, weight: float) -> None:
        """
        Adds a weighted edge between two nodes.
        """
        for tup in self.get_neighbors(node1):
            if tup[0] == node2:
                tup[1] = weight
                for tup in self.get_neighbors(node2):
                    if tup[0] == node2:
                        tup[1] = weight
                        return        
        self._adjacency_list[node1].append((node2, weight))
        node1.add_neighbor(node2, weight)
        self._adjacency_list[node2].append((node1, weight))
        node2.add_neighbor(node1, weight)


    def get_weight(self, node1: Node, node2: Node) -> float:
        """
        Returns the weight between the two given edges. Returns None if there is no edge.
        """
        for neighbor in self._adjacency_list[node1]:
            if neighbor[0] == node2:
                return neighbor[1]
        return None


    def get_neighbors(self, node: Node) -> list[tuple[Node, int]]:
        """
        Returns the list of neighbor tuples of the passed Node.
        """
        return self._adjacency_list[node]


    @property
    def nodes(self):
        """
        Returns a dict_keys containing all the nodes in the graph.
        """
        return self._adjacency_list.keys()


    @property
    def nodes_by_names(self) -> dict:
        """
        Returns a dictionary containing all the nodes in the graph as ("name", Node).
        """
        return self._nodes_by_name