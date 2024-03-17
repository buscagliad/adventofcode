import copy

#
# this class will create a segment of arbitray size
# this segment can have parts removed or parts added
# At some point: S = union [Li, Ri] i = 1 .. N (if N is 1, this would be
#                        equivalent to the initial segment
# NOTE:  Li <= Ri and Ri < Li+1 for all i
# in(a) is true if Li <= a <= Ri for some i
# length() is the total number of integers that are members of S
#

class Segment:
    def __init__(self, Lower, Upper):
        self.segments = []
        self.segments.append([Lower, Upper])

    def isin(self, n):
        for l, r in self.segments:
            if l <= n <= r:
                return True
        return False

    def first(self): # returns first value in segment
        return self.segments[0][0]

    def last(self):
        return self.segments[-1][1]

    def min(self): # returns first value in segment
        return self.segments[0][0]

    def max(self):
        return self.segments[-1][1]

    def clean(self):
        newseg = []
        lasta = None
        lastb = None
        for i, [a, b] in enumerate(self.segments):
            if i == 0:
                lasta = a
                lastb = b
            else:
                if lastb + 1 == a:
                    lastb = b
                else:
                    newseg.append([lasta, lastb])
                    lasta = a
                    lastb = b
        newseg.append(lasta, lastb)
        self.segments = newseg
            
    def length(self):
        s = 0
        for (a, b) in self.segments:
            s += b - a + 1
        return s
        
    def remove(self, a, b):
        if a > b:
            print("ERROR: remove expects segment [a,b] such that a <= b::  a = ", a, "  b = ", b)
        #print("Remove: ", a, b)
        newseg = []
        for l,r in self.segments:
            # if [a,b] segment is contained in [l,r]
            if l < a and b < r:
                newseg.append([l, a-1])
                newseg.append([b+1,r])
            # if [a,b] segment does not intersect segment [l,r] and this segment
            elif r < a or b < l:
                newseg.append([l,r])
            # if [l,r] is contained in [a,b] - get next segment
            elif a <= l and r <= b:
                continue
            # [l,r] must intersect [a,b]
            #
            #          [a             b]
            #       [l |               |   r]         add [l,a-1] and [b+1,r]
            # [l  r]   |               |    [l  r]    Handled in first if statement
            #          |    [l     r]  |              Handled in second if statement
            # [l       |     r]        |              Case 1: add segment [r+1,b]
            #          |     [l        |       r]     Case 2: add segment [b+1,r]
            #
            elif l <= a and r <= b:     # Case 1
                newseg.append([l, a-1])
            elif l <= b and b <= r:     # Case 2
                newseg.append([b+1,r])
            else:
                print("ERROR")
        self.segments = newseg
                

    def add(self, a, b):
        if a > b:
            print("ERROR: add expects segment [a,b] such that a <= b::  a = ", a, "  b = ", b)
        newseg = []
        #print("Add: ", a, b)
        for l,r in self.segments:
            # if [a,b] segment does not intersect segment [l,r] and this segment
            if r < a or b < l:
                newseg.append([l,r])
            # if [l,r] is contained in [a,b] - get next segment
            elif a <= l and r <= b:
                newseg.append([a,b])
            # [l,r] must intersect [a,b]
            #
            #          [a             b]
            # [l  r]   |               |    [l  r]    Handled in first if statement
            #          |    [l     r]  |              Handled in second if statement
            # [l       |     r]        |              Case 1: add segment [l,b]
            #          |     [l        |       r]     Case 2: add segment [a,r]
            #       [l |               |   r]         Case 3: add [l,r]
            #
            elif l <= a and r <= b:     # Case 1
                newseg.append([l, b])
            elif l <= b and b <= r:     # Case 2
                newseg.append([a,r])
            else:                       # Case 3
                newseg.append([l,r])
        self.segments = newseg

    def output(self):
        t = "Segments: "
        for [a,b] in self.segments:
            print(t, "[", a, ", ", b, "]")
            t = "          "
        print("Length: ", self.length())
          
def segtest():
    s = Segment(100, 1500)
    s.output()
    s.remove(500, 600)
    s.remove(200, 300)
    s.output()
    s.remove(550, 800)
    s.output()
    s.add(50, 100)
    s.output()
    s.add(450, 600)
    s.output()
    s.add(200, 500)
    s.output()
    print("Min: ", s.min(), "  Max: ", s.max())
    print("Length: ", s.length())

