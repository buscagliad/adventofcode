'''

--- Day 8: Memory Maneuver ---

The sleigh is much easier to pull than you'd expect for something its weight. Unfortunately, neither you nor the Elves know which way the North Pole is from here.

You check your wrist device for anything that might help. It seems to have some kind of navigation system! Activating the navigation system produces more bad news: "Failed to start navigation system. Could not read software license file."

The navigation system's license file consists of a list of numbers (your puzzle input). The numbers define a data structure which, when processed, produces some kind of tree that can be used to calculate the license number.

The tree is made up of nodes; a single, outermost node forms the tree's root, and it contains all other nodes in the tree (or contains nodes that contain nodes, and so on).

Specifically, a node consists of:

    A header, which is always exactly two numbers:
        The quantity of child nodes.
        The quantity of metadata entries.
    Zero or more child nodes (as specified in the header).
    One or more metadata entries (as specified in the header).

Each child node is itself a node that has its own header, child nodes, and metadata. For example:

2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
A----------------------------------
    B----------- C-----------
                     D-----

In this example, each node of the tree is also marked with an underline starting with a letter for easier identification. In it, there are four nodes:

    A, which has 2 child nodes (B, C) and 3 metadata entries (1, 1, 2).
    B, which has 0 child nodes and 3 metadata entries (10, 11, 12).
    C, which has 1 child node (D) and 1 metadata entry (2).
    D, which has 0 child nodes and 1 metadata entry (99).

The first check done on the license file is to simply add up all of the metadata entries. In this example, that sum is 1+1+2+10+11+12+2+99=138.

What is the sum of all metadata entries?



Your puzzle answer was 45210.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

The second check is slightly more complicated: you need to find the value of the root node (A in the example above).

The value of a node depends on whether it has child nodes.

If a node has no child nodes, its value is the sum of its metadata entries. So, the value of node B is 10+11+12=33, and the value of node D is 99.

However, if a node does have child nodes, the metadata entries become indexes which refer to those child nodes. A metadata entry of 1 refers to the first child node, 2 to the second, 3 to the third, and so on. The value of this node is the sum of the values of the child nodes referenced by the metadata entries. If a referenced child node does not exist, that reference is skipped. A child node can be referenced multiple time and counts each time it is referenced. A metadata entry of 0 does not refer to any child node.

For example, again using the above nodes:

    Node C has one metadata entry, 2. Because node C has only one child node, 2 references a child node which does not exist, and so the value of node C is 0.
    Node A has three metadata entries: 1, 1, and 2. The 1 references node A's first child node, B, and the 2 references node A's second child node, C. Because node B has a value of 33 and node C has a value of 0, the value of node A is 33+33+0=66.

So, in this example, the value of the root node is 66.

What is the value of the root node?

Your puzzle answer was 22793.

Both parts of this puzzle are complete! They provide two gold stars: **

'''
import sys
sys.setrecursionlimit(10000)

fname = 'data.txt'
nlist = []
DEBUG = False

for line in open(fname):
    w = line.strip().split()
    for a in w:
        nlist.append(int(a))

if DEBUG: print("Sum is: ", sum(nlist), "   length is: ", len(nlist))

depth = 0

nodename = 'A'

class Node:
    def __init__(self, nchilds, nmetas, txt):
        global nodename
        self.nchild = nchilds
        self.nmeta = nmetas
        self.meta = []
        self.children = []
        self.metasum = 0
        self.name = nodename
        nodename = chr(ord(nodename)+1)
        if DEBUG: print(txt, " :: ", self.name, " Created: ", nchilds, nmetas)
        
    def addmeta(self, metas):
        if DEBUG: print(" adding meta: ", metas, " to ", self.name)
        for v in metas:
            self.meta.append(v)
        self.metasum = sum(self.meta)
        
    def addchild(self, child):
        if DEBUG: print(" adding child: ", child.name, " to ", self.name)
        self.children.append(child)

    def sum(self, s = 0):
        s += sum(self.meta)
        for c in self.children:
            s = c.sum(s)
        return s

    def value(self):
        if len(self.children) == 0: return self.metasum

        s = 0
        if DEBUG: print(self.name, ", num children: ", len(self.children))
        for i in self.meta:
            i -= 1
            if i < 0 or i >= len(self.children): continue
            v = self.children[i].value()
            s += v
            if DEBUG: print("i is ", i, "  msum: ", self.children[i].metasum, v, s)
        return s

    def out(self):  
        print(self.nchild, self.nmeta, end = " ")
        if self.nchild > 0:
            for c in self.children:
                c.out()
        for i in self.meta:
            print(i, end = " ")

        
topnode = None
def parseZ(nl, ix, tnode):
    global psum, depth, topnode
    cn = nl[ix]
    mn = nl[ix+1]
    if ix == 0:
        top = True
        tnode = Node(cn, mn, "A")
        topnode = tnode
    else:
        top = False
    ix += 2
    if DEBUG: print("Depth: ", depth, "   ix: ", ix, "   cn: ", cn)
        
    depth += 1
    if DEBUG: print("  At depth: ", depth, "  cn: ", cn, "  mn: ", nl[ix+1])
    for j in range(cn):
        lcn = nl[ix]
        lmn = nl[ix+1]
        Xnode = Node(lcn, lmn, "L")
        if lcn == 0:
            ix += 2
            k = ix+lmn
            Xnode.addmeta(nl[ix:k])
            if DEBUG: print("Zero: ", ix, " : ", k - 1, "   depth = ", depth, nl[ix:k], "  zsum: ", sum(nl[ix:k]))
        else:
            k = parseZ(nl, ix, Xnode)
            ix = k
            Xnode.addmeta(nl[ix:ix+lmn])
            if DEBUG: print(" j of cn:", j, cn, " index: ", ix, " : ", ix+lmn - 1, "   depth = ", depth, nl[ix:ix+lmn])
            k = ix + lmn
        tnode.addchild(Xnode)
        ix = k
        #k+=mn
    if top : 
        if DEBUG: print("Return: ", k, "  summing: ", nl[k:k+mn], " cn/mn: ", cn, mn)
        tnode.addmeta(nl[k:k+mn])
    depth -= 1
    if DEBUG: print("Depth: ", depth, "   returning: ", k)    
    return k
    
k = parseZ(nlist, 0, topnode)

# Part 1: sum of metadata entries is:  45210 -- correct
print("Part 1: sum of metadata entries is: ", topnode.sum())
print("Part 2: value of root node is: ", topnode.value())


'''
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
A----------------------------------
    B----------- C-----------
                     D-----
'''
