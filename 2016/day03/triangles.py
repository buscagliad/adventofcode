import numpy as np

dfile = 'data.txt'

def procfile(df):
    count = 0
    for line in open(df, 'r'):
        w = line.strip().split()
        # print(w)
        ss = [int(w[0]), int(w[1]), int(w[2])]
        ss.sort()
        # print(ss)
        if sum(ss[:2]) > ss[2]: count += 1
    return count


def proc2file(df):
    count = 0
    f = open(df, "r")
    lines = f.readlines()
    numlines = len(lines)
    # print(numlines)
    li = 0
    while li < numlines:
        # print(lines)
        ts = np.zeros((3,3), dtype = int)
        for i in range(3):
            line = lines[li]
            w = line.strip().split()
            ts[0][i] = int(w[0])
            ts[1][i] = int(w[1])
            ts[2][i] = int(w[2])
            # print(ss)
            li += 1
        for k in range(3):
            ss = ts[k]
            ss.sort()
            if sum(ss[:2]) > ss[2]: count += 1
    return count

print("Part 1: Number of triangles is: ", procfile(dfile))
print("Part 2: Number of triangles is: ", proc2file(dfile))
