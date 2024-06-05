
chnum = [0]*256

for line in open('data.txt'):
    for a in line:
        chnum[ord(a)] += 1

print(chnum[ord('0')])
