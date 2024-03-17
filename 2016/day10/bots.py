
import numpy as np

Bots = {}
Outputs = [1]*3

MICRO_PRODUCT = 1

MICRO_CARE_1 = 17
MICRO_CARE_2 = 61
MICRO_BOT = -1

class Bot:
    def __init__(self, bnum, low, high):
        self.id = bnum
        self.chips = []
        self.low = low
        self.high = high
    def out(self):
        print("BOT: ", self.id, "  LOW: ", self.low, "  HIGH: ", self.high)

    def contains(self, c1, c2):
        return c1 in self.chips and c2 in self.chips
    def add(self, c1):
        global MICRO_BOT
        global Bots
        global Outputs
        global MICRO_PRODUCT
        self.chips.append(c1)
        if self.contains(MICRO_CARE_1, MICRO_CARE_2):
            MICRO_BOT = self.id
        # print("Adding ", c1, " to BOT: ", self.id)
        if len(self.chips) > 1:
            minc = min(self.chips)
            maxc = max(self.chips)
            self.chips.remove(minc)
            if self.low < 0:
                k = -self.low - 1
                if k < 3:
                    Outputs[k] *= minc
                    MICRO_PRODUCT *= minc
            else:
                Bots[self.low].add(minc)
            self.chips.remove(maxc)
            if self.high < 0:
                k = -self.high - 1
                if k < 3:
                    Outputs[k] *= maxc
                    MICRO_PRODUCT *= maxc
               #Outputs[-self.high].append(maxc)
            else:
                Bots[self.high].add(maxc)
        


def moves(val, bot):
    done = False
    while not done:
        Bots[bot].add(val)
        if MICRO_BOT > -1:
            return MICRO_BOT
        done = True
    return -1
#  0   1   2    3   4  5   6   7   8    9  10 11
# bot 91 gives low to bot 133 and high to bot 13
# bot 130 gives low to output 0 and high to bot 51
# value 61 goes to bot 119

def procbot(line):
    global Bots
    w = line.strip().split()
    if w[0] == "bot":
        bid = int(w[1])
        lid = int(w[6])
        hid = int(w[11])
        if w[5] == "output":
            low = -(lid + 1)
        else:
            low = lid
        if w[10] == "output":
            high = -(hid + 1)
        else:
            high = hid
        Bots[bid] = Bot(bid, low, high)

def procadd(line):
    global Bots
    w = line.strip().split()
    if w[0] == "value":
        val = int(w[1])
        bot = int(w[5])
        Bots[bot].add(val)


FILE = "data.txt"
for line in open(FILE):
    procbot(line)

for line in open(FILE):
    procadd(line)

print("Part 1: Micro BOT is ", MICRO_BOT)

print("Part 2: Product of outputs 0, 1 and 2 is ", MICRO_PRODUCT)
