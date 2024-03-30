
# 13269

garb = 0
def getscore(line):
    global garb
    depth = 1
    score = 0
    ix = 0
    ingarbage = False
    while ix < len(line.strip()):
        c = line[ix]
        if c == '<':    # start of garbage
            if ingarbage: garb += 1
            ingarbage = True
        elif c == '>':
            ingarbage = False
        elif c == '!':
            ix += 1 # ignore next character
        elif ingarbage:
            garb += 1
        if not ingarbage:
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                score += depth
        ix += 1
    return score

for line in open('data.txt'):
    print("Part 1: score of the river groups is: ", getscore(line))
    
def test():
    print(getscore("{}")) #, score of 1.
    print(getscore("{{{}}}")) #, score of 1 + 2 + 3 = 6.
    print(getscore("{{},{}}")) #, score of 1 + 2 + 2 = 5.
    print(getscore("{{{},{},{{}}}}")) #, score of 1 + 2 + 3 + 3 + 3 + 4 = 16.
    print(getscore("{<a>,<a>,<a>,<a>}")) #, score of 1.
    print(getscore("{{<ab>},{<ab>},{<ab>},{<ab>}}")) #, score of 1 + 2 + 2 + 2 + 2 = 9.
    print(getscore("{{<!!>},{<!!>},{<!!>},{<!!>}}")) #, score of 1 + 2 + 2 + 2 + 2 = 9.
    print(getscore("{{<a!>},{<a!>},{<a!>},{<ab>}}")) #, score of 1 + 2 = 3.

print("Part 2: number of garbage characters is: ", garb)

