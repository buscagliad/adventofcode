#
# baggage
#

class container:
    def __init__(color, count)
        self.color = color
        self.count = count

class bag:
    def __init__(color):
        self.color = color
        self.contains []
    def contains(color, count):
        self.contains.append(container(color, count))
    def has(color)
        for b in contains
            if (b.color == color): return True
            return 



def findBags(bag, color, count = 0)
    for c in bag.contains:
            if c.color == color: return b.count
            else: count += findBags(bags, b.color, count)
    return count
        

def findBags(bags, color, count = 0)
    for b in bags:
        for c in b.contains:
            if c.color == color: return b.count
            else: count += findBags(bags, b.color, count)
    return count
        
