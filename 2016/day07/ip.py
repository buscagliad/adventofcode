
def is_abba(s):
    for i in range(len(s)-3):
        if s[i] == s[i+3] and s[i+1] == s[i+2] and not s[i] == s[i+1]:
            return True
    return False

def get_aba(ll):
    aba = []
    for s in ll:
        for i in range(len(s)-2):
            if s[i] == s[i+2]:
                aba.append(s[i:i+3])
    return aba

def is_mirror(a, b):
    if a[0] == a[2] and b[0] == b[2]:
        if a[0] == b[1] and b[0] == a[1]: 
            return True
    return False

def check_bab_aba(ss, hs):
    A = get_aba(ss)
    B = get_aba(hs)
    for l in A:
        for m in B:
            if is_mirror(l, m): 
                #print(l,m)
                return True
    return False
    
def ip_support(line):
    #print(line)
    lines = []
    hss = []
    i = 0
    while line.find('[') >= 0:
        i1 = line.find('[')
        i2 = line.find(']')
        lines.append(line[:i1])
        hss.append(line[i1+1:i2])
        line = line[i2+1:]
    if len(line) > 0:
        lines.append(line)
    #
    # Part 1 search for ABBA
    #
    abba = False
    for ab in lines:
        if is_abba(ab):
            abba = True
    for hs in hss:
        if is_abba(hs):
            abba = False

    #
    # Part 2 search for ABA
    #
    aba = check_bab_aba(lines, hss)
    
    return abba, aba

part1_count = 0
part2_count = 0
for line in open('data.txt'):
    p1, p2 = ip_support(line.strip())
    if p1: part1_count += 1
    if p2: part2_count += 1


print("Part 1: Number of TLS supporing IP's: ", part1_count)
print("Part 2: Number of SSL supporing IP's: ", part2_count)

# 229 is too low for part2
