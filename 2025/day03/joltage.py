#
#  Day 03 - joltage
#

def jolt(t, n):
    lt = len(t)
    ten = 10**(n-1)
    s = 0
    ix = 0
    k = n
    for i in range(n):
        for a in "987654321":
            nix = t.find(a, ix, lt-k)
            if nix >= 0:
                s += ten * int(a)
                ten //= 10
                k -= 1
                ix = nix + 1
                break
    return s

p1 = 0
p2 = 0
for l in open('data.txt'):
    j = jolt(l, 2)
    p1 += j
    j = jolt(l, 12)
    p2 += j


print("Part 1: ", p1)
print("Part 2: ", p2)

# Part 1:  17087
# Part 2:  169019504359949
