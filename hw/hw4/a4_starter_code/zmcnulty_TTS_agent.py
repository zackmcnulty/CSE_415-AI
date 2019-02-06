'''
Zachary McNulty (zmcnulty, 1636402)

zmcnulty_TTS_agent.py
'''

from TTS_State import TTS_State
import time

# DEFINE GLOBAL VARIABLES
RIGHT = (1,0)
UP = (0,1)
UP_RIGHT = (1,1)
DOWN_RIGHT = (1,-1)

DIRECTIONS = [RIGHT, UP, UP_RIGHT, DOWN_RIGHT]

USE_CUSTOM_STATIC_EVAL_FUNCTION = False
VACANCIES = []
BLOCKED = []
BLACK = []
WHITE = []
# END GLOBAL VARIABLES


class My_TTS_State(TTS_State):

  # surveys board, noting the location of all blocked and vacant tiles
  # as well as those taken by colored pieces
  def survey_board(self):
    global VACANCIES, BLOCKED, BLACK, WHITE
    for i, row in enumerate(self.board):
        for j, tile in enumerate(row):
            if tile == ' ': VACANCIES.append((i,j))
            elif tile == '-': BLOCKED.append((i,j))
            elif tile == 'B': BLACK.append((i,j))
            else: WHITE.append((i,j)) 

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
    # so we know how close to our time_limit we are
    start_time = time.time()

    # use my custom static eval because hopefully its better
    global USE_CUSTOM_STATIC_EVAL_FUNCTION
    USE_CUSTOM_STATIC_EVAL_FUNCTION = False # True

    # Compute the new state for a move.
    # Start by copying the current state.
    new_state = My_TTS_State(current_state.board)
    # Fix up whose turn it will be.
    who = current_state.whose_turn
    new_who = 'B'  

    if who=='B': new_who = 'W'  
    new_state.whose_turn = new_who
    
    # Find SOME valid move so we don't get timed out
    # move is of the form (row, col)
    while True:
        spot = VACANCIES[-1]
        tile = current_state.board[spot[0]][spot[1]]
        if tile  == ' ':
            move = spot
            break
        else:
            VACANCIES.pop()
            if tile == 'B': BLACK.append(spot)
            else: WHITE.append(spot)

    # Look for a better move using some actual strategy

    # make the move we have decided on
    new_state.board[move[0]][move[1]] = who
    VACANCIES.remove(move)
    if who == 'B': BLACK.append(move)
    else: WHITE.append(move)

    # Make up a new remark
    new_utterance = "I'll think harder in some future game. Here's my move"

    return [[move, new_state], new_utterance]

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

    # convert current state object to My_TTS_State
    initial_state.__class__ = My_TTS_State

    # do any prep, like eval pre-calculation, here.
    # find blocked and vacant squares?

    # create Zobrist hash table for each state?
    initial_state.survey_board()
    

    # find VACANCIES
    

    return "OK"

# The following is a skeleton for the function called parameterized_minimax,
# which should be a top-level function in each agent file.
# A tester or an autograder may do something like
# import ABC_TTS_agent as player, call get_ready(),
# and then it will be able to call tryout using something like this:
# results = player.parameterized_minimax(**kwargs)

# TODO: implement a more optimal ordering for search rather
# than the default which is used ALWAYS
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
  max_depth_reached = 0 #NOTE: for max depth, what are we counting? max depth reached or max layer fully explored
  n_ab_cutoffs = 0

  # MY CODE!

  # use my custom static eval function if told so
  global USE_CUSTOM_STATIC_EVAL_FUNCTION
  USE_CUSTOM_STATIC_EVAL_FUNCTION = use_custom_static_eval_function

  # use my custom TTS state object
  current_state.__class__ = My_TTS_State

  if use_iterative_deepening_and_time:
      max_depth = -1

      #NOTE: assume max_play is < actually max depth of the system?
      while max_depth < max_ply and time.time() - start_time < time_limit:

          # results = [current_state static eval, n_states expanded, n static evals, n ab cutoffs]
          # returns None if ran out of time
          max_depth += 1
          dfs_results = DFS(current_state, max_depth, use_default_move_ordering, alpha_beta, time_limit - (time.time() - start_time))
        
          if results != None:
              current_state_static_val = dfs_results[0]
              n_states_expanded += dfs_results[1]
              n_static_evals_performed += dfs_results[2]
              n_ab_cutoffs += dfs_results[3]
          
      max_depth_reached = max_depth - 1 # NOTE: max depth reached or max depth fully explored (i chose latter)?
  else: 
      # just run DFS with the max depth starting at the max_play, and an unreasonably high time limt
      # so that its not an issue.
      results = DFS(current_state, max_ply, use_default_move_ordering, alpha_beta, 10**10)

      current_state_static_val = dfs_results[0]
      n_states_expanded += dfs_results[1]
      n_static_evals_performed += dfs_results[2]
      n_ab_cutoffs += dfs_results[3]
      max_depth_reached = max_ply #TODO: is the any reason not to do this?


  # Prepare to return the results, don't change the order of the results
  results = []
  results.append(current_state_static_val)
  results.append(n_states_expanded)
  results.append(n_static_evals_performed)
  results.append(max_depth_reached)
  results.append(n_ab_cutoffs)
  # Actually return the list of all results...
  return(results)

def DFS(current_state, max_depth, use_default_move_ordering, alpha_beta, time_limit):
    OPEN = [current_state]
