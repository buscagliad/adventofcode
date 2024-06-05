import sys
sys.setrecursionlimit(10000)

fname = 'data.txt'
nlist = []
DEBUG = False

for line in open(fname):
    w = line.strip().split()
    for a in w:
        nlist.append(int(a))

if 1 or DEBUG: print("Sum is: ", sum(nlist))
def sumzero(nl):
    done = False
    zsum = 0
    i = 0
    while i < len(nl):
        if nl[i] == 0:
            m = nl[i+1]
            for t in range(i+2,i+2+m):
                zsum += nl[t]

        i += 1
    print("Zero sum is: ", zsum)
sumzero(nlist)
        
psum = 0
zcount = 0

def zset(a, n):
    if a[n] == -1:
        print("zset: ", n)
    else:
        a[n] = -1

def zer(a, n, m):
    for i in range(n, m):
        zset(a, i)

def parseY(nl, sn, en):
    global psum, zcount
    if DEBUG: print(nl, psum)
    if en - sn < 2:
        print("WHAT it is zero?", nl[sn:en+1])
        zer(nl, sn, en+1)
        return 0
    cn = nl[sn]
    mn = nl[sn+1]
    zer(nl, sn, sn+2)
    len_nl = en - sn + 1
    if cn == 0:
        zcount += 1
        s = sn + 2
        e = sn + 2 + mn
        ns = sum(nl[s:e])
        if DEBUG: print("ZERO: ", nl[s:e], "  children: ", cn, 
            "  meta #: ", mn, "   Sum: ", ns, "   RetSum: ", psum)
        psum += ns
        if len_nl < 2:
            print("Problem A: ", nl[sn:en+1])
        zer(nl, s, e)
        parseY(nl, e, en)
        #sm = parse(nl[e:])
    else:
        e = en + 1
        s = en - mn + 1
        ns = sum(nl[s:e])
        zer(nl, s, e)
        psum += ns
        if DEBUG: print("NONO: ", nl[s:e], "  children: ", cn, 
            "  meta #: ", mn, "   Sum: ", ns, "   RetSum: ", psum)
        if (s - 2) < 2:
            print("Problem A: ", nl)
        parseY(nl, sn + 2, s - 1)
    return psum    

def active(l):
    cnt = 0
    for x in l:
        if x >= 0: cnt += 1
    print("active: ", cnt)
    return cnt

while active(nlist) > 0:
    s = -1
    e = -1
    for i, x in enumerate(nlist):
        if x >= 0:
            if s == -1: s = i
            e = i
    print(s, e)
    parseY(nlist, s, e)
        
    

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
        s = e - mn - 1
        ns = sum(nl[s:e])
        psum += ns
        if DEBUG: print("NONO: ", nl[s:e], "  children: ", cn, 
            "  meta #: ", mn, "   Sum: ", ns, "   RetSum: ", psum)
        if (s - 2) < 2:
            print("Problem A: ", nl)
        parseX(nl[2:s+1])
    return psum    
cn = nlist[0]
mn = nlist[1]



# 38777 is too low
# 926 zeroes
#print("Part 1: sum of metadata entries is: ", parseY(nlist, 0, len(nlist)-1), zcount)
print("Part 1: sum of metadata entries is: ", psum, zcount)


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
            
#n = Node(nlist)
    
        
