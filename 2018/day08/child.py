import random

def ranint(low, high):
    x = random.random()
    s = high - low + 1
    y = x * s + low
    return int(y)
    
maxdepth = 10
curdepth = 0
metasum = 0
totalsum = 0
class Node:
    def __init__(self, nchilds, nmetas, depth = 0):
        global maxdepth, curdepth, metasum, totalsum
        curdepth += 1
        self.nchild = nchilds
        self.nmeta = nmetas
        totalsum += nchilds + nmetas
        self.meta = []
        for i in range(nmetas):
            v = ranint(1, 9)
            metasum += v
            totalsum += v
            self.meta.append(v)
        self.summeta = sum(self.meta)
        self.children = []
        for i in range(nchilds):
            if curdepth < maxdepth:
                rch = ranint(0, 2)
            else:
                rch = 0
            rnm = ranint(1, 5)
            self.children.append(Node(rch, rnm, depth+1))

    def sum(self, s = 0):
        s += self.summeta
        for c in self.children:
            s = c.sum(s)
        return s

    def out(self):
        print(self.nchild, self.nmeta, end = " ")
        if self.nchild > 0:
            for c in self.children:
                c.out()
        for i in self.meta:
            print(i, end = " ")
    
n = Node(4, 3)
    
n.out()
print()
print("Metasum: ", metasum, "  Node.sum(): ", n.sum(), "  Total sum: ", totalsum)
