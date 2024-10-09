
def process(line):
    s = line.strip().split(',')
    if len(s) < 5: return
    if s[1] == ' 0':
        return
    print(s)

for l in open('flow.txt'):
    process(l)
