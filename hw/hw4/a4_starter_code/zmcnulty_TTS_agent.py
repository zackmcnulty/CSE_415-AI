'''
Zachary McNulty (zmcnulty, 1636402)

zmcnulty_TTS_agent.py
'''

from TTS_State import TTS_State


# DEFINE GLOBAL VARIABLES
RIGHT = (1,0)
UP = (0,1)
UP_RIGHT = (1,1)
DOWN_RIGHT = (1,-1)

DIRECTIONS = [RIGHT, UP, UP_RIGHT, DOWN_RIGHT]

USE_CUSTOM_STATIC_EVAL_FUNCTION = False

class MY_TTS_State(TTS_State):
  def static_eval(self):
    if USE_CUSTOM_STATIC_EVAL_FUNCTION:
      return self.custom_static_eval()
    else:
      return self.basic_static_eval()

  def basic_static_eval(self):
    #self.board gives the current board
    # K is a global variable
    num_rows = len(self.board)
    num_cols = len(self.board[0])
    CW = 0 # count of C(white, 2)
    CB = 0 # count of C(black, 2)
    
    for row in range(num_rows):
        for col in range(num_cols):
            for dir in DIRECTIONS:
               squares = [self.board[(row + i*dir[0]) % num_rows][(col + i*dir[1]) % num_cols] for i in range(K)]
               if squares.count('W') == 2:
                    CW += 1
               if squares.count('B') == 2:
                    CB += 1

    return CW - CB


  def custom_static_eval(self):
    raise ValueError("not yet implemented")

def take_turn(current_state, last_utterance, time_limit):

    # Compute the new state for a move.
    # Start by copying the current state.
    new_state = MY_TTS_State(current_state.board)
    # Fix up whose turn it will be.
    who = current_state.whose_turn
    new_who = 'B'  

    if who=='B': new_who = 'W'  
    new_state.whose_turn = new_who
    
    # Place a new tile
    location = _find_next_vacancy(new_state.board)
    if location==False: return [[False, current_state], "I don't have any moves!"]
    new_state.board[location[0]][location[1]] = who

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    move = location

    # Make up a new remark
    new_utterance = "I'll think harder in some future game. Here's my move"

    return [[move, new_state], new_utterance]

def _find_next_vacancy(b):
    for i in range(len(b)):
      for j in range(len(b[0])):
        if b[i][j]==' ': return (i,j)
    return False

def moniker():
    return "Squarepants" # Return your agent's short nickname here.

def who_am_i():
    return '''
        My name is Spongebob Squarepants. I just wanted to thank zmcnulty
        for bringing me here today. Let's show the NFL how its done.
        This one is for Stephen Hillenburg.

            The winner takes all
            It's the thrill of one more kill
            The last one to fall
            Will never sacrifice their will
            Don't ever look back
            On the wind closing in
            The only attack
            Were their wings on the wind
            Oh the daydream begins
            And it's sweet, sweet, sweet victory, yeah!
            And it's ours for the taking
            It's ours for the fight
            In the sweet, sweet, sweet victory, yeah!
            And the world is last to fall


    '''
# ONLY CALLED ON AT THE BEGINNING OF THE GAME!
def get_ready(initial_state, k, who_i_play, player2Nickname):
    # do any prep, like eval pre-calculation, here.

    # find where the blocked squares are?
    return "OK"

# The following is a skeleton for the function called parameterized_minimax,
# which should be a top-level function in each agent file.
# A tester or an autograder may do something like
# import ABC_TTS_agent as player, call get_ready(),
# and then it will be able to call tryout using something like this:
# results = player.parameterized_minimax(**kwargs)

def parameterized_minimax(
       current_state=None,
       use_iterative_deepening_and_time = False,
       max_ply=2,
       use_default_move_ordering = False,
       alpha_beta=False, 
       time_limit=1.0,
       use_custom_static_eval_function=False):

  # All students, add code to replace these default
  # values with correct values from your agent (either here or below).
  current_state_static_val = -1000.0
  n_states_expanded = 0
  n_static_evals_performed = 0
  max_depth_reached = 0
  n_ab_cutoffs = 0

  # STUDENTS: You may create the rest of the body of this function here.

  # Prepare to return the results, don't change the order of the results
  results = []
  results.append(current_state_static_val)
  results.append(n_states_expanded)
  results.append(n_static_evals_performed)
  results.append(max_depth_reached)
  results.append(n_ab_cutoffs)
  # Actually return the list of all results...
  return(results)

