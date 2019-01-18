# Issue is that something is being assigned a depth before the min path to it
# is found, and then that is erroneously used to find depths of those after it


''' IDDFS.py
by Zachary McNultyJ
Assignment 2, in CSE 415, Winter 2019.
This file contains the implementation for the Iterative Deepening Depth First Search
Algorithm. It can search through problem space for the optimal path between some
initial state and some goal state (defined by the problem).
'''

import sys

# choose your problem
if sys.argv==[''] or len(sys.argv)<2:
#  import EightPuzzle as Problem
  import TowersOfHanoi as Problem
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to ItrDFS")
COUNT = None
BACKLINKS = {}

def runIDDFS():
  initial_state = Problem.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(initial_state)
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH, MAX_DEPTH
  solved = False
  COUNT = 0
  MAX_OPEN_LENGTH = 0
  MAX_DEPTH = -1 
  while not solved:
    MAX_DEPTH += 1
    BACKLINKS = {}
    solved = IDDFS(initial_state)
    

  print(str(COUNT)+" states expanded.")
  print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))

def IDDFS(initial_state):
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH, MAX_DEPTH

# STEP 1. Put the start state on a list OPEN
  OPEN = [initial_state]
  CLOSED = []
  BACKLINKS[initial_state] = None
  DEPTHS = {}
  DEPTHS[initial_state] = 0

# STEP 2. If OPEN is empty, output “DONE” and stop.
  while OPEN != []:
    report(OPEN, CLOSED, COUNT)
    if len(OPEN)>MAX_OPEN_LENGTH: MAX_OPEN_LENGTH = len(OPEN)

# STEP 3. Select the first state on OPEN and call it S.
#         Delete S from OPEN.
#         Put S on CLOSED.
#         If S is a goal state, output its description
    S = OPEN.pop(0)
    if S not in CLOSED:
        CLOSED.append(S)

    if Problem.GOAL_TEST(S):
      print(Problem.GOAL_MESSAGE_FUNCTION(S))
      path = backtrace(S)
      print('Length of solution path found: '+str(len(path)-1)+' edges')
      return True
    COUNT += 1

# STEP 4. Generate the list L of successors of S and delete 
#         from L those states already appearing on CLOSED.
# ONLY ADD SUCCESSORS IF DEPTH OF S < max depth!

    if DEPTHS[S] < MAX_DEPTH:
        L = []
        for op in Problem.OPERATORS:
          if op.precond(S):
            new_state = op.state_transf(S)
            
            # revisit a node if its calculated DEPTH changes because this means
            # we can possibly travel farther down this branch


            if not (new_state in CLOSED) or DEPTHS[new_state] > DEPTHS[S] + 1:
              L.append(new_state)
              DEPTHS[new_state] = DEPTHS[S] + 1
              BACKLINKS[new_state] = S


    # STEP 5. Delete from OPEN any members of OPEN that occur on L.
    #         Insert all members of L at the front of OPEN.
        OPEN = L + [o for o in OPEN if o not in L]
    
    print_state_list("OPEN", OPEN)
    # STEP 6. Go to Step 2.

# max depth reached without finding solution; increase max depth and repeat.
  print("max depth of ", MAX_DEPTH, " reached. Expanding depth and repeating process!")
  return False



def print_state_list(name, lst):
    if len(lst) > 0:
      print(name+" is now: ",end='')
      for s in lst[:-1]:
        print(str(s),end=', ')
      print(str(lst[-1]))
    else:
        print(name, " is now []")

def backtrace(S):
  global BACKLINKS
  path = []
  while S:
    path.append(S)
    S = BACKLINKS[S]
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(s)
  return path    
  
def report(open, closed, count):
  print("len(OPEN)="+str(len(open)), end='; ')
  print("len(CLOSED)="+str(len(closed)), end='; ')
  print("COUNT = "+str(count))

if __name__=='__main__':
  runIDDFS()


