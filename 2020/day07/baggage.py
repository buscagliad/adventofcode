#
# baggage
#
from anytree import Node, RenderTree

class container:
    def __init__(self, color, count):
        self.color = color
        self.count = count
    def display(self):
        print("  ", self.count, " of ", self.color);

class bag:
    def __init__(self, color):
        self.color = color
        self.contains = []
    def add(self, color, count):
        self.contains.append(container(color, count))
        #print("adding color ", color, "  with ", count)
    def has(self, color):
        for c in self.contains:
            if (c.color == color): return c.count
        return 0
    def has(self, color, count = 0):
        for c in self.contains:
            if (c.color == color): count += c.count
        return 0
    def display(self):
        print ("Bag name: ", self.color, " Num contains: ", len(self.contains))
        for b in self.contains:
            b.display()

##
## getBag will search bags for the color requested and return it
def getBag(bags, color):
    for b in bags:
        if b.color == color: return [b, True]
    return [b, False]

##
## tbag is an of object class bag
def countBags(bags, tbag, count = 0):
    #print ("Bag ", str(tbag.color), " has:")
    if len(tbag.contains) == 0: return 0
    for c in tbag.contains:
        [nb, valid] = getBag(bags, c.color)
        #print ("Bag ", str(tbag.color), "  bag: ", c.color, " count ", c.count)
        count += c.count * (countBags(bags, nb) + 1)
    return count


def canContain(bags, bag, color, result = False):
    if result: return True
    if bag.has(color) : 
        return True
    for c in bag.contains:
        if c.color == color: return True
        [nbag, valid] = getBag(bags, c.color)
        if valid: result = canContain(bags, nbag, color)
        if result: return True
    return result

def createTree(fname):
    bagName = ""
    bags = []
    thisCount = 0
   # thisbag = bag("DONTUSE")
    for line in open(fname, 'r'):
        #print("LINE: ", line)
        words = line.split()
        if len(words) < 2: break
        numnext = False
        for w in words:
            #print (w)
            if w == "no": break
            if w == "bag." or w == "bags." : 
                numnext = False
                thisbag.add(bagName, thisCount)
                break;
            if numnext:
                thisCount = int(w)
                numnext = False
                bagName = ""
                #print("int word is " + str(w), "  thisCount ", thisCount)
                continue
            if w == "bags": 
                thisbag = bag(bagName)
                #print ("Creating bag [" + str(bagName) + "]")
                bagName = ""
                continue
            if w == "bags," or w == "bag,"  :
                numnext = True
                thisbag.add(bagName, thisCount)
                continue
            if w == "contain":
                numnext = True
                continue
            if bagName == "":
                bagName = w
            else:
                bagName += ' ' + w
            #print ("bagName ", bagName)
        bagName = ""
        #thisbag.display()
        bags.append(thisbag)
    #print("Bags: ", len(bags))
    #for b in bags:
    #    b.display()
    return bags

bags = createTree("data.txt")

searchBag = "shiny gold"
numberOfStartingBags = 0

for b in bags:
    [nb, valid] = getBag(bags, b.color)
    if valid: 
        #nb.display()
        if canContain(bags, nb, searchBag): numberOfStartingBags += 1
        #print (str(nb.color), " Contains ", searchBag, " ", canContain(bags, nb, searchBag))

print ("Part 1:  Total starting bags ", numberOfStartingBags)

[tbag, valid] = getBag(bags,searchBag)
print ("Part 2:  Total bags in ", searchBag, " is ", countBags(bags, tbag))
