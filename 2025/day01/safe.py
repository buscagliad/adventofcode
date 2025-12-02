#
#  Day 01 - safe
#

class Safe:
    def __init__(self):
        self.dial = 50
        self.zeros = 0
        self.anyzeros = 0
        self.debug = False
    def state(self, lr, d, v, ez, az):
        a = 0
        if self.dial < 0 or self.dial > 99:
            print("ERROR", self.dial)
            exit(1)
        self.zeros += ez
        self.anyzeros += az
        if self.debug: print(lr, "Val: ", v, "  Last dial: ", d, "  Cur dial: ", self.dial, "  Z: ", self.zeros, "(", ez, ")", " AZ: ", self.anyzeros, "(", az, ")")
    def right(self, v):
        sv = v
        sd = self.dial
        tozero = 100 - self.dial
        anyz = 0
        zers = 0
        if v >= tozero:
            anyz += 1
            v -= tozero
            while v >= 100:
                v -= 100
                anyz += 1
            self.dial = v
        else:
            self.dial += v

        if self.dial == 0:
            zers += 1
        self.state("r", sd, sv, zers, anyz)
    def left(self, v):
        sv = v
        sd = self.dial
        anyz = 0
        zers = 0
        if self.dial == 0:
            tozero = 100
        else:
            tozero = self.dial
        if v >= tozero:
            anyz += 1
            v -= tozero
            while v >= 100:
                v -= 100
                anyz += 1
            if v == 0:
                self.dial = 0
            else:
                self.dial = 100 - v
        else:
            self.dial -= v
            self.dial += 100
            self.dial %= 100
            
        if self.dial == 0:
            zers += 1
        self.state("l", sd, sv, zers, anyz)

safe = Safe ()

def runit():
    for l in open('data.txt'):
        lr = l[0]
        v = int(l[1:])
        #int(lr, v)
        if lr == 'L': safe.left(v)
        elif lr == 'R': safe.right(v)

    print("Part 1: Number of zeros: ", safe.zeros)
    print("Part 2: Number of total zeros: ", safe.anyzeros)

runit()


