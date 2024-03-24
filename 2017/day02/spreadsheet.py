'''
--- Day 2: Corruption Checksum ---

As you walk through the door, a glowing humanoid shape yells in your direction. "You there! Your state appears to be idle. Come help us repair the corruption in this spreadsheet - if we take another millisecond, we'll have to display an hourglass cursor!"

The spreadsheet consists of rows of apparently-random numbers. To make sure the recovery process is on the right track, they need you to calculate the spreadsheet's checksum. For each row, determine the difference between the largest value and the smallest value; the checksum is the sum of all of these differences.

For example, given the following spreadsheet:

5 1 9 5
7 5 3
2 4 6 8

    The first row's largest and smallest values are 9 and 1, and their difference is 8.
    The second row's largest and smallest values are 7 and 3, and their difference is 4.
    The third row's difference is 6.

In this example, the spreadsheet's checksum would be 8 + 4 + 6 = 18.

What is the checksum for the spreadsheet in your puzzle input?

'''

def part1(line):
    w = line.strip().split()
    minw = int(w[0])
    maxw = minw
    for ss in w:
        s = int(ss)
        minw = min(s, minw)
        maxw = max(s, maxw)
    return maxw - minw

def part2(line):
    w = line.strip().split()
    s = [int(num) for num in w]
    s.sort()
    for i in range(len(s)-1):
        for j in range(i+1,len(s)):
            if (s[j] // s[i]) * s[i] == s[j]:
                #print(i, s[i], j, s[j])
                return s[j] // s[i]


psum = 0
p2sum = 0
for line in open('data.txt'):
    psum += part1(line)
    p2sum += part2(line)
    
print("Part1 - sum is: ", psum)
print("Part2 - sum is: ", p2sum)
