def init(fname):
    trees = []
    with open(fname) as f:
       for line in f:
           trees.append(line.strip());
    num_columns = len(trees[0])
    num_rows = len(trees)
    #print("Number of rows: " + str(num_rows))
    #print("Number of columns: " + str(num_columns))
    return trees

def count(t, right, down):
    rc = 0
    c = right
    r = down
    num_columns = len(t[0])
    num_rows = len(t)
    while r < num_rows :
        #print("r = " + str(r) + "  c = " + str(c))
        if t[r][c] == '#' : rc = rc + 1
        r = r + down
        c = c + right
        if  c >= num_columns: c = c - num_columns
    return rc

trees = init('data.txt')
r1d1 = count(trees, 1, 1)
r3d1 = count(trees, 3, 1)
r5d1 = count(trees, 5, 1)
r7d1 = count(trees, 7, 1)
r1d2 = count(trees, 1, 2)
print("Part1: Number of tress for slope (3,1): " + str(count(trees, 3, 1)))
print("Part2: Multiply various slopes: " + str(r1d1 * r3d1 * r5d1 * r7d1 * r1d2))