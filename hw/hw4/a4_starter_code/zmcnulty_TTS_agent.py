'''
Zachary McNulty (zmcnulty, 1636402)

zmcnulty_TTS_agent.py
'''

from TTS_State import TTS_State
import time
from random import randint

# DEFINE GLOBAL VARIABLES
RIGHT = (1,0)
UP = (0,1)
UP_RIGHT = (1,1)
DOWN_RIGHT = (1,-1)

DIRECTIONS = [RIGHT, UP, UP_RIGHT, DOWN_RIGHT]

USE_CUSTOM_STATIC_EVAL_FUNCTION = False
VACANCIES = []
K = 1 # default; will be overwritten

ZOBRIST_HASHES = {}
zobristnum = None

# END GLOBAL VARIABLES


class My_TTS_State(TTS_State):

  def __init__(self, board, whose_turn="W"):
    super().__init__(board, whose_turn)
    self.num_rows = len(self.board)
    self.num_cols = len(self.board[0])
    global zobristnum

    if zobristnum == None:
        self.init_zobrist()

  def init_zobrist(self):
    global zobristnum
    num_squares = self.num_cols * self.num_rows
    num_states = 4 # black white empty blocked

    zobristnum = [[0]*num_states for i in range(num_squares)]
    for i in range(num_squares):
        for j in range(num_states):
            zobristnum[i][j] = randint(0, 4294967296)

  def zobrist_hash(self):
      val = 0
      for i,row in enumerate(self.board):
          for j,tile in enumerate(row):
              if tile == ' ': piece = 0
              elif tile == 'W': piece = 1
              elif tile == 'B': piece = 2
              else: piece = 3#tile == '-'

              val ^= zobristnum[i * self.num_cols + j][piece]

      return val

  def get_vacancies_default(self):
      vacancies = []
      for i, row in enumerate(self.board):
          for j, tile in enumerate(row):
              if tile == ' ':
                  vacancies.append((i,j))

      return vacancies

  # TODO: change to optimize?
  def get_vacancies(self):
      return self.get_vacancies_default()

  def static_eval(self):
    if USE_CUSTOM_STATIC_EVAL_FUNCTION:
      return self.custom_static_eval()
    else:
      return self.basic_static_eval()

  # assumes that K < both dimensions of the board
  def basic_static_eval(self):
    #self.board gives the current board
    # K is a global variable
    global K
    CW = 0 # count of C(white, 2)
    CB = 0 # count of C(black, 2)
    
    num_rows = len(self.board)
    for i, row in enumerate(self.board):
        num_cols = len(row)
        for j, col in enumerate(row):
            for dir in DIRECTIONS:
               squares = [self.board[(i + k*dir[0]) % num_rows][(j + k*dir[1]) % num_cols] for k in range(K)]
               if squares.count('W') == 2:
                    CW += 1
               if squares.count('B') == 2:
                    CB += 1

    return CW - CB


  def custom_static_eval(self):
    global K
    W_score = 0
    B_score = 0
    base = 3
   
    num_rows = len(self.board)
    for i, row in enumerate(self.board):
        num_cols = len(row)

        for j, col in enumerate(row):
            # at each index i, store the number of lines of length K
            # with i White tiles or i Black tiles respectively
            # i.e. this counts how many lines with i W/B that converge on a given square!
            CW = [0]*(K+1)
            CB = [0]*(K+1)

            for dir in DIRECTIONS:
               squares = [self.board[(i + k*dir[0]) % num_rows][(j + k*dir[1]) % num_cols] for k in range(K)]
               CW[squares.count('W')] += 1
               CB[squares.count('B')] += 1

            W_score += sum([s*base**i for i,s in enumerate(CW)])
            B_score += sum([s*base**i for i,s in enumerate(CB)])


    return W_score - B_score

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
    # also guarentees that VACANCIES has only OPEN spots
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
    max_depth = -1
    max_ply = 10 # put a depth limit

    #NOTE: assume max_ply is < actually max depth of the system?
    while max_depth < max_ply and time.time() - start_time < time_limit:

      # results = [current_state static eval, n_states expanded, n static evals, n ab cutoffs]
      # returns None if ran out of time
      max_depth += 1

      # begin search at last layer previously explored.

      # make a valid move and assess its state
      options = {}
      for spot in VACANCIES:
        if new_state.board[spot[0]][spot[1]] == ' ':
            new_state.board[spot[0]][spot[1]] = who
            options[spot] = parameterized_minimax(new_state) 
            new_state.board[spot[0]][spot[1]] = ' '
        else: 
            VACANCIES.remove(spot)

      move = max(options.keys(), key=(lambda key: options[key]))
      # have this return best move..
    


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
    global K
    K = k

    # do any prep, like eval pre-calculation, here.
    # find blocked and vacant squares?

    # create Zobrist hash table for each state?


    # find VACANCIES, sorted in order of relevance
    VACANCIES = initial_state.get_vacancies()
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

  # give a bit of time for program to finish up so we dont exceed time limit
  time_buffer = 0.01

  start_time = time.time()
  time_limit = time_limit - time_buffer

  # use my custom static eval function if told so
  global USE_CUSTOM_STATIC_EVAL_FUNCTION
  USE_CUSTOM_STATIC_EVAL_FUNCTION = use_custom_static_eval_function

  # use my custom TTS state object
  current_state.__class__ = My_TTS_State

  # get all the open squares.
  if use_default_move_ordering:
    vacancies = current_state.get_vacancies_default()
  else:
    vacancies = current_state.get_vacancies()

  if use_iterative_deepening_and_time:
      max_depth = -1

      #NOTE: assume max_ply is < actually max depth of the system?
      while max_depth <= max_ply and time.time() - start_time < time_limit:

          # results = [current_state static eval, n_states expanded, n static evals, n ab cutoffs]
          # returns None if ran out of time
          max_depth += 1

          # begin search at last layer previously explored.
          # save this for above; initial_open = [state for state in DEPTHS if DEPTHS[state] == max_depth - 1]

          # UNLIKE our hw2, if we find a state that is 5 moves away, there is no
          # way for us to reach that state in less than 5 moves so we do not have to worry about
          # rexpanding given states (save that for later

          dfs_results = DFS(current_state, vacancies, max_depth, use_default_move_ordering, alpha_beta, time_limit - (time.time() - start_time))
        
          if dfs_results != None: # DFS returns None if it is running out of time
              current_state_static_val = dfs_results[0]
              n_states_expanded += dfs_results[1]
              n_static_evals_performed += dfs_results[2]
              n_ab_cutoffs += dfs_results[3]
          
      max_depth_reached = max_depth - 1 # NOTE: max depth reached or max depth fully explored (i chose latter)?
  else: 
      # just run DFS with the max depth starting at the max_ply, and an unreasonably high time limt
      # so that its not an issue.
      dfs_results = DFS(current_state, vacancies, max_ply, use_default_move_ordering, alpha_beta)

      current_state_static_val = dfs_results[0]
      n_states_expanded += dfs_results[1]
      n_static_evals_performed += dfs_results[2]
      n_ab_cutoffs += dfs_results[3]
      max_depth_reached = min(max_ply, len(vacancies)) #TODO: is the any reason not to do this?


  # Prepare to return the results, don't change the order of the results
  results = []
  results.append(current_state_static_val)
  results.append(n_states_expanded)
  results.append(n_static_evals_performed)
  results.append(max_depth_reached)
  results.append(n_ab_cutoffs)
  # Actually return the list of all results...
  return(results)

# NOTE: See HW2 IDDFS.py for an example of how this was implemented; I reused most of my ideas from there
# who = whose turn it current is
# initial_open = what states to start on the OPEN list
# DEPTHS list of depths of each state
def DFS(current_state, vacancies, max_depth, use_default_move_ordering, alpha_beta, time_limit = 10**8, alpha = -10**8, beta = 10**8):
    start_time = time.time()

    states_expanded = 0
    static_evals = 0
    num_ab_cutoffs = 0

   # check whose turn it is
    who = current_state.whose_turn
    if who == 'B':
        current_state_static_val = 10**8
    else:
        current_state_static_val = -10**8

    #NOTE: might want to give a few fractions of a second in leeway
    # results = [current_state static eval, n_states expanded, n static evals, n ab cutoffs]
    if time.time() - start_time > time_limit: 
        return None

    #NOTE: do we want to count the latter case where the board is full as expanding a state???
    elif max_depth == 0 or len(vacancies) == 0:
        static_evals  = 1
        zhash = current_state.zobrist_hash()
        if zhash in ZOBRIST_HASHES:
            current_state_static_val = ZOBRIST_HASHES[zhash]
        else:
            current_state_static_val = current_state.static_eval()
            ZOBRIST_HASHES[zhash] = current_state_static_val

        return [current_state_static_val, states_expanded, static_evals, num_ab_cutoffs]
    else:
        states_expanded = 1
        # for each possible vacancy/move:
        #   make a new board after making that move
        #   swap whose turn it is
        #   Run DFS on the new board.
        for (i,j) in vacancies:
            new_state = My_TTS_State(current_state.board)
            new_state.board[i][j] = who

            if who == 'B':
                new_state.whose_turn = 'W'
                beta = min(beta, current_state_static_val)
            else:
                new_state.whose_turn = 'B'
                alpha = max(alpha, current_state_static_val)

            if alpha_beta and beta < alpha:
                num_ab_cutoffs += 1
            else:
                new_vacancies = [v for v in vacancies if not v == (i,j)]
                results = DFS(new_state, new_vacancies,  max_depth - 1, use_default_move_ordering, alpha_beta, time_limit - (time.time() - start_time), alpha, beta)

                if results == None: # we are running out of time!
                    return None

                if who == 'B': # black is minimizer
                    current_state_static_val = min(current_state_static_val, results[0]) 
                else: # white is maximizer
                    current_state_static_val = max(current_state_static_val, results[0]) 
                        
                states_expanded += results[1]
                static_evals += results[2]
                num_ab_cutoffs += results[3]


    return [current_state_static_val, states_expanded, static_evals, num_ab_cutoffs]



K = 5
inital_board = \
            [[' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            ['-', ' ', '-', ' '],
            [' ', ' ', ' ', ' ']]

#inital_board = \
#        [['W', 'W'],
#          [' ', ' '],
#          [' ', ' '],
#          [' ', ' ']]

init_state = My_TTS_State(inital_board)
init_state.whose_turn = 'W'
USE_CUSTOM_STATIC_EVAL_FUNCTION = False

print("static_eval: ", init_state.static_eval())


start = time.time()
print("[current_state_static_val, n_states_expanded, static evals, max_depth, num_ab cutoffs ]:", parameterized_minimax(init_state, use_iterative_deepening_and_time = True, max_ply = 10, alpha_beta=True, time_limit = 1))
print(time.time() - start)
#start = time.time()
#print("[current_state_static_val, n_states_expanded, static evals, max_depth, num_ab cutoffs ]:", parameterized_minimax(init_state, use_iterative_deepening_and_time = False, max_ply = 5, alpha_beta=True))
#print(time.time() - start)

