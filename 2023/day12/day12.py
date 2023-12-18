import numpy as np
from itertools import combinations
import functools
from typing import List, Tuple

def hashinarow(l):
	count = 0
	for a in l:
		if a == '#' : count += 1
		else: return count
	return count


lakes = [".", "#."]
for i in range(2,25):
	lakes.append(''.join(["#", lakes[i-1]]))


###
#
# procline, will do the following:
#     find w[i], i = 0..n, such that 
#       sum(w[:n]) < len(pline) + n
#
# procline2 will keep a stack of sub-strings s all starting with ? or #
#			and going for w[wi] characters - then the following cases are dealt with
#			the next char is:
#				# - if first char is ? push onto stack s[1:]
#						otherwise do not push onto stack
#				? - required to be a dot, increase counter
#						push string after ? starting with a ? or #  onto stack
#				. - increase counter, push string after . starting with a ? or #  onto stack
#

@functools.cache
def counter(lstr : str, w: Tuple[int], wc : int) -> int:
	#
	# check to see if we have completed this list:
	if len(lstr) == 0:
		if len(w) == 0:
			#print("FOUND")
			return 1
		return 0

	# # check to see if we are at the end of our w number
	# if (len(w) == 0) :
		# ## check if we have
		# numslashes = lstr.count('#')
		# if numslashes > 0 : return 0
		# else:
			# return counter(lstr[1:], w[1:], 0)
	#
	# deal with current char
	#
	if lstr[0] == '.': # ignore
		return counter(lstr[1:], w, wc)
		
	if lstr[0] == '#':
		if len(w) == 0: # no more lakes to find
			return 0
		
		if (len(lstr) < w[0]): # could do: sum(w) + len(w) - 1 ??
			return 0	# not enough room to finish
			
		# do a look ahead to see that there are NO dots
		for i in range(w[0]):
			if lstr[i] == '.' : return 0
		
		#
		# we have found w[0] hashes, this will fail above
		# 
		if len(lstr) == w[0]:
			#print("lstr: ", lstr, "  w: ", w, "  wc: ", wc)
			return counter("", w[1:], wc)
			
		if lstr[w[0]] == "#":
			#print("lstr: ", lstr, "  w: ", w, "  wc: ", wc)
			return 0
		
		# if we go here, lstr has w[0] hashes
		return counter(lstr[w[0]+1:], w[1:], 0)	# increment pound count and put on stand
		
		
	# if we get here: we have a '?'
	return (counter(''.join(['#', lstr[1:]]), w, 0)	# treat '?' as a '#'				
		       + counter(''.join(['.', lstr[1:]]), w, 0))	# treat '?' as a '.'				



###
#
#   procline2 uses the list structure:
##		line is the string of '.', '#', '?'
#		s = [ix, wi, wc]
#		ix is the current index of line that is being processed
#		wi is the index into the list of lakes
#       wc is the count of #'s (when wc == w[wi] you can continue!!
#
def procline2(pline, w, debug = False):
	st = []
	wi = 0
	numwi = len(w)
	st.append([0, 0, 0])
	if debug: print(pline, "  w: ", w)
	count = 0
	while st:
		ix, wi, wc = st.pop()
		if debug: print("ix: ", ix, "  wi: ", wi, "  wc: ", wc)
		
		if ix < len(pline):
			ch = pline[ix]
		else:
			ch = 'X'	# fake end of line

		if ch == '.' and wc == 0:
			st.append([ix+1, wi, 0])
			continue
		#
		# did we find a solution?
		#
		if wi == len(w):
			if pline[ix:].find('#') >= 0: 
				continue	# fail, we've found all the lakes but there are still more #'s
				if debug: print("FAIL, found all lakes but there are ", pline[ix:].count('#'), " #'s left")
			else:
				count += 1	# success
				if debug: print("SUCCESS! count: ", count)
				continue
			
		if wc == w[wi]:
			if ch == '#':
				if debug: print("Found string of #'s for w[", wi, "] = ", w[wi], " but next char is a #")
			elif ch == '?' or ch == '.': # we'll use it as a dot
				if debug: print("Found lake for w[", wi, "] = ", w[wi])
				st.append([ix+1, wi+1, 0])
			continue	# failed to find the lake
		
		#
		# deal with current char
		#
		if ch == '#':
			st.append([ix+1, wi, wc+1])	# increment pound count and put on stand
		elif ch == '.':
			continue					# ran into a dead end
		elif ch == '?':
			st.append([ix+1, wi, wc+1])	# treat '?' as a '#'				
			if wc == 0 : st.append([ix+1, wi, 0])	# treat '?' as a '.'				
			
	return count



def processPart1(line):
	line = line.strip()
	w = line.split(' ')
	fields = w[0]
	x = w[1].split(',')
	#m = Tuple[int
	#m = [int(i) for i in x]
	m = tuple(int(i) for i in x)
	#for i in x: m.append(int(i))
	#print(line, "  arangements: ",  procline2(fields, m, False))
	c = counter(fields, tuple(m), 0)
	#print(fields, m, "  arrangements: ", c) 
	return c

def processPart2(line):
	line = line.strip()
	w = line.split(' ')
	fields = w[0]
	x = w[1].split(',')

	fields = w[0]
	x = w[1].split(',')
	m = 5 * tuple(int(i) for i in x)
	for i in range(4):
		fields = ''.join([fields,'?',w[0]])
	c = counter(fields, tuple(m), 0)
	#print(fields, m, "  arrangements: ", c) 
	return c

count = 0
for line in open("data.txt"):
	count += processPart1(line)
print ("Part 1: Number of possible valid arrangements: ", count)


count = 0
for line in open("data.txt"):
	count += processPart2(line)
	
print ("Part 2:: Number of possible 5-fold arrangements: ", count)
