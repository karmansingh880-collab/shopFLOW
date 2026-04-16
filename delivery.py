# ============================================================
# delivery.py  —  ShopFlow
# CONCEPT: Graph + BFS (Breadth-First Search)
#
# We model the delivery network as a GRAPH:
#   - Nodes  = Cities (Warehouse, Mohali, Chandigarh, etc.)
#   - Edges  = Roads connecting cities
#
# BFS (Breadth-First Search) finds the SHORTEST path
# from the Warehouse to the customer's city.
#
# HOW BFS WORKS:
#   1. Start at Warehouse. Put it in a queue.
#   2. Take the first city from queue.
#   3. Check all its neighbors:
#        - If neighbor = destination → DONE, return path!
#        - Else → add neighbor to queue (if not visited yet)
#   4. Repeat until destination found or queue empty.
#
# BFS guarantees the FEWEST number of hops (shortest route).
# ============================================================

from collections import deque


class DeliveryGraph:
    def __init__(self):
        # Adjacency list: { city: [list of connected cities] }
        self.graph = {}

    def add_city(self, city):
        """Add a city (node) to the graph."""
        if city not in self.graph:
            self.graph[city] = []

    def add_road(self, city1, city2):
        """Add a road (undirected edge) between two cities."""
        self.graph[city1].append(city2)
        self.graph[city2].append(city1)

    def bfs_route(self, start, destination):
        """
        Find the shortest route from start to destination using BFS.
        Returns a list of cities forming the path, or None if unreachable.
        """
        if destination not in self.graph:
            return None   # city doesn't exist in our network

        visited = set()                         # cities we've already explored
        queue = deque([(start, [start])])       # queue of (current_city, path_so_far)
        visited.add(start)

        while queue:
            city, path = queue.popleft()        # take the next city to explore

            if city == destination:
                return path                     # found it! return the full path

            for neighbor in self.graph[city]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None   # no route found

    def get_all_cities(self):
        """Return list of all cities except Warehouse."""
        return [c for c in self.graph if c != "Warehouse"]

    def get_network_info(self):
        """Return graph as list of dicts for UI display."""
        rows = []
        for city, neighbors in self.graph.items():
            rows.append({
                "city": city,
                "connected_to": ", ".join(neighbors)
            })
        return rows


def setup_delivery_network():
    """
    Build and return a pre-configured delivery network.

    Network layout:
        Warehouse ──── Mohali ──── Panchkula ──── Ambala
             └────── Chandigarh ──┘
    """
    g = DeliveryGraph()

    # Add all cities
    for city in ["Warehouse", "Mohali", "Chandigarh", "Panchkula", "Ambala"]:
        g.add_city(city)

    # Add roads between cities
    g.add_road("Warehouse",  "Mohali")
    g.add_road("Warehouse",  "Chandigarh")
    g.add_road("Mohali",     "Panchkula")
    g.add_road("Chandigarh", "Panchkula")
    g.add_road("Panchkula",  "Ambala")

    return g
