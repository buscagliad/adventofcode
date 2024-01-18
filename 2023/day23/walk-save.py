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

class Node:
  def __init__(self, start, stop, steps):
    self.left = None
    self.right = None
    self.start = start
    self.stop = stop
    self.steps = steps
  def PrintTree(self):
    if self.left:
      self.left.PrintTree()
    print( self.data),
    if self.right:
      self.right.PrintTree()
  def insert(self, start, stop, steps):
    # Compare the new value with the parent node
    if self.steps:
      if steps < self.steps:
        if self.left is None:
          self.left = Node(start, stop, steps)
        else:
          self.left.insert(start, stop, steps)
      elif data > self.data:
        if self.right is None:
          self.right = Node(start, stop, steps)
        else:
          self.right.insert(start, stop, steps)
      else:
        self.data = data

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

def nextStepsOld(c, d):
  steps = []
  for nd in [RIGHT, DOWN, LEFT, UP]:
    if d == (nd + 2) % 4: continue  # cannot go backwards
    i = c[0] + DIRlist[nd][0]
    j = c[1] + DIRlist[nd][1]
    if i < 0 or i >= gridRow: continue
    if j < 0 or j >= gridCol: continue
    if grid[i][j] >= 0: steps.append([(i,j), nd])
  return steps

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
    if not grid[i][j] == NOOP: 
      endpath = True
      break
    else:
      steps.append([(i,j), nd])
      break
  return endpath, steps

seen = set()
def getTreeOld(start, d):
  global seen
  # if the starting block is not consistent with the direction to travel
  # return
  #dd = getVal(grid, start, d)
  #print("getTree: ", start[0],start[1],"  v: ",grid[start[0], start[1]], "  dd: ", dd)
  #if not d == dd :
  #  return


  if (start,d) in seen: return
  steps = 0
  curStep = start
  lastStep = curStep
  done = False
  lastDir = d
  
  while not done:
    s = nextSteps(curStep, d)
    if len(s) == 1:
      lastStep = curStep
      steps += 1
      d = s[0][1]
      curStep = s[0][0]
      lastDir = d
    else:
      #
      # base on 'lastDir' direction, we'll only
      # consider some of the returned nodes:
      #   last step       new node
      #   RIGHT           RIGHT, DOWN, UP
      #   LEFT            LEFT, DOWN, UP
      #   UP              UP, LEFT, RIGHT
      #   DOWN            DOWN, LEFT, RIGHT
      #
      done = True
      seen.add((start, d))
      print("Start: ", start, "  end: ", curStep, " dist: ", steps, "  lastDir: ", lastDir, "  lastStep: ", lastStep)
      for a, b in s:
        dd = grid[a]
        print("a: ", a, "  b: ", b, " dd: ", dd)
        if ( (lastDir == RIGHT) and dd in [RIGHT, DOWN, UP]  or
             (lastDir == LEFT)  and dd in [ LEFT, DOWN, UP]  or
             (lastDir == UP)    and dd in [ UP, LEFT, RIGHT]  or
             (lastDir == DOWN)  and dd in [ DOWN, LEFT, RIGHT]) :
          getTree(a, b)

seen = set()
paths = []
def getTree(start, d):
  global seen

  starters = [[start, d]]

  #if (start,d) in seen: return
  while starters:
    start, d = starters.pop()
    print("Start: ", start, "  d: ", d, DIRname[d])
    steps = 0
    curStep = start
    lastStep = curStep
    done = False
    lastDir = d
    
    while not done:
      endpath, s = nextSteps(curStep, d)
      print("nextSteps: ", endpath, s)
      if endpath:
        paths.append([start, s[0][0], s[0][1]])
        print("Start: ", s)
        a, b = nextSteps(curStep, d)
        print("Next: ", b)
        done = True
      # else:
        # if len(s) == 1:
          # lastStep = curStep
          # steps += 1
          # d = s[0][1]
          # curStep = s[0][0]
          # lastDir = d
        # else:
          # #
          # # base on 'lastDir' direction, we'll only
          # # consider some of the returned nodes:
          # #   last step       new node
          # #   RIGHT           RIGHT, DOWN, UP
          # #   LEFT            LEFT, DOWN, UP
          # #   UP              UP, LEFT, RIGHT
          # #   DOWN            DOWN, LEFT, RIGHT
          # #
          # done = True
          # for a, b in s:
            # print("a: ", a, "  b: ", b, " dd: ", dd)
          # #seen.add((start, d))
          # for a, b in s:
            # dd = grid[a]
            # starters.append([a, b])
            # # if ( (lastDir == RIGHT) and dd in [RIGHT, DOWN, UP]  or
                 # # (lastDir == LEFT)  and dd in [ LEFT, DOWN, UP]  or
                 # # (lastDir == UP)    and dd in [ UP, LEFT, RIGHT]  or
                 # # (lastDir == DOWN)  and dd in [ DOWN, LEFT, RIGHT]) :

for line in open('test.txt', 'r'):
  process(line)

getTree((0,1), DOWN)
print(paths)
def printgrid():
  for i in range(gridRow):
    for j in range(gridCol):
      print("%3d " % grid[i][j], end="")
    print()
  print()

	
