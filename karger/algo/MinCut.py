import copy
import math
import random
import matplotlib as mpt
import os


def MinCut(graph, t):
    global cuts
    while len(graph) > t:
        # TODO: use importance sampling
        start = random.choice(list(graph.keys()))
        finish = random.choice(graph[start])

        # print start, finish
        # # Adding the edges from the absorbed node:
        for edge in graph[finish]:
            if edge != start:  # this stops us from making a self-loop
                graph[start].append(edge)

        # # Deleting the references to the absorbed node and changing them to the source node:
        for edge in graph[finish]:
            graph[edge].remove(finish)
            if edge != start:  # this stops us from re-adding all the edges in start.
                graph[edge].append(start)
        del graph[finish]

    # # Calculating and recording the mincut
    mincut = len(graph[list(graph.keys())[0]])
    cuts.append(mincut)
    # print graph
    return graph


def FastMinCut(graph):

    if len(graph) < 6:
        return MinCut(graph, 2)
    else:
        t = 1 + int(len(graph) / math.sqrt(2))
        graph_1 = MinCut(graph, t)
        graph_2 = MinCut(graph, t)
        if len(graph_1) > len(graph_2):
            return FastMinCut(graph_2)
        else:
            return FastMinCut(graph_1)

# return min(FastMinCut(graph_1), FastMinCut(graph_2))

def read_karger(filename):
    global graph    # graph[node] is assigned a list of nodes it is connected to
    global cuts     
    global edge_list
    global edge_num
    graph_file = open(filename)
    cuts = []
    edge_num = 0
    # print "Loading from", filename
    for line in graph_file:
        node = int(line.split()[0])
        edges = []
        for edge in line.split()[1:]:
            edges.append(int(edge))
        graph[node] = edges
        edge_num = edge_num + len(edges)
        edge_list.append(len(edges))
    graph_file.close()

def write_matrix(filename):
    global graph
    f = open(filename, 'w')
    for j in range(1, len(graph) + 1):
        for i in range(1, 201):
            if i not in graph[j]:
                f.write('0 ')
            else:
                f.write('1 ')
        f.write('\n')
    f.close()    

def read_aoc(filename):
    global graph
    global cuts
    global edge_list
    global edge_num
    for line in open(filename):
        ws = line.strip().split()
        node = int(line.split()[0])
        edges = []
        for edge in line.split()[1:]:
            edges.append(int(edge))
        graph[node] = edges
        edge_num = edge_num + len(edges)
        edge_list.append(len(edges))
    graph_file.close()

    for line in open(filename):
        ws = line.strip().split()
        fe = ws[0][0:3]
        if fe in edge_count.keys():
            edge_count[fe] += 1
        else:
            component.append(fe)
            edge_count[fe] = 1
        for w in ws[1:] :
            connections.add((fe, w))
            edges.append((fe, w))
            if w in edge_count.keys():
                edge_count[w] += 1
            else:
                component.append(w)
                edge_count[w] = 1
                

edge_list = []
cuts = []
graph = {}
edge_num = 0

def main():
    read_karger("../data/KargerMinCut.txt")

    write_matrix('../data/matrix.txt')

    # # print the general info of the graph.
    count = 200
    i = 0
    mincut = 10000000
    mingraph = {}
    while i < count:
        graph1 = copy.deepcopy(graph)
        g = MinCut(graph1, 2)
        # g = FastMinCut(graph1)
        i += 1
        thiscut = len(graph[list(graph.keys())[0]])
        if thiscut < mincut:
            mincut = thiscut
            mingraph = copy.deepcopy(g)

    print("Total edges:     ", edge_num / 2)
    print("Total vertices:  ", len(graph))
    print("Maximum degree:  ", max(edge_list))
    print("Minimum degree:  ", min(edge_list))
    print("average degree:  ", sum(edge_list) / len(edge_list))
    print("Runing times:    ", len(cuts))
    # print() cuts
    # print() "Maxcut is", max(cuts)
    print("Mincut is        ", min(cuts))
    print("Min graph:       ", mingraph)

if __name__ == '__main__':
    main()
