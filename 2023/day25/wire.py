import fileinput
import random
import numpy as np

def connected(M, c, start = 0):
    numverts = len(c)
    vis = np.zeros(numverts, dtype = int)
    travel = []
    travel.append(0)
    while travel:
        i = travel.pop()
        for j in range(numverts):
            if M[i][j]:
                if vis[j]: continue
            else:
                continue
            vis[j] = 1
            travel.append(j)
    #print("Number of vertices: ", numverts, "  Connected from ", start, " is ", sum(vis))
    return sum(vis)
        
def find(parents, i):
    r = i
    while r in parents:
        r = parents[r]
    while i in parents:
        p = parents[i]
        parents[i] = r
        i = p
    return i


def unite(parents, i, j):
    parents[i] = j


def karger(n, edges):
    edges = list(edges)
    random.shuffle(edges)
    parents = {}
    for i, j in edges:
        if n <= 2:
            break
        i = find(parents, i)
        j = find(parents, j)
        if i == j:
            continue
        unite(parents, i, j)
        n -= 1
    count = 0
    # print("******************")
    redges = []
    for (i, j) in edges:
        if find(parents, i) != find(parents, j):
            count += 1
            #print("(",i,",",j,")")
            redges.append((i,j))
    #return sum(find(parents, i) != find(parents, j) for (i, j) in edges)
    return redges

def getminpath(filename):
    lines = list(fileinput.input(filename))
    n = len(lines)
    edges = set()
    for line in lines:
        fields = iter(map(int, line.split()))
        u = next(fields)
        edges.update((min(u, v), max(u, v)) for v in fields)
    mincut = 100000000
    minpath = []
    for k in range(1000):
        kk = karger(n, edges)
        if len(kk) < mincut:
            mincut = len(kk)
            minpath = kk
    return minpath


def aoc(filename):
    edges = []
    edge_count = dict()
    component = []
    connections = set()
    #This code is contributed by Neelam Yadav
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

    num_components = len(edge_count)

    #print("Num_components: ", num_components)
    for ci in component:
        for cj in component:
            if (ci, cj) in connections:
                    if not (cj, ci) in connections:
                        connections.add((cj, ci))

    mat = np.zeros((num_components,num_components), dtype=int)
    tmpfile = "temp.txt"
    f = open(tmpfile, 'w')
    for i, ci in enumerate(component):
        f.write(str(i) + " ")
        for j, cj in enumerate(component):
            if i == j: continue
            if (ci, cj) in connections:
                #print("adding ", i+1, j+1)
                f.write(str(j) + " ")
                # print(ci, cj)
                mat[i][j] = 1
                mat[j][i] = 1
        f.write("\n")
    f.close()
    edgelist = getminpath(tmpfile)
    
    #
    # remove the edges fou
    for (i, j) in edgelist:
        mat[i][j] = 0
        mat[j][i] = 0

    x = connected(mat, component)
    print("Part 1 - Product of separated graphs: ", x * (len(component)-x))

if __name__ == "__main__":
    aoc("data.txt")
