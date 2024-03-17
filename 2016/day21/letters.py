'''
--- Day 21: Scrambled Letters and Hash ---
The computer system you're breaking into uses a weird scrambling function to store its passwords. It shouldn't be much trouble to create your own scrambled password so you can add it to the system; you just have to implement the scrambler.

The scrambling function is a series of operations (the exact list is provided in your puzzle input). Starting with the password to be scrambled, apply each operation in succession to the string. The individual operations behave as follows:

swap position X with position Y means that the letters at indexes X and Y (counting from 0) should be swapped.
swap letter X with letter Y means that the letters X and Y should be swapped (regardless of where they appear in the string).
rotate left/right X steps means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
rotate based on position of letter X means that the whole string should be rotated to the right based on the index of letter X (counting from 0) as determined before this instruction does any rotations. Once the index is determined, rotate the string to the right one time, plus a number of times equal to that index, plus one additional time if the index was at least 4.
reverse positions X through Y means that the span of letters at indexes X through Y (including the letters at X and Y) should be reversed in order.
move position X to position Y means that the letter which is at index X should be removed from the string, then inserted such that it ends up at index Y.
For example, suppose you start with abcde and perform the following operations:

swap position 4 with position 0 swaps the first and last letters, producing the input for the next step, ebcda.
swap letter d with letter b swaps the positions of d and b: edcba.
reverse positions 0 through 4 causes the entire string to be reversed, producing abcde.
rotate left 1 step shifts all letters left one position, causing the first letter to wrap to the end of the string: bcdea.
move position 1 to position 4 removes the letter at position 1 (c), then inserts it at position 4 (the end of the string): bdeac.
move position 3 to position 0 removes the letter at position 3 (a), then inserts it at position 0 (the front of the string): abdec.
rotate based on position of letter b finds the index of letter b (1), then rotates the string right once plus a number of times equal to that index (2): ecabd.
rotate based on position of letter d finds the index of letter d (4), then rotates the string right once, plus a number of times equal to that index, plus an additional time because the index was at least 4, for a total of 6 right rotations: decab.
After these steps, the resulting scrambled password is decab.

Now, you just need to generate a new scrambled password and you can access the system. Given the list of scrambling operations in your puzzle input, what is the result of scrambling abcdefgh?

Your puzzle answer was gcedfahb.
--- Part Two ---

You scrambled the password correctly, but you discover that you can't actually modify the password file on the system. You'll need to un-scramble one of the existing passwords by reversing the scrambling process.

What is the un-scrambled version of the scrambled password fbgdceah?

Your puzzle answer was hegbdcfa.

Both parts of this puzzle are complete! They provide two gold stars: **




'''

import copy
from itertools import permutations

forward=[]

def rotate(inl, d):
    # slice string in two parts for left and right
    if (d < 0):
        d = -d
        first = inl[0 : d]
        second = inl[d :]
    else:
        first = inl[0 : len(inl)-d]
        second = inl[len(inl)-d : ]
    return second + first

debug = False

def modpwd(line, pwd):
    if (debug) : print(line.strip())
    w = line.strip().split()
    newpwd=""
    match w[0]:
        case "swap":
            if w[1] == "position":
                a = int(w[2])
                b = int(w[5])
            else:
                a = pwd.find(w[2])
                b = pwd.find(w[5])
            n = min(a, b)
            m = max(a, b)
            #   0     6
            #   abcdefghi
            #   gbcdefahi
            newpwd = pwd[:n] + pwd[m] + pwd[n+1:m] + pwd[n] + pwd[m+1:]
        case "rotate":
            if w[1] == "based": 
                a = w[6]
                n = pwd.find(a)
                if (n >= 4): n += 1
                n += 1
                n = n % len(pwd)
                newpwd = rotate(pwd, n)
            else:
                d = int(w[2])
                if w[1] == "left":
                    d = -d
                    rot = "right"
                else:
                    rot = "left"
                newpwd = rotate(pwd, d)
                
        case "move":
#move position X to position Y means that the letter which is at index X should be 
#removed from the string, then inserted such that it ends up at index Y.
            a = int(w[2])
            b = int(w[5])
            mvletter = pwd[a]
            tmp = pwd[:a]+pwd[a+1:]
            newpwd = tmp[:b] + mvletter + tmp[b:]
            
        case "reverse":
            a = int(w[2])
            b = int(w[4])
            newpwd = pwd[:a]
            for a in reversed(pwd[a:b+1]):
                newpwd += a
            newpwd += pwd[b+1:]
    return newpwd

def proclist(l, pwd):
    npwd = copy.deepcopy(pwd)

    for c in l:
        #print(npwd)
        npwd = modpwd(c, npwd)
    return npwd

def process(line, pwd):
    newpwd = modpwd(line, pwd)
    if (debug) : 
        print(pwd, " --> ", newpwd)
    return newpwd

def test():
    pwd ='abcde'
    pwd = process("swap position 4 with position 0", pwd)   # swaps the first and last letters, producing the input for the next step, ebcda.
    pwd = process("swap letter d with letter b", pwd)       # swaps the positions of d and b: edcba.
    pwd = process("reverse positions 0 through 4", pwd)     # causes the entire string to be reversed, producing abcde.
    pwd = process("rotate left 1 step" , pwd)               # shifts all letters left one position, causing the first letter to wrap to the end of the string: bcdea.
    pwd = process("move position 1 to position 4", pwd)     # removes the letter at position 1 (c), then inserts it at position 4 (the end of the string): bdeac.
    pwd = process("move position 3 to position 0", pwd)     # removes the letter at position 3 (a), then inserts it at position 0 (the front of the string): abdec.
    pwd = process("rotate based on position of letter b", pwd) 
    # finds the index of letter b (1), then rotates the string right once plus a number of times equal to that index (2): ecabd.
    pwd = process("rotate based on position of letter d", pwd) # finds the index of letter d (4), then rotates the string right once, plus a number of times equal to that index, plus an additional time because the index was at least 4, for a total of 6 right rotations: decab.
    # After these steps, the resulting scrambled password is decab.



debug = False
input_string = "abcdefgh"
        
 
part1 = ""
part2 = ""
for ppwd in permutations(input_string):
    pwd = ''.join(ppwd)
    npwd = pwd
    for line in open('data.txt'):
        npwd = process(line, npwd)
    if (pwd == 'abcdefgh'):
        part1 = npwd
    if(npwd == "fbgdceah"):
        part2 = pwd
        break

print("Part 1: new pass code is: ", part1)
print("Part 2: starting key is: ", part2)
