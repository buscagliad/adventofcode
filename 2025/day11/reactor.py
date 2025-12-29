from collections import deque

cmap = {}

conns = [] # list of all connections

# Python Code to count paths from source 
# to destinattion using Topological Sort
# found this at https://www.geeksforgeeks.org/dsa/count-possible-paths-two-vertices/
# modified to add 'required' tests
def countPaths(n, edgeList, source, destination, required=None):

    # Create adjacency list (1-based indexing)
    graph = [[] for _ in range(n + 1)]
    indegree = [0] * (n + 1)

    for u, v in edgeList:
        graph[u].append(v)
        indegree[v] += 1

    # Perform topological sort using Kahn's algorithm
    q = deque()
    for i in range(1, n + 1):
        if indegree[i] == 0:
            q.append(i)

    topoOrder = []
    while q:
        node = q.popleft()
        topoOrder.append(node)

        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                q.append(neighbor)

    # Array to store number of ways to reach each node
    ways = [0] * (n + 1)
    ways[source] = 1

    # Traverse in topological order
    for node in topoOrder:
        for neighbor in graph[node]:
            ways[neighbor] += ways[node]

    return ways[destination]

def test_this():

    n = 5

    # Edge list: [u, v] represents u -> v
    edgeList = [
        [1, 2], [1, 3], [1, 5],
        [2, 5], [2, 4], [3, 5], [4, 3]
    ]

    source = 1
    destination = 5

    print(countPaths(n, edgeList, source, destination))


def paths(start, end):
    global conns
        
    n = len(conns)

    return countPaths(n, conns, start, end)
    
        
    
def init(fname, exclude=[]):
    global conns
    global cmap
    conns.clear()
    cmap.clear()
    circ = {}
    #
    # initialize map
    #
    index = 1
    for l in open(fname):
        # ggg: out
        ll = l.strip().split()
        c = ll[0][:3]
        if c in exclude: continue
        ol = []
        cmap[c] = index

        for oc in ll[1:]:
            if oc in exclude: continue
            ol.append(oc)
        
        circ[c] = ol
        index += 1

    cmap['out'] = index
    out_index = cmap['out']
    for key in cmap:
        if key == 'out': continue
        src = cmap[key]
        for des in circ[key]:
            conns.append([src, cmap[des]])

def pathcomp(src, dest, exc):
    global cmap

    init("data.txt", exc)
    s_index = cmap[src]
    d_index = cmap[dest]
    #print(s_index, d_index, len(cmap))
    src_to_dest_exc = paths(s_index, d_index)
    #print(src, " to ", dest, " wihout ", exc, " : ", src_to_dest_exc)
    #print("difference: ", src_to_dest - src_to_dest_exc)
    return src_to_dest_exc
    

# test_this()
# exit(1)
init("data.txt")
print("Part 1: ", pathcomp('you', 'out', []))

A = pathcomp('svr', 'fft', ['dac', 'out'])
B = pathcomp('fft', 'dac', ['svr', 'out'])
C = pathcomp('dac', 'out', ['fft', 'svr'])

D = pathcomp('svr', 'dac', ['fft', 'out'])
E = pathcomp('dac', 'fft', ['svr', 'out'])
F = pathcomp('fft', 'out', ['dac', 'svr'])

print("Part 2: ", A*B*C + D*E*F)
#
# 6141 is too low
# Part 2:  549705036748518


