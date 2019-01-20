# Issue is that something is being assigned a depth before the min path to it
# is found, and then that is erroneously used to find depths of those after it

# use recursive backtracking?


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

print("\nWelcome to IDDFS")
# count keeps track of the number of nodes visited

def runIDDFS():
  initial_state = Problem.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(initial_state)

  global COUNT, BACKLINKS, MAX_OPEN_LENGTH, MAX_DEPTH, DEPTHS
  solved = False
  COUNT = 0
  MAX_OPEN_LENGTH = 0
  MAX_DEPTH = 0 


  # Backlinks keeps track of the previous node in the shortest path to state S
  # DEPTHS keeps track of the length of the shortest path to state S
  # these BOTH persist throughout each run of the IDDFS algorithm as the max depth
  # is increased.
  BACKLINKS = {}
  DEPTHS = {}
  DEPTHS[initial_state] = 0

  while not solved:
    MAX_DEPTH += 1
    solved = IDDFS(initial_state)
    

  print(str(COUNT)+" states expanded.")
  print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))

def IDDFS(initial_state):
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH, MAX_DEPTH, DEPTHS
  print(DEPTHS)

# STEP 1. Put all the nodes at the previous MAX_DEPTH on OPEN
#         i.e. start next search where the previous one left off
  OPEN = [key for key in DEPTHS if DEPTHS[key] == (MAX_DEPTH - 1)]
  BACKLINKS[initial_state] = None


# STEP 2. If OPEN is empty, output “DONE” and stop. Restart algorithm with higher max depth
  while OPEN != []:
    report(OPEN, COUNT)
    if len(OPEN)>MAX_OPEN_LENGTH: MAX_OPEN_LENGTH = len(OPEN)

# STEP 3. Select the first state on OPEN and call it S.
#         Delete S from OPEN.
#         If S is a goal state, output its description

    S = OPEN.pop(0)

    if Problem.GOAL_TEST(S):
      print(Problem.GOAL_MESSAGE_FUNCTION(S))
      path = backtrace(S)
      print('Length of solution path found: '+str(len(path)-1)+' edges')
      return True

    # count number of nodes expanded
    COUNT += 1


# STEP 4. Generate the list L of successors of S 
#           DONT add S's successors if S is already at the max depth
#           Only add a node to open if it has not be expanded yet (DEPTH not known)
#           or if we found a shorter path to it (old depth < new depth)

    if DEPTHS[S] < MAX_DEPTH:
        L = []
        for op in Problem.OPERATORS:
          if op.precond(S):
            new_state = op.state_transf(S)
            
            # revisit a node if its calculated DEPTH changes because this means
            # we can possibly travel farther down this branch

            if not (new_state in DEPTHS) or DEPTHS[new_state] > DEPTHS[S] + 1:
              L.append(new_state)
              try:
                  DEPTHS[new_state] = min(DEPTHS[new_state], DEPTHS[S] + 1)
              except:
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
  
def report(open, count):
  print("len(OPEN)="+str(len(open)), end='; ')
  print("COUNT = "+str(count))

if __name__=='__main__':
  runIDDFS()


