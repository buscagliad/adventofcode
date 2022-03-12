def valid(pline, part):
    #6-9 b: nbvrbptfbbnbxb
    list=pline.split('-')
    minc = int(list[0])
    list = list[1].split()
    maxc = int(list[0])
    charv = list[1].replace(':', '')
    if (part == 1):
        c = list[2].count(charv)
        if minc <= c and c <= maxc: return True
    else:
        print(pline)
        if list[2][minc-1] == charv  and  list[2][maxc-1] != charv:
            print("{True } Line: " + list[2] + "  charv: " + charv + "  minc = " + str(minc) + "  maxc = " + str(maxc) + "  c1 = " + list[2][minc-1] + "  c2 = " + list[2][maxc-1])
            return True
        elif list[2][minc-1] != charv  and  list[2][maxc-1] == charv:
            print("{True } Line: " + list[2] + "  charv: " + charv + "  minc = " + str(minc) + "  maxc = " + str(maxc) + "  c1 = " + list[2][minc-1] + "  c2 = " + list[2][maxc-1])
            return True
        print("{False} Line: " + list[2] + "  charv: " + charv + "  minc = " + str(minc) + "  maxc = " + str(maxc) + "  c1 = " + list[2][minc-1] + "  c2 = " + list[2][maxc-1])
    return False


with open('data.txt') as f:
    good_passwords_1 = 0
    good_passwords_2 = 0
    for line in f:
        if valid(line, 2) : good_passwords_2 = good_passwords_2 + 1
        if valid(line, 1) : good_passwords_1 = good_passwords_1 + 1

print("Number of good passwords (part 1): " + str(good_passwords_1))
print("Number of good passwords (part 2): " + str(good_passwords_2))
