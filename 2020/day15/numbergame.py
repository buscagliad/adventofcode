import copy
from collections import defaultdict


def ngame(cmnt, nlist, totalplays) :
	starting = copy.deepcopy(nlist)	# for record keeping
	lastseen = defaultdict(tuple)	# val will be the dictionary lookup
										# [0] is the last time val was seen
										# [1] is the previous to last time val was seen
	
	for i, val in enumerate(nlist) :
		lastseen[val] = (i, None)
	if 0 not in lastseen : lastseen[0] = (None, None)
	speak = nlist[-1]				# last element in nlist is the first 'spoken' number
	plays = len(nlist)
	#print(lastseen)
	while plays < totalplays:
		if lastseen[speak][1] is not None :	# second or greater time we have seen this number
			next_speak = 	lastseen[speak][0] - lastseen[speak][1]
			if not lastseen[next_speak] :	# first time we've seen this number
				lastseen[next_speak] = (plays, None)
			else :
				lastseen[next_speak] = (plays, lastseen[next_speak][0])
			speak = next_speak
		else : # first time we have seen this number
			speak = 0
			lastseen[speak] = (plays, lastseen[speak][0])
		plays += 1
		#if plays %1000000 == 0 : print ("Play ", plays, " spoken: ", speak, flush=True)

	print(cmnt, " from the starting numbers ",  starting, ", the ",
		totalplays, " number spoken is ", speak, flush=True)


#ngame([1, 3, 2], 2020)

#ngame([0, 3, 6], 2020)

#ngame([2, 1, 3], 2020)

#ngame([1, 2, 3], 2020)

#ngame([2, 3, 1], 2020)

#ngame([3, 2, 1], 2020)

#ngame([3, 1, 2], 2020)

ngame("Part 1:", [1,12,0,20,8,16], 2020)

ngame("Part 2:", [1,12,0,20,8,16], 30000000)


