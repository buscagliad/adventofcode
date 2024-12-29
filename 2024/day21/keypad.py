'''import os
from pathlib import Path
from time import perf_counter
from itertools import product
timer_script_start=perf_counter()
SCRIPT_PATH=Path(os.path.realpath(__file__))
INPUT_PATH="data.txt"
DIRECTIONS = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)][::2]
UP, RIGHT, DOWN, LEFT = DIRECTIONS
def add(*ps): return tuple(map(sum,zip(*ps)))
def sub(p1,p2):
    return tuple(a-b for a,b in zip(p1,p2))
timer_parse_start=perf_counter()
############################## PARSER ##############################
with open(INPUT_PATH) as file:
    lines = file.read().splitlines()
num_pad_lines = """
789
456
123
.0A
""".strip().splitlines()
dir_pad_lines = """
.^A
<v>
""".strip().splitlines()
print(num_pad_lines)
print(dir_pad_lines)
num_pad = {(i,j):c for i,line in enumerate(num_pad_lines) for j,c in enumerate(line) if c != "."}
dir_pad = {(i,j):c for i,line in enumerate(dir_pad_lines) for j,c in enumerate(line) if c != "."}
num_pad.update({v:k for k,v in num_pad.items()})
dir_pad.update({v:k for k,v in dir_pad.items()})

############################## PART 1 ##############################
def step(source, target, pad):
    ti,tj = pad[target]
    si,sj = pad[source]
    di = ti - si
    dj = tj - sj
    vert = "v"*di+"^"*-di
    horiz = ">"*dj+"<"*-dj
    if dj > 0 and (ti,sj) in pad:
        rpath = vert+horiz+"A"
    elif (si,tj) in pad:
        rpath = horiz+vert+"A"
    elif (ti,sj) in pad:
        rpath = vert+horiz+"A"
    #print("CHEAT:: ", source, si, sj, " to ", target, ti, tj, " ", rpath)
    return rpath
############################## PART 2 ##############################

def routes2(path, pad):
    out = []
    start = "A"
    for end in path:
        out.append(step(start,end,pad))
        start = end
    return Counter(out)












'''
from collections import Counter

#  +---+---+---+
#  | 7 | 8 | 9 |
#  +---+---+---+
#  | 4 | 5 | 6 |
#  +---+---+---+
#  | 1 | 2 | 3 |
#  +---+---+---+
#      | 0 | A |
#      +---+---+
class NumPad():
    def __init__(self):
        self.pad = ["789", "456", "123", " 0A"]
        self.col = 2
        self.row = 3
        self.debug = False
    def find(self, ch):
        for r in range(4):
            for c in range(3):
                if ch == self.pad[r][c]:
                    if self.debug:print("Found ", ch, " at ", r, c)
                    return r, c
        print("ERROR in find: ", ch)

    def goto(self, ch):
        hpath = ""  # horizontal path
        row, col = self.find(ch)
        dr = row - self.row
        dc = col - self.col
    
        if dc > 0: hm = '>' 
        else: hm = '<'
        
        if dr > 0: vm = 'v'
        else: vm = '^'

        hpath = ""  # horizontal path
        for _ in range(abs(dc)): hpath += hm
        vpath = ""  # vertical path
        for _ in range(abs(dr)): vpath += vm
        
        if self.debug:print("Output ", abs(c-self.col), " of ", d)
        if self.debug:print("Output ", abs(r-self.row), " of ", d)
        #
        # determine whether to do horizontal or vertical first
        # we do horizontal first when y == 3
        # we do vertical first when self.row == 3
        # otherwise we do vertical first
        #
            
        if dc > 0 and not self.pad[row][self.col]  == ' ':
            path = vpath+hpath
        elif not self.pad[self.row][col] == ' ':
            path = hpath+vpath
        elif not self.pad[row][self.col] == ' ':
            path = vpath+hpath      
        path += 'A'
        # path2 = step(self.button(), c, self)
        if self.debug: print("KEYPAD:  ", self.button(), self.row, self.col, 
            " to ", ch, row, col,
            ' :: ', path)
        self.moves(path)
        return path

    def move(self, d):
        if self.debug:
            print("Num Pad command: ", d, " current location: ", self.where(), end = "")
        tf, ch = self.domove(d)
        if self.debug:
            print("  new location: ", self.where())
        return tf, ch
    def moves(self, l):
        for a in l:
            self.move(a)
    def domove(self, d):
        if d == '>':
            if self.col < 2 : 
                self.col += 1
                return True, ' '
        elif d == '<':
            if self.row == 3: leftx = 1
            else: leftx = 0
            if self.col > leftx : 
                self.col -= 1
                return True, ' '
        elif d == '^':
            if self.row > 0: 
                self.row -= 1
                return True, ' '
        elif d == 'v':
            if self.col == 0: boty = 2
            else: boty = 3
            if self.row < boty : 
                self.row += 1
                return True, ' '
        elif d == 'A':
            return True, self.button()
        print("Num Pad ERROR - domove ", self.row, self.col, d)
        exit(1)

    def where(self):
        return  self.row, self.col
    def button(self):
        return self.pad[self.row][self.col]
    def out(self):
        print("Num Pad:  x, y: ", self.where(), "   key: ", self.button())

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
class ArrowPad():
    def __init__(self):
        self.pad = [' ^A', '<v>']
        self.col = 2
        self.row = 0
        self.debug = False

    def find(self, ch):
        for r in range(2):
            for c in range(3):
                if ch == self.pad[r][c]:
                    if self.debug:print("Found ", ch, " at ", r, c)
                    return r, c
        print("ERROR in find: ", c)

    def moves(self, l):
        for a in l:
            self.move(a)
    def goto(self, ch):
        hpath = ""
        row, col = self.find(ch)
        if col < self.col: c = '<'
        else: c = '>'
        if self.debug:print("Output ", abs(col-self.col), " of ", ch)
        for _ in range(abs(col-self.col)): hpath += c
        vpath = ""
        if row < self.row: c = '^'
        else: c = 'v'
        if self.debug:print("Output ", abs(row-self.row), " of ", ch)
        for _ in range(abs(row-self.row)): vpath += c
        #
        # determine whether to do x or y first
        # we do y first when self.row == 0 and y == 1
        # we also do y first when self.col > 0 and x == 0
        # otherwise it don't matter
        #

        if self.col < col and self.pad[row][self.col] != ' ':
            path = vpath + hpath
        elif self.pad[self.row][col] != ' ':
            path = hpath + vpath
        else:
            path = vpath + hpath
        
        path += 'A'
        self.moves(path)
        return path

    def move(self, d):
        if d == '>':
            if self.col < 2 : 
                self.col += 1
                return True, ' '
        elif d == '<':
            if ( (self.col == 2) or 
                 (self.col == 1 and self.row == 1) ):
                self.col -= 1
                return True, ' '
        elif d == '^':
            if not (self.row == 1 and self.col == 0): 
                self.row -= 1
                return True, ' '
        elif d == 'v':
            if self.row == 0: 
                self.row += 1
                return True, ' '
        elif d == 'A' or d == 10:
            return True, self.button()
        print("Arrow Pad ERROR - domove ", self.row, self.col, d)
        exit(1)


    def where(self):
        return self.col, self.row
    def button(self):
        if (self.col < 0 or self.col > 2 or
            self.row < 0 or self.row > 1):
            print("ArrowPad - bad xy: ", self.where())
            return 'X'
        return self.pad[self.row][self.col]
    def out(self):
        print("Arrow Pad:  x, y: ", self.where(), "   key: ", self.button())


def decodeA(code):
    N = NumPad()
    for a in code:
        Nt, Nc = N.move(a)
        if Nc == ' ': continue
        print(Nc, end="")
    print()
    
def decodeB(code):
    N = NumPad()
    A1 = ArrowPad()
    A2 = ArrowPad()
    for c in code:
        At, b = A1.move(c)
        if b == ' ': continue
        At, a = A2.move(b)
        if a == ' ': continue
        Nt, Nc = N.move(a)
        if Nc == ' ': continue
        print(Nc, end="")
    print()


def test1():
    A = NumPad()
    for y in range(4):
        for x in range(3):
            print("  ",A.pad[x][y], end="")
        print()
        
    for a in "<>>><<<<vvvv^^^^":
        A.move(a)
        A.out()
    N = NumPad()
    for a in ['>', '<', 'v', '^']:
        N.move(a)
        N.out()

def test2():
    decodeA("<A^A>^^AvvvA")
    decodeA("<A^A^>^AvvvA")
    decodeA("<A^A^^>AvvvA")

def test3():
    decodeB("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A")
    print("Result should be: 029A")
    decodeB("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A")
    print("Result should be: 980A: ")
    decodeB("<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A")
    print("Result should be: 179A: ")
    decodeB("<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")
    print("Result should be: 456A: ")
    decodeB("<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A")
    print("Result should be: 379A: ")
    decodeB("<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")
#test2()
#test3()
#test3()

def compcode(st):
    cc = int(st[:3])
    return cc

codes = ["964A", "246A", "973A", "682A", "180A"]
#codes = ["029A", "980A", "179A", "456A", "379A"]

def shortNcode(N, code):
    seq = ""
    for c in code:
        seq += N.goto(c)
    return seq

def shortAcode(A, code):
    seq = ""
    for c in code:
        seq += A.goto(c)
    return seq

#
# shortAcodes will return a counter with the 
# count of each arrow sequence
#
def shortAcodes(code):
    if DEBUG: print("shortAcodes: ", code)
    seq = []
    A = ArrowPad()
    for c in code:
        for a in c:
            seq.append(A.goto(a))
    cSeq = Counter(seq)
    if DEBUG: print("keypad: ", cSeq)
    return cSeq

def shortNcodes(code):
    seq=[]
    N = NumPad()
    for c in code:
        for a in c:
            seq.append(N.goto(a))
    return Counter(seq)

v = 0
A1 = ArrowPad()
A2 = ArrowPad()
N = NumPad()
DEBUG = False
for c in codes:
    cc = compcode(c)
    sc = shortNcode(N, c)
    #print(c, " --> ", sc)
    #decodeA(sc)
    sc2 = shortAcode(A1, sc)
    #print("SC2: ", sc2)
    sc3 = shortAcode(A2, sc2)
    if DEBUG: 
        print("Code: ", c, "   Length: ", len(sc3), "  Complex: ", cc)
        decodeB(sc3)
        print(sc3)
    v += len(sc3) * cc

print("Part 1: sum of code complexities is: ", v)



'''

v = 0
A1 = ArrowPad()
A2 = ArrowPad()
N = NumPad()
lensc3 = 0
'''
DEBUG = False
numPadPaths = []
for c in codes:
    numPadPaths.append ((shortNcodes(c)))
total = 0
if DEBUG: print("numPadPaths: ", numPadPaths, flush=True)
for _ in range(25):
    updated_paths = []
    for codecounter in numPadPaths:
        # sc is the count of each arrow path
        ncnt=Counter()
        if DEBUG: print("cnts: ", codecounter)
        for sPath, n in codecounter.items():
            dPath = shortAcodes(sPath)
            if DEBUG:print("dPath: ", dPath)
            for p in dPath:
                dPath[p] *= n
            ncnt.update(dPath)
        if DEBUG:print("ncnt: ", ncnt)
        updated_paths.append(ncnt)
    if DEBUG:print(updated_paths)
    numPadPaths = updated_paths

def sumit(nn):
    t = 0
    for code, count in nn.items():
        t += len(code) * count
    return t

mults = [int(c[:-1]) for c in codes]
total = 0

for n,cnts in enumerate(numPadPaths):
    total += mults[n] * sumit(cnts)    

print("Part 2: sum of code complexities is: ", total)
#Part 2: 258263972600402
