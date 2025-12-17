import time



class Player:
    def __init__(self, idx, numstars, laststar):
        global roster
        self.idx = idx
        self.name = roster.getPlayerName(idx)
        self.laststar = laststar
        self.numstars = numstars
        self.email = roster.getPlayerEmail(idx)
        self.problems = [[0,0]]*26
        self.lastStarDate = 0
        self.lastPuzzle = ""

    def addDay(self, day, p1, p2=0):
        self.problems[day] = [int(p1), int(p2)]
        # print(self.name, " adding day ", day, " times: ", int(p1), int(p2))
        if p1 > self.lastStarDate:
            self.lastStarDate = p1
            self.lastPuzzle = "Day " + str(day) + " Part 1"
        if p2 > self.lastStarDate:
            self.lastStarDate = p2
            self.lastPuzzle = "Day " + str(day) + " Part 2"
    def out(self):
        print("***  ", self.name)
        print()
        tm = time.localtime(self.laststar)
        stm = time.strftime("%d %b %Y %H:%M:%S", tm)
        print(" Number of stars: ", self.numstars, end="")
        if (self.numstars > 0) : print ("      Last Star: ", stm);
        else:  print()
        for d in range(len(self.problems)):
            t1, t2 = self.problems[d]
            if t1 == 0 and t2 == 0: continue
            sp = ""
            if d < 10: sp = " "
            
            print("   Day ", sp, d, end = "", sep = "")
            print("   Part 1: ", pltime(t1), end = "", sep = "")
            if t2 > 0:
                print("   Part 2: ", pltime(t2), end = "", sep = "")
            print()
        print()

    def simpleout(self, n):
        if (n == 0):
            print("    Name                        # Stars  Last Star Achieved")
            return
        tm = time.localtime(self.laststar)
        stm = time.strftime("%d %b %Y %H:%M:%S", tm)
        if (self.numstars == 0) : stm = ""
        print(f'{n:2d}  {self.name:30}  {self.numstars:3d}  {stm}')

    def csvOut(self, csvFile, hdr=False):
        if hdr:
            csvFile.write("Stars,Name,Last Star,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25\n")
        else:
            if self.numstars == 0: return
            csvFile.write("%d" %(self.numstars))
            csvFile.write(",%s"  %(self.name))
            csvFile.write(",%s"  %(pltime(self.lastStarDate)))
            for one,two in self.problems[1:]:
                if two: day = 2
                elif one: day = 1
                else: day = 0
                csvFile.write(",%d"  %(day))
            csvFile.write("\n")

class Roster:
    def __init__(self, fname):
        self.Roster = {}
        for l in open(fname):
            w = l.strip().split(',')
            self.Roster[int(w[0])] = [w[1],w[2],False]

    def getPlayerName(self, idx):
        if idx in self.Roster.keys():
            self.Roster[idx][2] = True
            return self.Roster[idx][0]
        else:
            print("ERROR - XXX no such player index: ", idx)
            return "ERROR"

    def getPlayerEmail(self, idx):
        if idx in self.Roster.keys():
            return self.Roster[idx][1]
        else:
            print("ERROR - YYY no such player index: ", idx)
            return "ERROR"

    def nonexist(self):
        for idx in self.Roster.keys():
            if not self.Roster[idx][2]:
                print(idx, self.Roster[idx])
        
    def out(self):
        print(self.Roster.keys())
        for k, v in self.Roster.items():
            print(k, v)

#
# returns True if p1 is better than p2
# either more stars OR
# last star was earlier
#
def plcomp(p1, p2):
    if p1.numstars == p2.numstars:
        if p1.laststar < p2.laststar:
            return -1
        else:
            return 1
    if p1.numstars > p2.numstars:
        return -1
    else:
        return 1

def pltime(t):
    tm = time.localtime(t)
    stm = time.strftime("%d %b %Y %H:%M:%S", tm)
    return stm

roster = Roster("roster.csv")
