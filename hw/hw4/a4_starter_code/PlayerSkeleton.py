'''PlayerSkeleton.py
A bare-bones agent that plays Toro-Tile Straight,
but rather poorly.

To create your own agent, make a copy of this file, using
the naming convention YourUWNetID_TTS_agent.py.

If you need to import additional custom modules, use
a similar naming convention... e.g.,
YourUWNetID_TTS_custom_static.py


'''

from TTS_State import TTS_State

USE_CUSTOM_STATIC_EVAL_FUNCTION = False

class MY_TTS_State(TTS_State):
  def static_eval(self):
    if USE_CUSTOM_STATIC_EVAL_FUNCTION:
      return self.custom_static_eval()
    else:
      return self.basic_static_eval()

  def basic_static_eval(self):
    raise Exception("basic_static_eval not yet implemented.")

  def custom_static_eval(self):
    raise Exception("custom_static_eval not yet implemented.")


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
    return "Buddy" # Return your agent's short nickname here.

def who_am_i():
    return """My name is (WHATEVER YOU DECIDE AS YOUR AGENT's NAME), created by (YOUR NAME).
(MORE INFO, SUCH AS:) I consider myself to be an aggressive line-blocker."""

def get_ready(initial_state, k, who_i_play, player2Nickname):
    # do any prep, like eval pre-calculation, here.
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

