#
# graph.py
#
import numpy as np
import heapq as heap
import copy
from collections import defaultdict

class Graph:
    def __init__(self, directed = True):
        self.vertices=[]
        self.edges=defaultdict()
        self.vertNames=defaultdict()
        self.directed = directed
        self.debug = False
    def __str__(self):
        self.print()
    def addedge(self, vertA, vertB, dist):
        if not vertA in self.vertices:
            self.vertices.append(vertA)
        if not vertB in self.vertices:
            self.vertices.append(vertB)
        self.edges[vertA, vertB] = dist
        if not self.directed:
            self.edges[vertB, vertA] = dist
    def  print(self):
        for v1 in self.vertices:
            for v2 in self.vertices:
                if v1 == v2: continue
                if (v1,v2) in self.edges:
                    print(v1, " --> ", v2, " : ", self.edges[(v1,v2)])
    def getmindistance(self, start, stop):
        if not start in self.vertices:
            print("ERROR - Starting point ", start, " is not a vertex")
            return -1
        if not stop in self.vertices:
            print("ERROR - End point ", stop, " is not a vertex")
            return -1
        visited = [False] * len(self.vertices)
        # don't have an Inf for integers - going to assume 1 trillion is large enough
        distance = defaultdict()
        q = []
        for v in self.vertices:
            distance[v] = 1000000000000
            heap.heappush(q, v)
        distance[start] = 0
        while q:
            current = q.pop()
            if (self.debug) : print(current, " ", distance[current])
            visited.append(current)
            for adjNode in self.vertices:
                #if adjNode in visited: continue
                if not (current, adjNode) in self.edges: continue
                newDist = distance[current] + self.edges[current, adjNode]
                if distance[adjNode] > newDist:
                    distance[adjNode] = newDist
                    if (self.debug) : print("***", current, " -> ", adjNode, " == ", newDist)
                    heap.heappush(q, adjNode)
        return distance[stop]
                
    def getmaxdistance(self, start, stop):
        if not start in self.vertices:
            print("ERROR - Starting point ", start, " is not a vertex")
            return -1
        if not stop in self.vertices:
            print("ERROR - End point ", stop, " is not a vertex")
            return -1
        visited = [False] * len(self.vertices)
        distance = defaultdict()
        q = []
        for v in self.vertices:
            distance[v] = 0
            heap.heappush(q, v)
        distance[start] = 0
        while q:
            current = q.pop()
            if (self.debug) : print(current, " ", distance[current])
            visited.append(current)
            for adjNode in self.vertices:
                #if adjNode in visited: continue
                if not (current, adjNode) in self.edges: continue
                newDist = distance[current] + self.edges[current, adjNode]
                if distance[adjNode] < newDist:
                    distance[adjNode] = newDist
                    if (self.debug) : print("***", current, " -> ", adjNode, " == ", newDist)
                    heap.heappush(q, adjNode)
        return distance[stop]  

    # A Python Program to detect
    # cycle in an undirected graph

    def is_cyclic_util(self, v, visited, parent):
      
        # Mark the current node as visited
        visited[v] = True

        # Recur for all the vertices
        # adjacent to this vertex
        for i in self.adj[v]:
          
            # If an adjacent vertex is not visited,
            # then recur for that adjacent
            if not visited[i]:
                if is_cyclic_util(i, adj, visited, v):
                    return True
                  
            # If an adjacent vertex is visited and
            # is not parent of current vertex,
            # then there exists a cycle in the graph.
            elif i != parent:
                return True

        return False

    def is_cyclic(self):
        V = len(self.vertices)
        # Mark all the vertices as not visited
        visited = [False] * V

        # Call the recursive helper function
        # to detect cycle in different DFS trees
        for u in range(V):
          
            # Don't recur for u if it is already visited
            if not visited[u]:
                if self.is_cyclic_util(u, visited, -1):
                    return True

        return False

        
# A Python Program to detect
# cycle in an undirected graph

def is_cyclic_util(v, adj, visited, parent):
  
    # Mark the current node as visited
    visited[v] = True

    # Recur for all the vertices
    # adjacent to this vertex
    for i in adj[v]:
      
        # If an adjacent vertex is not visited,
        # then recur for that adjacent
        if not visited[i]:
            if is_cyclic_util(i, adj, visited, v):
                return True
              
        # If an adjacent vertex is visited and
        # is not parent of current vertex,
        # then there exists a cycle in the graph.
        elif i != parent:
            return True

    return False

def is_cyclic(V, adj):
  
    # Mark all the vertices as not visited
    visited = [False] * V

    # Call the recursive helper function
    # to detect cycle in different DFS trees
    for u in range(V):
      
        # Don't recur for u if it is already visited
        if not visited[u]:
            if is_cyclic_util(u, adj, visited, -1):
                return True

    return False

# Driver program to test above functions
def testCycle():
    V = 3
    adj = [[] for _ in range(V)]

    adj[1].append(0)
    adj[0].append(1)
    adj[0].append(2)
    adj[2].append(0)
    adj[1].append(2)
    adj[2].append(1)

    print("Contains cycle" if is_cyclic(V, adj) else "No Cycle")

    V = 3
    adj2 = [[] for _ in range(V)]

    adj2[0].append(1)
    adj2[1].append(0)
    adj2[1].append(2)
    adj2[2].append(1)

    print("Contains Cycle" if is_cyclic(V, adj2) else "No Cycle")


def test():
    g = Graph()
    g.addedge((0, 1), (5, 3), 15)
    g.addedge((5, 3), (13, 5), 22)
    g.addedge((13, 5), (19, 13), 38)
    g.addedge((19, 13), (19, 19), 10)
    g.addedge((19, 19), (22, 21), 5)
    g.addedge((13, 5), (13, 13), 12)
    g.addedge((13, 13), (19, 13), 10)
    g.addedge((13, 13), (11, 21), 18)
    g.addedge((11, 21), (19, 19), 10)
    g.addedge((5, 3), (3, 11), 22)
    g.addedge((3, 11), (13, 13), 24)
    g.addedge((3, 11), (11, 21), 30)
    #g.print()

    print("Get min distance: ", g.getmindistance((0, 1), (22, 21)))
    print("Get max distance: ", g.getmaxdistance((0, 1), (22, 21)))


testCycle()
