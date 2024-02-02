
FIRST = 20151125
MULT = 252533
DIV = 33554393

# both MULT and DIV are prime

def row1(row):
    s = 1
    r = 0
    for i in range(row-1):
        r += 1
        s += r
    return s

def triangle(row, col):
    rn = row1(row+col-1)
    return rn + col - 1

#for i in range(10):
#    print(i, row1(i))

def test():
    for r in range(1, 10):
        for c in range(1, 10):
            print(triangle(r, c), " ", end = "")
        print()

index = triangle(2981, 3075)


code = FIRST

for i in range(1,index):
    code *= MULT
    code %= DIV

print("Part 1 - machine code: ", code)
