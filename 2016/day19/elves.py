'''
--- Day 19: An Elephant Named Joseph ---

The Elves contact you over a highly secure emergency channel. Back at the North Pole, the Elves are busy misunderstanding White Elephant parties.

Each Elf brings a present. They all sit in a circle, numbered starting with position 1. Then, starting with the first Elf, they take turns stealing all the presents from the Elf to their left. An Elf with no presents is removed from the circle and does not take turns.

For example, with five Elves (numbered 1 to 5):

  1
5   2
 4 3

    Elf 1 takes Elf 2's present.
    Elf 2 has no presents and is skipped.
    Elf 3 takes Elf 4's present.
    Elf 4 has no presents and is also skipped.
    Elf 5 takes Elf 1's two presents.
    Neither Elf 1 nor Elf 2 have any presents, so both are skipped.
    Elf 3 takes Elf 5's three presents.

So, with five Elves, the Elf that sits starting in position 3 gets all the presents.

With the number of Elves given in your puzzle input, which Elf gets all the presents?

Your puzzle answer was 1816277.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

Realizing the folly of their present-exchange rules, the Elves agree to instead steal presents from the Elf directly across the circle. If two Elves are across the circle, the one on the left (from the perspective of the stealer) is stolen from. The other rules remain unchanged: Elves with no presents are removed from the circle entirely, and the other elves move in slightly to keep the circle evenly spaced.

For example, with five Elves (again numbered 1 to 5):

    The Elves sit in a circle; Elf 1 goes first:

      1
    5   2
     4 3

    Elves 3 and 4 are across the circle; Elf 3's present is stolen, being the one to the left. Elf 3 leaves the circle, and the rest of the Elves move in:

      1           1
    5   2  -->  5   2
     4 -          4

    Elf 2 steals from the Elf directly across the circle, Elf 5:

      1         1 
    -   2  -->     2
      4         4 

    Next is Elf 4 who, choosing between Elves 1 and 2, steals from Elf 1:

     -          2  
        2  -->
     4          4

    Finally, Elf 2 steals from Elf 4:

     2
        -->  2  
     -

So, with five Elves, the Elf that sits starting in position 2 gets all the presents.

With the number of Elves given in your puzzle input, which Elf now gets all the presents?

Your puzzle answer was 1816277.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

Realizing the folly of their present-exchange rules, the Elves agree to instead steal presents from the Elf directly across the circle. If two Elves are across the circle, the one on the left (from the perspective of the stealer) is stolen from. The other rules remain unchanged: Elves with no presents are removed from the circle entirely, and the other elves move in slightly to keep the circle evenly spaced.

For example, with five Elves (again numbered 1 to 5):

    The Elves sit in a circle; Elf 1 goes first:

      1
    5   2
     4 3

    Elves 3 and 4 are across the circle; Elf 3's present is stolen, being the one to the left. Elf 3 leaves the circle, and the rest of the Elves move in:

      1           1
    5   2  -->  5   2
     4 -          4

    Elf 2 steals from the Elf directly across the circle, Elf 5:

      1         1 
    -   2  -->     2
      4         4 

    Next is Elf 4 who, choosing between Elves 1 and 2, steals from Elf 1:

     -          2  
        2  -->
     4          4

    Finally, Elf 2 steals from Elf 4:

     2
        -->  2  
     -

So, with five Elves, the Elf that sits starting in position 2 gets all the presents.

With the number of Elves given in your puzzle input, which Elf now gets all the presents?


Your puzzle answer was 1410967.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

import random
import circlist as cl
import numpy as np
########  PART 1



N=3005290
# Example Usage:
part1 = cl.CircularLinkedList()
# Adding elements
for n in range(1, N+1):
    part1.add_element(n)


el = part1.current
while  part1.count > 1:
    el = part1.remove_next(el)
    #print(part1.count)

print(f"Part 1: with {N} elves the one who gets all of the presents is: ", part1.current.data)


#
# NOTE: the code below was used to discover the pattern for E(N)
#
'''
part2 = cl.CircularLinkedList()
# Adding elements
for N in range(2, 2200):
    for n in range(1, N+1):
        part2.add_element(n)


    el = part2.head
    while  part2.count > 1:
        el = part2.remove_across(el)
    print(N, part2.head.data)
    part2.clear()
'''
######### PART 2
#
#      E(n) is the elf number that will receive all the presents
#
# Note that:  
#       E(2) = 1
#       E(4) = 1
#       E(10) = 1
#       E(28) = 1
#       E(244) = 1
#       E(730) = 1
#
#   Ai : E(Ai) = 1   ->  {2, 4, 10, 28, 244, 730, ...} = A
#
#   A[i+1] - A[i] = 3 * (A[i] - A[i-1]), A[0] = 2, A[1] = 4
#
#   A[i+1] = 4 * A[i] - 3 * A[i-1]
#
#
A = np.zeros(22, dtype = int)
A[0] = 2
A[1] = 4
for n in range(2, 22):
    A[n] = 4 * A[n-1] - 3 * A[n-2]

#
# for a given number of elves, N, find i, such that:
#     A[i] <= N < A[i+1]
#
# compute:  d = N - A[i]   and H = (A[i+1] - A[i]) / 2
#
#     if d < H/2 then
#          E[N] = d + 1
#     else
#          E[N] = H + 2 * (d - H)
# 

def E(N):
    k = 0
    for i in range(1, 21):
        if A[i] <= N < A[i+1]:
            k = i
            break
    d = N - A[i]
    H = (A[i+1] - A[i]) // 2
    if d < H :
         retE = d + 1
    else:
         retE = H + 2 * (d - H + 1)
    return retE



print(f"Part 2: with {N} elves the one who gets all of the presents is: ", E(N))


