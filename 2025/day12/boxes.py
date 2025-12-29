
boxes=[]


class box():
    def __init__(self, n, l1, l2, l3):
        self.id = n
        self.layout = []
        self.layout.append(l1)
        self.layout.append(l2)
        self.layout.append(l3)

        self.dense = 0
        for a in self.layout:
            for b in a:
                if b=='#': self.dense += 1
        # print (self.id, self.layout, self.dense)
    def spots(self):
        return self.dense

def init(fname):
    # read in entire file
    f = []
    nlines = 0
    for l in open(fname):
        f.append(l.strip())
    #print(f)
    index = 0
    Done = False
    ok = 0
    while not Done:
        if index >= len(f):
            break
        if f[index][1] == ':':
            boxes.append(box(f[index][0], f[index+1], f[index+2], f[index+3]))
            index += 5
        else:
            p = f[index].split(':')
            rowcol = p[0].split('x')
            [row, col] = [int(rowcol[0]), int(rowcol[1])]
            numboxes = [int(a) for a in p[1].split()]
            # print(row, col, numboxes)
            area = row * col
            rarea = 0
            for i, b in enumerate(boxes):
                rarea += boxes[i].spots() * numboxes[i]
            # print(area, rarea, rarea > area)
            if (area > rarea): ok += 1
                
            index += 1
    print("Part 1: ", ok)

init('data.txt')
