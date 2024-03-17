'''
--- Day 20: Firewall Rules ---

You'd like to set up a small hidden computer here so you can use it to get back into the network later. However, the corporate firewall only allows communication with certain external IP addresses.

You've retrieved the list of blocked IPs from the firewall, but the list seems to be messy and poorly maintained, and it's not clear which IPs are allowed. Also, rather than being written in dot-decimal notation, they are written as plain 32-bit integers, which can have any value from 0 through 4294967295, inclusive.

For example, suppose only the values 0 through 9 were valid, and that you retrieved the following blacklist:

5-8
0-2
4-7

The blacklist specifies ranges of IPs (inclusive of both the start and end value) that are not allowed. Then, the only IPs that this firewall allows are 3 and 9, since those are the only numbers not in any range.

Given the list of blocked IPs you retrieved from the firewall (your puzzle input), what is the lowest-valued IP that is not blocked?

Your puzzle answer was 17348574.
--- Part Two ---

How many IPs are allowed by the blacklist?

Your puzzle answer was 104.

Both parts of this puzzle are complete! They provide two gold stars: **
'''
import segment as seg

ips = seg.Segment(0, 4294967295)

ranges=[]
for l in open('data.txt', 'r'):
    w = l.strip().split('-')
    a = int(w[0])
    b = int(w[1])
    ranges.append((a,b))
    ips.remove(a,b)

done = False
lowip = 0
while not done:
    done = True
    for (l, r) in ranges:
        if l <= lowip and lowip <= r:
            lowip = r + 1
            done = False
            break
            

print("Part 1: the lowest acceptable IP is: ", ips.min())
print("Part 2: the total number of good IPs is: ", ips.length())
