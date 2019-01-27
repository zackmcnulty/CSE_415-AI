# IDEA: store the BLOCKS of the rubix cube as my state. Individually, each
# block keeps track of the colors of each face (when viewed from a specific
# orientation). Then, simply just move the blocks to different positions in the cube.





'''zmcnulty_Rubik2Cube.py
'''
#<METADATA>
QUIET_VERSION = '0.2'
PROBLEM_NAME = 'Rubik Cube'
PROBLEM_VERSION = '0.2'
PROBLEM_AUTHORS = ['Z. McNulty']
PROBLEM_CREATION_DATE = '26-JAN-2018'
PROBLEM_DESC=\
'''This formulation of the Rubik 2-Cube uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET2 tools interface.
'''
#</METADATA>

#<COMMON_DATA>
abbr_converter = {'F':'Front', 'B':'Back', 'U':'Up', 'D':'Down', 'L':'Left', 'R':'Right', 'cw': 'clockwise', 'ccw': 'counter-clockwise'}


#</COMMON_DATA>

#<COMMON_CODE>
import random
import time


# each block, if we observe its orientation correctly,
# will have a top face, a front face, and a left face
# that face the exterior of the cube
class Block:

    # NOTE: For a given block, the top face is the face that is located on either to
    # up or down side of the entire cube. This reference frame is important, and 
    # maintaining it is the reason rotate_left and rotate_right are required below.
    def __init__(self,front, left, top):
        self.front = front
        self.top = top
        self.left = left

    def __eq__(self, other):
        return self.front == other.front and self.top == other.top and self.left == other.top

    def copy(self):
        return Block(self.front, self.left, self.top)

    def rotate_left(self):
        temp = self.front
        self.front = self.left
        self.left = self.top
        self.top = temp

    def rotate_right(self):
        temp = self.front
        self.front = self.top
        self.top = self.left
        self.left = temp

# ===========================================================

class State:
    
  def __init__(self, d=None):
      self.d = []
      if d != None:
          for colors in zip(d[::3], d[1::3], d[2::3]):
              self.d += [Block(colors[0], colors[1], colors[2])]
        
  def __eq__(self,s2):
    for i, block in enumerate(self.d):
        if block != s2.d[i]: return False
    else:
        return True
        
  def __str__(self):

    result = 'Up/Front/Down Right Back Left\n'
    # add the string representation of top face
    result += str(self.d[6].top) + ' ' +  str(self.d[7].top) + '\n' + str(self.d[2].top) + ' ' + str(self.d[3].top) + '\n'
    result += '---\n'
    # add string representation of the Front,Right, Back, and Left Faces top row only
    result += ' '.join([str(self.d[2].front), str(self.d[3].left), '|',str(self.d[3].front), str(self.d[7].left),'|', str(self.d[7].front), str(self.d[6].left), '|',  str(self.d[6].front), str(self.d[2].left)]) + '\n'
    # add string representation of the Front,Right, Back, and Left Faces bottom row only
    result += ' '.join([str(self.d[1].left), str(self.d[0].front),'|', str(self.d[0].left), str(self.d[4].front), '|', str(self.d[4].left), str(self.d[5].front), '|', str(self.d[5].left), str(self.d[1].front)]) + '\n'
    result += '---\n'
    # add string representation of bottom face
    result += ' '.join([str(self.d[1].top), str(self.d[0].top)]) + '\n' + ' '.join([str(self.d[5].top), str(self.d[4].top)]) + '\n'
    return result



  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State()
    news.d = [block.copy() for block in self.d]
    return news

  # we can always rotate the cube in any direction we want;
  # there are no restrictions
  def can_move(self,dir):
      return True

  # Copies self, and performs the given move on the copy, returning that copy
  # NOTE: When rotating blocks throughout the cube, moving their location changes
  # which face is being interpreted as top/front/left. As a result, we have to rotate
  # these during the move. We have found that if a block rotates across the top/bottom,
  # we have to rotate its faces left, and if it moves up/down to its new place,
  # we have to rotate its faces right. This rotation is not required with the Top/bottom
  # faces as these faces are where the reference frame is set
  def move(self,dir):
    news = self.copy()
    if dir == 'F':
        # move front face 90 clockwise
        # Blocks 0 --> 1, 1-->2, 2-->3, 3-->0
        temp = news.d[0]
        news.d[0] = news.d[3]
        news.d[3] = news.d[2]
        news.d[2] = news.d[1]
        news.d[1] = temp

        # rotate cubes after moving them
        # right diagonal rotates left, left diagonal rotates right
        news.d[2].rotate_left()
        news.d[3].rotate_right()
        news.d[1].rotate_right()
        news.d[0].rotate_left()

    elif dir == 'U':
        # move top face 90 clockwise
        # Blocks 3 --> 2, 2-->6, 6-->7, 7-->3
        temp = news.d[3]
        news.d[3] = news.d[7]
        news.d[7] = news.d[6]
        news.d[6] = news.d[2]
        news.d[2] = temp

    elif dir == 'R':
        # move left face 90 clockwise
        # Blocks 0 --> 3, 3--7, 7-->4, 4-->0

        temp = news.d[0]
        news.d[0] = news.d[4]
        news.d[4] = news.d[7]
        news.d[7] = news.d[3]
        news.d[3] = temp

        # rotate entries to counteract change of perspective
        # blocks rotating across top/bottom rotate left, those
        # rotating up/down rotate right
        news.d[3].rotate_left()
        news.d[4].rotate_left()
        news.d[0].rotate_right()
        news.d[7].rotate_right()

    elif dir == 'L':
        # move right face 90 clockwise
        # Blocks 2-->1, 1-->5, 5-->6, 6-->2
        temp = news.d[2]
        news.d[2] = news.d[6]
        news.d[6] = news.d[5]
        news.d[5] = news.d[1]
        news.d[1] = temp

        # rotate diagonal entries left
        news.d[2].rotate_right()
        news.d[5].rotate_right()
        news.d[6].rotate_left()
        news.d[1].rotate_left()

    elif dir == 'B':
        # move back face 90 clockwise
        # Blocks 7-->6, 6-->5, 5-->4, 4-->7
        temp = news.d[7]
        news.d[7] = news.d[4]
        news.d[4] = news.d[5]
        news.d[5] = news.d[6]
        news.d[6] = temp

        # rotate
        news.d[4].rotate_right()
        news.d[6].rotate_right()
        news.d[7].rotate_left()
        news.d[5].rotate_left()

    elif dir == 'D': 
        # move bottom face 90 clockwise
        # Blocks 1-->0, 0-->4, 4-->5, 5-->1
        temp = news.d[1]
        news.d[1] = news.d[5]
        news.d[5] = news.d[4]
        news.d[4] = news.d[0]
        news.d[0] = temp

    return news # return new state
    
  def edge_distance(self, s2):
    # ONLY VALID IF S2 is REACHABLE FROM CURRENT STATE
    return 1.0

# =============================================================
  
def goal_test(s):
    solved_state_list = [0,2,4,    3,0,4,   0,3,1,   2,0,1,   2,5,4,   5,3,4,   3,5,1,   5,2,1]
    solved_state = State(solved_state_list)
    
    return str(solved_state) == str(s)

def goal_message(s):
    return 'You are a cubing monster!'

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)
#</COMMON_CODE>

#<INITIAL_STATE>

# n is the number of turns you want to scramble the cube with
# S is a SOLVED CUBE that should be scrambled
# returns the scarmbled state
def mix_cube(n, S):
    for _ in range(n):
        direction = random.choice(['F','B', 'U', 'D', 'L', 'R'])
        S = S.move(direction)

    return S

    ## block front, left, top

    # DONT allow initial state to be specified; too easy to make it
    # unsolvable
try:
  import sys
  shuffle_count = sys.argv[2]
  print(' Number of shuffles to mix cube as given on the command line: '+shuffle_count)
  n = int(shuffle_count)
except:

  n = 100  
  print('Using default number of shuffles: 100')
  print(' (To use a specific number of shuffles , enter it on the command line, e.g.,')
  print('python3 UCS.py zmcnulty_Rubik2Cube 25')


random.seed(1234) # for reproducibility
solved_state_list = [0,2,4,    3,0,4,   0,3,1,   2,0,1,   2,5,4,   5,3,4,   3,5,1,   5,2,1]
solved_state = State(solved_state_list)
#print(solved_state)

# mix up the cube with 100 random moves
init_state = mix_cube(n, solved_state)

CREATE_INITIAL_STATE = lambda: init_state
#</INITIAL_STATE>

#<OPERATORS>

# rotate the front, back, up side, downside, left, and right 90 degrees
# clockwise 

possible_moves = ['F','B', 'U', 'D', 'L', 'R']
OPERATORS = [Operator('Move the ' + str(abbr_converter[move]) + ' face in the clockwise direction.',
                      lambda s,face=move: s.can_move(face),
                      # The default value construct is needed
                      # here to capture the value of dir
                      # in each iteration of the list comp. iteration.
                      lambda s,face=move: s.move(face))
             for move in possible_moves]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

