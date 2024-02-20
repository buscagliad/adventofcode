# Python 3 code to demonstrate the 
# working of MD5 (byte - byte)
 
import hashlib

def genkey(pad, n):
    hash_str = pad + str(n)
    result = hashlib.md5(hash_str.encode())
    key = result.hexdigest()
    return key
#
# rehash a key 'n' times
#
def multkey(key, n):
    for i in range(n):
        result = hashlib.md5(key.encode())
        key = result.hexdigest()
    return key
        

def istriple(key):
    index = 1000
    rt = 'q'
    for trip in ["000","111","222","333","444","555","666","777",
        "888","999","aaa","bbb","ccc","ddd","eee","fff"]:
        k = key.find(trip)
        if k < 0: continue
        # if k < len(key) - 3 and key[k+3] == key[k]: continue
        if k < index:
            index = k
            rt = trip[0]
    return rt

def isquint(key, hexdig):
    quint = hexdig + hexdig  + hexdig + hexdig + hexdig
    if quint in key: return True
    return False

allkeys = []
DEBUG = False

#
# generate n keys and put them in allkeys
def genkeys(pad, n, part2 = False):
    global allkeys
    allkeys.clear()
    for k in range(n):
        key = genkey(pad, k)
        if (part2): key = multkey(key, 2016)
        allkeys.append(key)

pad = "cuanljph"    # 23769, 20606 - solution checks
# pad = "qzyelonm"    # 15168, 20864 - solution checks
# pad = "abc"       # 22728, 22551 - solution checks
NUMGENKEYS = 35000
for part2 in [False, True]:
    done = False
    n = 0
    keynum = 0
    next1000 = 0
    key=""
    genkeys(pad, NUMGENKEYS, part2)
    while keynum < 64:
        key = allkeys[n]
        d = istriple(key)
        if d == 'q': 
            n += 1
            continue
        #
        # we are here because we found a triple!, now look for a quint
        # in the next 1000 keys
        #       
        for h in range(1, 1001):
            next1000 = n + h
            if next1000 >= NUMGENKEYS : print("ERROR, next 1000: ", next1000)
            quintkey = allkeys[next1000]
            if isquint(quintkey, d):
                keynum += 1
                if (DEBUG): print("Found key:", keynum, " GEN: ", n, " KEY: ", key, 
                    " N1000: ", h, "\n                          QUINT: ", quintkey, " at ", next1000)
                break
        n += 1
    # DEBUG=True
    if part2 == False:
        print("Part 1:  n = ", n-1, "  64th key: ", key)
    else:
        print("Part 2:  n = ", n-1, "  64th key: ", key)
        # 20141 & 20142 is too low
    #print("KEY 0", allkeys[0])
