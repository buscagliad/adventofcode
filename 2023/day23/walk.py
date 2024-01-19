import numpy as np

import copy

grid = np.zeros([200,200], dtype = int)
gridCol = 0
gridRow = 0

##
#             RIGHT    DOWN     LEFT    UP       NO-OP    
DIRlist  = [ ( 0, 1), (1, 0), (0, -1), (-1, 0), ( 0, 0)  ]
DIRname = [ "RIGHT", "DOWN", "LEFT", "UP", "NO-OP" ]

START = -1
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3
NOOP = 4

def connected(a, b):
  d = abs(a[0] - b[0] + a[1] - b[1])
  if d == 1: return True
  return False

class Node:
  def __init__(self, start, stop, steps, endNode = False):
    self.connected = []
    self.start = start
    self.stop = stop
    self.steps = steps
    self.nodemin = steps
    self.nodemax = steps
    self.visited = False
    self.dist = 0
    self.endNode = endNode
    
  def search(self):
      if self.endNode: return self.dist + self.steps
      for c in self.connected:
          if not c.visited:
              c.visited = True
              s = self.dist + c.steps
              if s > c.dist: c.dist = s
              return c.search()
       print("SHOULD NEVER GET HERE")
       exit(1)
  def PrintTree(self):
    print(self.start, self.stop, self.steps)
    if not self.connected: return
    for c in self.connected:
      c.PrintTree()

  def insert(self, start, stop, steps, endNode = False):
    print("INSERT:: Comparing ", self.stop, " to ", start)
    if connected(self.stop, start):
        print("APPENDING::  ", start, " to ", self.stop)
        self.connected.append(Node(start, stop, steps, endNode))
        return True
    # Compare the new value with the parent node
    if not self.connected:
      return False
    tv = False
    for c in self.connected:
      tv = tv or c.insert(start, stop, steps, endNode)
    return tv

  def sum(self, s = 0):
    global pathMin
    global pathMax
    s += self.steps
    print("sum-", s)
    if self.connected:
      for c in self.connected:
        s = c.sum(s)
        if s > self.nodemax:
          self.nodemax = s
        elif s < self.nodemin:
          self.nodemin = s
    return s

def process(line):
  global gridRow
  global gridCol
  j = 0
  gridCol = len(line) - 1
  for a in line.strip():
    if a == '#':
      grid[gridRow][j] = -1
    elif a == '>':
      grid[gridRow][j] = RIGHT
    elif a == '<':
      grid[gridRow][j] = LEFT
    elif a == '^':
      grid[gridRow][j] = UP
    elif a == 'v':
      grid[gridRow][j] = DOWN
    elif a == '.':
      grid[gridRow][j] = NOOP
    j += 1
  gridRow += 1


def getVal(g, s, d):
  i = s[0] + DIRlist[d][0]
  j = s[1] + DIRlist[d][1]
  #print("getval: ", i, j,"  v: ",grid[i][j])
  return g[i][j]

def nextSteps(c, d):
  steps = []
  endpath = False
  for nd in [RIGHT, DOWN, LEFT, UP]:
    if d == (nd + 2) % 4: continue  # cannot go backwards
    i = c[0] + DIRlist[nd][0]
    j = c[1] + DIRlist[nd][1]
    if i < 0 or i >= gridRow: continue
    if j < 0 or j >= gridCol: continue
    if grid[i][j] == -1: continue
    if grid[i][j] == NOOP: 
      endpath = False
      steps.append([(i,j), nd])
      break
    else:
      steps.append([(i,j), nd])
      endpath = True
      break
  return endpath, steps

def moveStep(s, d):
    i = s[0] + DIRlist[d][0]
    j = s[1] + DIRlist[d][1]
    if i < 0 or i >= gridRow: return
    if j < 0 or j >= gridCol: return
    return (i,j)

seen = set()
paths = []
def getTree(start, d):
  global seen

  starters = [[start, d]]
  finalStep = (gridRow-1, gridCol-2)
  trueStart = True
  #if (start,d) in seen: return
  while starters:
    start, d = starters.pop()
    npt = (start[0] + DIRlist[d][0], start[1] + DIRlist[d][1])
    if not trueStart and not d == grid[npt]:
      #print("Rejected")
      continue
    #else:
      #print("Accepted")
    #print("Processing From QUQUE::  Start: ", start, "  d: ", d, DIRname[d])
    trueStart = False
    curStep = start
    lastStep = curStep
    curStep = moveStep(curStep, d)
    steps = 1
    done = False
    lastDir = d
    
    while not done:
      endpath, s = nextSteps(curStep, d)
      #print("Next step: ", s)
      if len(s) == 0: break
      steps += 1
      if steps == 1: endpath = False
      curStep = s[0][0]
      d = s[0][1]
      #print("nextSteps: ", endpath, curStep)
      if curStep == finalStep:
        if not ((start, s[0][0])) in seen:
          paths.append([start, s[0][0], steps])
          seen.add((start, s[0][0]))
        done = True
      if endpath:
        if not ((start, s[0][0])) in seen:
          paths.append([start, s[0][0], steps])
          seen.add((start, s[0][0]))
        a, b = nextSteps(curStep, d)
        #print("End of path: ", s, "  a: ", a, "  b: ", b)
        for n in [RIGHT, DOWN, LEFT, UP]:
          if n == (b[0][1] + 2) % 4: continue ## cannot reverse direction
          starters.append([b[0][0], n])
          #print("Pushed on queue Next: ", b[0][0], n, DIRname[n])
        done = True


for line in open('test.txt', 'r'):
  process(line)

getTree((0,1), DOWN)

tr = Node(paths[0][0], paths[0][1], paths[0][2])
used = [0]*len(paths)
used[0] = 1
done = False
for p in paths:
    print(p[0], p[1], p[2])


while not done:
  found = False
  for i, p in enumerate(paths):
    if used[i] == 1: continue
    print("Looking to insert: ", p[0], p[1], p[2])
    last = (p[1] == (gridRow-1,gridCol-2))
    if (last) : print("LAST")
    if tr.insert(p[0], p[1], p[2], last): 
      used[i] = 1
      print("Inserted: ", p[0], p[1], p[2], " total: ", sum(used))
      found = True
      break
  done = (sum(used) == len(paths)) or (not found)

tr.PrintTree()

print(tr.sum())
print(tr.nodemin, tr.nodemax)
print(tr.search())

# for p in paths:
  # print(p)
# def printgrid():
  # for i in range(gridRow):
    # for j in range(gridCol):
      # print("%3d " % grid[i][j], end="")
    # print()
  # print()

    
for i, p in enumerate(paths):
  if used[i] == 1: continue
  print("NOT able to insert: ", p[0], p[1], p[2])
