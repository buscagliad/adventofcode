'''

--- Day 21: Chronal Conversion ---

You should have been watching where you were going, because as you wander the new North Pole base, you trip and fall into a very deep hole!

Just kidding. You're falling through time again.

If you keep up your current pace, you should have resolved all of the temporal anomalies by the next time the device activates. Since you have very little interest in browsing history in 500-year increments for the rest of your life, you need to find a way to get back to your present time.

After a little research, you discover two important facts about the behavior of the device:

First, you discover that the device is hard-wired to always send you back in time in 500-year increments. Changing this is probably not feasible.

Second, you discover the activation system (your puzzle input) for the time travel module. Currently, it appears to run forever without halting.

If you can cause the activation system to halt at a specific moment, maybe you can make the device send you so far back in time that you cause an integer underflow in time itself and wrap around back to your current time!

The device executes the program as specified in manual section one and manual section two.

Your goal is to figure out how the program works and cause it to halt. You can only control register 0; every other register begins at 0 as usual.

Because time travel is a dangerous activity, the activation system begins with a few instructions which verify that bitwise AND (via bani) does a numeric operation and not an operation as if the inputs were interpreted as strings. If the test fails, it enters an infinite loop re-running the test instead of allowing the program to execute normally. If the test passes, the program continues, and assumes that all other bitwise operations (banr, bori, and borr) also interpret their inputs as numbers. (Clearly, the Elves who wrote this system were worried that someone might introduce a bug while trying to emulate this system with a scripting language.)

What is the lowest non-negative integer value for register 0 that causes the program to halt after executing the fewest instructions? (Executing the same instruction multiple times counts as multiple instructions executed.)

Your puzzle answer was 5745418.
--- Part Two ---

In order to determine the timing window for your underflow exploit, you also need an upper bound:

What is the lowest non-negative integer value for register 0 that causes the program to halt after executing the most instructions? (The program must actually halt; running forever does not count as halting.)

Your puzzle answer was 5090905.

Both parts of this puzzle are complete! They provide two gold stars: **

NOTE: I decoded the program to rewrite my data.txt program in more efficient
code.  The trick to part 2 is to identify that the sequence (R3, R4) repeats 
after 3911 entries.  Also, there was a trick in that the 'last' R4 value
appears earlier in the sequence, and thus would not be the value for which 
the program needs the most steps.

'''

R1 = R2 = R3 = R4 = R5 = 0

def out(t=""):
    print(R0, R1, R2, R3, R4, R5, t, flush=True)

R3 = 65536			
R4 = 14464005
R0 = 12695433


count = 0
rem = 0
blue = True
check = False

def get_key(l, val):
    for key, value in l.items():
        if val == value:
            return key
    return 0
    
def get_count(l, val):
    n = 0
    for key, value in l.items():
        if val == value:
            n += 1
    return n

count = 0
done = False
def rout(n, cr = False):
    return
    print(n,  end="")
    if cr:
        print()
    else:
        print(",", end="")

pairs = []
R4s = []
while(blue):
    #if check:
    #    R3 = R4 | 65536   
    if check:  
        R3 = R4 | 65536 # line 6
        R4 = 14464005       # line 7
        
    #rout(R3)
    #rout(R4)
    
        
    #rout(R2)
    R2 = R3 & 255       # line 8
    rout(R2)
    #print("Before ", b, "   After ", R2)
    R4 += R2

    R4 &= 0xFFFFFF  
    R4 *= 65899     
    R4 &= 0xFFFFFF 
    #rout(R4)
    #R3 = R2
    #green = False
    check = 0
    if 256 > R3:
        check = 1
        #continue
    else:
        check = 0
    #rout(check)

    if check == 0:
    #    R3 = R4 | 65536
    #else:
        R2 = R3 // 256
        R3 = R2
        count += 1
    #rout(R3, True)
    #if (count > 100000000):
    #    blue = False
    #    print("count exceeded: ", count)
    #    continue        
    else:
        if len(pairs) == 0:
            print("Part 1:  Value that takes least steps to reach: ", R4)
        # print(R3, R4)
        addPair = True
        if R4 in R4s:
            addPair = False
        
        R4s.append(R4)
            
        if (R3,R4) in pairs:
            if not done: print("Part 2:  Value that takes most steps to reach: ", lastR4)
            done = True
            blue=False
        else:
            if addPair:
                pairs.append((R3,R4))
                lastR4 = R4

