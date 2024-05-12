
import os
TMP_FILE = "/tmp/guards.py.tmp"
SRC_FILE = "data.txt"

sorts = "sort " + SRC_FILE + " > " + TMP_FILE

os.system(sorts)   

Guards = {}

MINS_IN_MONTH = 31 

daymonths = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
mday = []
s = 0
for a in daymonths:
    mday.append(s)
    s += a
#print(mday)

def yearmin(month, day, hour, minute):
    daynum = mday[month] + day
    return daynum * 24 * 60 + hour * 60 + minute


class Guard:
    def __init__(self, num, m):
        self.gnum = num
        self.sleep = 0
        self.lastsleep = 0
        self.lastawake = 0
        self.shiftstart = m
        self.amins = [0] * 24*60

    def asleep(self, month, day, hour, minute):
        m = yearmin(month, day, hour, minute)
        self.lastsleep = hour * 60 + minute
        
    def awake(self, month, day, hour, minute):
        m = yearmin(month, day, hour, minute)
        self.lastawake = hour * 60 + minute
        self.sleep += self.lastawake - self.lastsleep
        for i in range(self.lastsleep, self.lastawake):
            self.amins[i] += 1

    def shift(self, month, day, hour, minute):
        m = yearmin(month, day, hour, minute)
        self.shiftstart = m
        


'''
00000000001111111111222222222233333333334444444444
01234567890123456789012345678901234567890123456789
[1518-02-20 00:01] Guard #2777 begins shift
[1518-02-20 00:16] falls asleep
[1518-02-20 00:20] wakes up
[1518-02-20 00:46] falls asleep
[1518-02-20 00:53] wakes up 
'''

guard = "-1"
for line in open(TMP_FILE):
    year = int(line[1:5])
    month = int(line[6:8])
    day = int(line[9:11])
    hour = int(line[12:14])
    minute = int(line[15:17])
    toyear = yearmin(month, day, hour, minute)
    w = line[26:].split()
    match(line[19:24]):
        case "Guard":
            guard = int(w[0])
            if guard in Guards:
                Guards[guard].shift(month, day, hour, minute)
            else:
                Guards[guard] = Guard(guard, toyear)
        case "falls":
            Guards[guard].asleep(month, day, hour, minute)
        case "wakes":
            Guards[guard].awake(month, day, hour, minute)

tn = 0
maxsleep = 0
for n in Guards:
    g = Guards[n]
    if g.sleep > maxsleep:
        maxsleep = g.sleep
        tn = n
    #print(g.gnum, " :  sleeps: ", g.sleep)
    
v = max(Guards[tn].amins)
mm = Guards[tn].amins.index(v)
gid = Guards[tn].gnum
#print(gid, Guards[tn].sleep, mm)

print("Part 1: Guard ID: ", gid, "  most minute: ", mm, "  product: ", mm * gid)

mv = 0
mg = 0
mm = 0
for n in Guards:
    g = Guards[n]
    v = max(g.amins)
    m = g.amins.index(v)
    gid = g.gnum
    if v > mv:
        mv = v
        mg = gid
        mm = m
    
print("Part 2: Guard id: ", mg, "  Minute: ", mm, "  Product: ",  mm * mg)

os.system("rm " +  TMP_FILE)
