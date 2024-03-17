import heapq

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, name, edges):
        self.vertices[name] = edges

    def dijkstra(self, start):
        # Initialize distances to all vertices as infinity
        distances = {vertex: float('infinity') for vertex in self.vertices}
        distances[start] = 0
        
        # Use a priority queue (min heap) to keep track of vertices to visit next
        priority_queue = [(0, start)]
        
        while priority_queue:
            # Pop the vertex with the smallest distance from the priority queue
            current_distance, current_vertex = heapq.heappop(priority_queue)
            
            # If current distance is already greater than the known distance, skip
            if current_distance > distances[current_vertex]:
                continue
            
            # Visit neighbors of the current vertex
            for neighbor, weight in self.vertices[current_vertex].items():
                distance = current_distance + weight
                
                # If new distance is shorter than the known distance, update it
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        return distances

# Example usage:
if __name__ == "__main__":
    # Create a graph
    graph = Graph()
    graph.add_vertex('A', {'B': 3, 'C': 4})
    graph.add_vertex('B', {'A': 3, 'C': 1, 'D': 7})
    graph.add_vertex('C', {'A': 4, 'B': 1, 'D': 2})
    graph.add_vertex('D', {'B': 7, 'C': 2})
    
    # Find the shortest paths from vertex 'A'
    shortest_paths_from_A = graph.dijkstra('A')
    
    print("Shortest paths from vertex A:")
    for vertex, distance in shortest_paths_from_A.items():
        print(f"To {vertex}: {distance}")
