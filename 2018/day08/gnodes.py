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
        self.value = 0
        self.children = []
        
    def addmeta(self, metas):
        global maxdepth, curdepth, metasum, totalsum
        for v in metas:
            metasum += v
            totalsum += v
            self.meta.append(v)
        self.summeta = sum(self.meta)
        
    def addchild(self, child):
            self.children.append(child)

    def sum(self, s = 0):
        s += sum(self.meta)
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
    
A = Node(2, 3)
A.addmeta([1, 1, 2])
B = Node(0, 3)
B.addmeta([10, 11, 12])
A.addchild(B)
C = Node(1, 1)
C.addmeta([2])
A.addchild(C)
D = Node(0, 1)
D.addmeta([99])
C.addchild(D)
'''
2 3                           1 1 2
    0 3 10 11 12 1 1        2 
                     0 1 99



2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
A----------------------------------
    B----------- C-----------
                     D-----

'''

A.out()
print()
print("Metasum: ", metasum, "  Node.sum(): ", A.sum(), "  Total sum: ", totalsum)
