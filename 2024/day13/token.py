'''
--- Day 13: Claw Contraption ---
Next up: the lobby of a resort on a tropical island. The Historians take a moment to admire the hexagonal floor tiles before spreading out.

Fortunately, it looks like the resort has a new arcade! Maybe you can win some prizes from the claw machines?

The claw machines here are a little unusual. Instead of a joystick or directional buttons to control the claw, these machines have two buttons labeled A and B. Worse, you can't just put in a token and play; it costs 3 tokens to push the A button and 1 token to push the B button.

With a little experimentation, you figure out that each machine's buttons are configured to move the claw a specific amount to the right (along the X axis) and a specific amount forward (along the Y axis) each time that button is pressed.

Each machine contains one prize; to win the prize, the claw must be positioned exactly above the prize on both the X and Y axes.

You wonder: what is the smallest number of tokens you would have to spend to win as many prizes as possible? You assemble a list of every machine's button behavior and prize location (your puzzle input). For example:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
This list describes the button configuration and prize location of four different claw machines.

For now, consider just the first claw machine in the list:

Pushing the machine's A button would move the claw 94 units along the X axis and 34 units along the Y axis.
Pushing the B button would move the claw 22 units along the X axis and 67 units along the Y axis.
The prize is located at X=8400, Y=5400; this means that from the claw's initial position, it would need to move exactly 8400 units along the X axis and exactly 5400 units along the Y axis to be perfectly aligned with the prize in this machine.
The cheapest way to win the prize is by pushing the A button 80 times and the B button 40 times. This would line up the claw along the X axis (because 80*94 + 40*22 = 8400) and along the Y axis (because 80*34 + 40*67 = 5400). Doing this would cost 80*3 tokens for the A presses and 40*1 for the B presses, a total of 280 tokens.

For the second and fourth claw machines, there is no combination of A and B presses that will ever win a prize.

For the third claw machine, the cheapest way to win the prize is by pushing the A button 38 times and the B button 86 times. Doing this would cost a total of 200 tokens.

So, the most prizes you could possibly win is two; the minimum tokens you would have to spend to win all (two) prizes is 480.

You estimate that each button would need to be pressed no more than 100 times to win a prize. How else would someone be expected to play?

Figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?

Your puzzle answer was 29187.

--- Part Two ---
As you go to win the first prize, you discover that the claw is nowhere near where you expected it would be. Due to a unit conversion error in your measurements, the position of every prize is actually 10000000000000 higher on both the X and Y axis!

Add 10000000000000 to the X and Y position of every prize. After making this change, the example above would now look like this:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279
Now, it is only possible to win a prize on the second and fourth claw machines. Unfortunately, it will take many more than 100 presses to do so.

Using the corrected prize coordinates, figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?

Your puzzle answer was 99968222587852.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

prizeAdd = 0

def solve(A1, B1, T1, A2, B2, T2):
    T1 += prizeAdd
    T2 += prizeAdd
    Bn = A2*T1-A1*T2
    Bd = B1*A2-B2*A1
    Ad = B2*A1-B1*A2
    An = B2*T1-B1*T2
    A = int(An / Ad + 0.5)
    B = int(Bn / Bd + 0.5)
    T1x = A*A1 + B*B1
    T2x = A*A2 + B*B2
    #print(Bn, Bd, Bn/Bd, B, An, Ad, An/Ad, A)
    if T1x == T1 and T2x == T2:
        return A, B
    return 0, 0
# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400
def pline(l):
    n1 = l.find("X+") + 2
    n2 = n1 + l[n1:].index(",")
    #print(l[n1:n2])
    A = int(l[n1:n2])
    n1 = l.find("Y+") + 2
    #print(l[n1:len(l)])
    B = int(l[n1:len(l)])
    return A, B
    
def process(l1, l2, l3):
    A1, B1 = pline(l1)
    A2, B2 = pline(l2)
    
    n1 = l3.find("X=") + 2
    n2 = n1 + l3[n1:].index(",")
    #print(l[n1:n2])
    T1 = int(l3[n1:n2])
    n1 = l3.find("Y=") + 2
    #print(l[n1:len(l)])
    T2 = int(l3[n1:len(l3)])
    A, B = solve(A1, A2, T1, B1, B2, T2)
    if A > 0: 
        #print(A, B, 3*A+B)
        return 3*A + B
    return 0
    
def procfile(fn, pa):
    global prizeAdd
    n = 0
    nt = 0
    ngames = 0
    prizeAdd = pa
    for l in open(fn):
        if n == 0: 
            l1 = l
        elif n == 1: 
            l2 = l
        elif n == 2: 
            l3 = l
        elif n == 3:
            ngames += 1
            nt += process(l1, l2, l3)
            n = -1
        n += 1
    return nt

PA = 10000000000000

print("Part 1: minimum number of tokens: ", procfile('data.txt', 0))
print("Part 2: minimum number of tokens: ", procfile('data.txt', PA))
    
#print(pline("Button A: X+94, Y+34"))
                    
#print(solve(94, 22, 8400, 34, 67, 5400))
