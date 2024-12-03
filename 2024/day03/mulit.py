'''
--- Day 3: Mull It Over ---

"Our computers are having issues, so I have no idea if we have any Chief Historians in stock! You're welcome to check the warehouse, though," says the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop. The Historians head out to take a look.

The shopkeeper turns to you. "Any chance you can see why our computers are having issues again?"

The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. All of the instructions have been jumbled up!

It seems like the goal of the program is just to multiply some numbers. It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly, mul(123,4) would multiply 123 by 4.

However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored, even if they look like part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

For example, consider the following section of corrupted memory:

xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))

Only the four highlighted sections are real mul instructions. Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?

Your puzzle answer was 179571322.
--- Part Two ---

As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact. If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.

There are two new instructions you'll need to handle:

    The do() instruction enables future mul instructions.
    The don't() instruction disables future mul instructions.

Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))

This corrupted memory is similar to the example from before, but this time the mul(5,5) and mul(11,8) instructions are disabled because there is a don't() instruction before them. The other mul instructions function normally, including the one at the end that gets re-enabled by a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).

Handle the new instructions; what do you get if you add up all of the results of just the enabled multiplications?

Your puzzle answer was 103811193.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

def pmul(xy):
    a = b = 0
    #print(xy[:9])
    for i in range(4):
        d = xy[i]
        if d.isdigit():
            a = a * 10 + int(d)
            #print(a, d)
        else:
            break
    if xy[i] != ',': 
        #print("i ",i, xy[i]) 
        return 0
    for j in range(i+1,i+5):
        d = xy[j]
        if d.isdigit():
            b = b * 10 + int(d)
        else:
            break
    if xy[j] != ')':
        #print("j ",j, xy[j]) 
        return 0
    #print(a, " * ", b, " = ", a*b)
    return a*b

domul = True
def mul(l, part2 = False):
    global domul
    sm = 0
    w = l
    while True:
        #print(w)
        s = w.find("mul")
        if s == -1: break
        if part2:
            dt = w.find("don't()")
            if dt >0 and dt < s:
                w = w[dt+4:]
                domul = False
                continue
            dd = w.find("do()")
            if dd > 0 and dd < s:
                domul = True
                w = w[dd+4:]
                continue
            
            
        if s >= 0:
            #print(w[s:])
            if w[s+3] == "(":
                v = pmul(w[s+4:])
                if domul: sm += v
                #print(sm, v)
                w = w[s+4:]
            else:
                w = w[s+4:]
        else:
            break
    #print(sm)
    return sm

s = 0
for line in open('data.txt'):
    k = mul(line)
    s += k
    #print(s, k)

print("Part 1: valid multiplies sum to: ", s)

s = 0
for line in open('data.txt'):
    k = mul(line, True)
    s += k
    #print(s, k)
print("Part 2: valid multiplies sum to: ", s)

# Part 2: valid multiplies sum to:  105264641 -- too high
