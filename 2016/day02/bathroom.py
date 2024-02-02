
keypad = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]



def process1(line, r, c):
    for a in line:
        if a == 'U':
            r = max(0, r-1)
        elif a == 'D':
            r = min(2, r+1)
        elif a == 'L':
            c = max(0, c-1)
        elif a == 'R':
            c = min(2, c+1)
    return keypad[r][c], r, c

kp2row = ["1", "234", "56789", "ABC", "D"]
kp2col = ["5", "26A", "137BD", "48C", "9"]

kp2 = ["  1  ", " 234 ", "56789", " ABC ", "  D  "]

def process2(line, r, c):

    for a in line:
        ri = r
        ci = c
        if a == 'U':
            ri = max(0, r-1)
        elif a == 'D':
            ri = min(4, r+1)
        elif a == 'L':
            ci = max(0, c-1)
        elif a == 'R':
            ci = min(4, c+1)
        if not kp2[ri][ci] == ' ':
            r = ri
            c = ci
    return kp2[r][c], r, c

r = 1
c = 1
code = 0
dfile = 'data.txt'
for line in open(dfile, 'r'):
    k, r, c = process1(line, r, c)
    code = 10 * code + k

print("Part 1: Bathroom code is: ", code)

scode = ""
r=2
c=0
for line in open(dfile, 'r'):
    k, r, c = process2(line, r, c)
    scode += k

print("Part 2: Bathroom code is: ", scode)
    
