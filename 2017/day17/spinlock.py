

class Spin:
    def __init__(self, rate):
        self.spinlist = [0]
        self.nextvalue = 1
        self.current = 0
        self.rate = rate
    def add(self):
        ins = (self.current + self.rate) % (len(self.spinlist))
        newspin = []
        self.current = ins
        newspin.extend(self.spinlist[:ins])
        newspin.append(self.nextvalue)
        newspin.extend(self.spinlist[ins:])
        self.spinlist = newspin
        self.nextvalue += 1
    def out(self):
        print(self.spinlist)

sp = Spin(3)

for i in range(9):
    sp.add()
    sp.out()
