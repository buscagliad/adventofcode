import sys
sys.setrecursionlimit(10000)

fname = 'test.txt'
nlist = []
DEBUG = True

for line in open(fname):
    w = line.strip().split()
    for a in w:
        nlist.append(int(a))

if 1 or DEBUG: print("Sum is: ", sum(nlist))

psum = 0

def parseY(nl):
    global psum
    if DEBUG: print(nl, psum)
    if len(nl) < 2:
        if 1 or DEBUG: print("WHAT it is zero?", nl)
        return 0
    cn = nl[0]
    mn = nl[1]
    if cn == 0:
        s = 2
        e = 2 + mn
        ns = sum(nl[s:e])
        if DEBUG: print("ZERO: ", nl[s:e], "  children: ", cn, 
            "  meta #: ", mn, "   Sum: ", ns, "   RetSum: ", psum)
        psum += ns
        if (len(nl) - e) < 2:
            print("Problem A: ", nl)
        if (e < len(nl)): parseX(nl[e:])
        #sm = parse(nl[e:])
    else:
        e = len(nl)
        s = e - mn
        ns = sum(nl[s:e])
        psum += ns
        if DEBUG: print("NONO: ", nl[s:e], "  children: ", cn, 
            "  meta #: ", mn, "   Sum: ", ns, "   RetSum: ", psum)
        if (s - 2) < 2:
            print("Problem A: ", nl)
        parseX(nl[2:s])
    return psum

zcount = 0
def parseX(nl):
    global psum, zcount
    if DEBUG: print(nl, psum)
    if len(nl) < 2:
        if 1 or DEBUG: print("WHAT it is zero?", nl)
        return 0
    cn = nl[0]
    mn = nl[1]
    if cn == 0:
        zcount += 1
        s = 2
        e = 2 + mn
        ns = sum(nl[s:e])
        if DEBUG: print("ZERO: ", nl[s:e], "  children: ", cn, 
            "  meta #: ", mn, "   Sum: ", ns, "   RetSum: ", psum)
        psum += ns
        if (len(nl) - e) < 2:
            print("Problem A: ", nl)
        if (e < len(nl)): parseX(nl[e:])
        #sm = parse(nl[e:])
    else:
        e = len(nl)
        s = e - mn
        ns = sum(nl[s:e])
        psum += ns
        if DEBUG: print("NONO: ", nl[s:e], "  children: ", cn, 
            "  meta #: ", mn, "   Sum: ", ns, "   RetSum: ", psum)
        if (s - 2) < 2:
            print("Problem A: ", nl)
        parseX(nl[2:s])
    return psum    
cn = nlist[0]
mn = nlist[1]


def sumzero(nl):
    done = False
    zsum = 0
    while len(nl):
        i = 0
        for key in range(0, 12):
            if i >= len(nl): break
            if nl[i] == key:
                mc = nl[i+1]
                s = i + 2
                e = s + mc
                q = sum(nl[s:e])
                print(nl[i:e], q)
                zsum += q
                nl = nl[:i] + nl[e:]
            else:
                i += 1
    print("Zero sum is: ", zsum)
        
# 38777 is too low
print("Part 1: sum of metadata entries is: ", parseX(nlist), zcount)

#sumzero(nlist)
'''
class Node:
    def __init__(self, nchild, nmeta, array):
        self.nchild = nchild
        self.nmeta = nmeta
        self.meta = array
        self.val = sum(array)
        self.children = []
    def add(self. nchild, nmeta, array):
        self.children.append(Node(nchild, nmeta, array)
'''    
class Node:
    def __init__(self, s):
        nchild = s[0]
        nmeta = s[1]
        self.meta = 0
        if nchild == 0:
            mds = 2             # metadata start
            mde = 2 + nmeta     # metadata end
            self.meta += sum(s[mds:mde])
            self.children.append((Node(s[mde:])))
        else:
            self.children = []
            mds = len(s)-nmeta-1   # metadata start
            mde = len(s)           # metadata end
            self.meta += sum(s[mds:mde])
            self.children.append(Node(s[2:mds]))
    def value(self, s = 0):
        s += self.meta
        
        for i, c in enumerate(self.children):
            s = value(c, s)
        
        return s
            
n = Node(nlist)
    
        
