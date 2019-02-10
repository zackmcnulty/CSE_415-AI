'''
Zachary McNulty (zmcnulty, 1636402)

zmcnulty_TTS_agent.py
'''

from TTS_State import TTS_State
import time
from random import randint
from random import shuffle

# DEFINE GLOBAL VARIABLES
RIGHT = (1,0)
UP = (0,1)
UP_RIGHT = (1,1)
DOWN_RIGHT = (1,-1)

DIRECTIONS = [RIGHT, UP, UP_RIGHT, DOWN_RIGHT]

USE_CUSTOM_STATIC_EVAL_FUNCTION = False
K = 1 # default; will be overwritten

ZOBRIST_HASHES = {}
zobristnum = None

# END GLOBAL VARIABLES


class My_TTS_State(TTS_State):

  def init_zobrist(self):
    global zobristnum
    num_cols = len(self.board[0])
    num_rows = len(self.board)
    num_squares = num_cols * num_rows
    num_states = 4 # black white empty blocked

    zobristnum = [[0]*num_states for i in range(num_squares)]
    for i in range(num_squares):
        for j in range(num_states):
            zobristnum[i][j] = randint(0, 4294967296)

  def zobrist_hash(self):
      global zobristnum
      if zobristnum == None:
        self.init_zobrist()

      num_cols = len(self.board[0])
      num_rows = len(self.board)
      val = 0
      for i,row in enumerate(self.board):
          for j,tile in enumerate(row):
              if tile == ' ': piece = 0
              elif tile == 'W': piece = 1
              elif tile == 'B': piece = 2
              else: piece = 3#tile == '-'
              val ^= zobristnum[i * num_cols + j][piece]

      return val

  def get_vacancies_default(self):
      vacancies = []
      for i, row in enumerate(self.board):
          for j, tile in enumerate(row):
              if tile == ' ':
                  vacancies.append((i,j))

      return vacancies

  # consider populated areas first!
  # sort the vacancies by the number of neighbors either B or W descending
  def get_vacancies(self):
     num_cols = len(self.board[0])
     num_rows = len(self.board)
     vacancies = self.get_vacancies_default()
     adjacents = {v:0 for v in vacancies}

     for spot in vacancies:
         count = 0
         for dir in [(1,0), (1,1), (0,1), (-1,0), (0,-1), (-1,-1), (1,-1), (-1,1)]:
             if self.board[(spot[0] + dir[0]) % num_rows][(spot[1] + dir[1]) % num_cols] in ['W', 'B']:
                 count +=1
         
         adjacents[spot] = count

     return sorted(vacancies, reverse=True, key = lambda v: adjacents[v])
            

    


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
               count_W = squares.count('W')
               count_B = squares.count('B')
               count_forbid = squares.count('-')
               if count_W == 2 and count_B == 0 and count_forbid == 0:
                    CW += 1
               if count_B == 2 and count_W == 0 and count_forbid == 0:
                    CB += 1

    return CW - CB


  def custom_static_eval(self):
    global K
    W_score = 0
    B_score = 0
    base = 10
   
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
               count_B = squares.count('B')
               count_W = squares.count('W')
               count_forbid = squares.count('-')
               if count_forbid == 0:
                   if count_B == 0:
                       CW[squares.count('W')] += 1
                   elif count_W == 0:
                       CB[squares.count('B')] += 1

            W_score += sum([s*base**i for i,s in enumerate(CW)])
            B_score += sum([s*base**i for i,s in enumerate(CB)])


    return W_score - B_score

def take_turn(current_state, last_utterance, time_limit):

    # use my custom static eval function if told so
    global USE_CUSTOM_STATIC_EVAL_FUNCTION
    USE_CUSTOM_STATIC_EVAL_FUNCTION = True
    default_ordering = False

    # use my custom TTS state object
    current_state.__class__ = My_TTS_State

    if default_ordering:
        vacancies = current_state.get_vacancies_default()
    else:
        vacancies = current_state.get_vacancies()
   
    # no possible moves
    if len(vacancies) == 0:
        return [[False, current_state], "The game has ended"]

    who = current_state.whose_turn
    new_state = My_TTS_State(current_state.board)
    if who == 'W': new_state.whose_turn = 'B'
    else: new_state.whose_turn = 'W'

    # give a bit of time for program to finish up so we dont exceed time limit
    time_buffer = 0.01
    start_time = time.time()
    time_limit = time_limit - time_buffer

    max_depth = -1

    while time.time() - start_time < time_limit:

        # results = [current_state static eval, n_states expanded, n static evals, n ab cutoffs, best_move]
        # returns None if ran out of time
        max_depth += 1

        dfs_results = DFS(current_state, vacancies, max_depth, use_default_move_ordering=default_ordering, alpha_beta=True, time_limit=time_limit - (time.time() - start_time))
      
        if dfs_results != None:
                move = dfs_results[4]
                last_results = dfs_results
          

    # make the move we have decided on
    new_state.board[move[0]][move[1]] = who

    # Make up a new remark
    new_utterance = make_utterance(new_state, last_results, last_utterance)
    return [[move, new_state], new_utterance]


# says something clever I guess
# makes comments about the current state of the game.
def make_utterance(current_state, last_results, last_utterance):
    vac_count= len(current_state.get_vacancies())
    static_val = current_state.static_eval()
    spaces = len(current_state.board) * len(current_state.board[0])

    if "lose" in last_utterance:
        return "don't say that. It is not over until its over"
    elif vac_count < 5:
        return "Oh we are in the endgame now... Only " + str(vac_count) + " moves left..."
    elif vac_count / spaces > 0.8:
        return "This game has barely just begun. There are still " + str(3**vac_count) + "games that could be played, roughly"
    elif static_val < 0.8*last_results[0]:
        return "At first I thought I was in a good place, but now I am not so sure. I don't like what I see a few moves ahead."
    elif last_results[0] < -200:
        return "This is not looking good for me. You're ahead on points, " + str(-1*last_results[0]) + " points according to my calculations."
    elif last_results[0] > 200:
        return "I make this game look easy! According to my calculations, I am " + str(last_results[0]) + " points ahead!"
    else:
        rhymes = {'0':"zero is my hero", '1':"one is so much fun", '2':"oh two boo hoo", '3':"three is good for me", '4':"four is more", '5':"five is alive", '6':"six just don't mix", '7':"seven is heaven", '8':"eight is fate", '9':"nine is just fine"}
        left = ", ".join([rhymes[digit] for digit in str(last_results[4][0])])
        right = ", ".join([rhymes[digit] for digit in str(last_results[4][1])])
        return left + " but " + right




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
    global K
    K = k

    # do any prep, like eval pre-calculation, here.
    # find blocked and vacant squares?

    # create Zobrist hash table for each state?

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

  # get all the open squares.
  if use_default_move_ordering:
    vacancies = current_state.get_vacancies_default()
  else:
    vacancies = current_state.get_vacancies()

  if use_iterative_deepening_and_time:
      # give a bit of time for program to finish up so we dont exceed time limit
      time_buffer = 0.01
      start_time = time.time()
      time_limit = time_limit - time_buffer

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
      print(dfs_results[4])
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

def DFS(current_state, vacancies, max_depth, use_default_move_ordering, alpha_beta, time_limit = 10**8, alpha = -10**8, beta = 10**8):
    start_time = time.time()

    states_expanded = 0
    static_evals = 0
    num_ab_cutoffs = 0

   # check whose turn it is; set the initial value v of the given state
    who = current_state.whose_turn
    if who == 'B':
        current_state_static_val = 10**8
    else:
        current_state_static_val = -10**8



    # if we dont have any time left
    if time.time() - start_time > time_limit: 
        return None

    #NOTE: do we want to count the latter case where the board is full as expanding a state??? NO see piazza
    # else if we are at the max depth/no moves are left calculate the static evaluation function
    # check if it is a state we already calculated in ZOBRIST_HASHES
    elif max_depth == 0 or len(vacancies) == 0:
        static_evals = 1
        zhash = current_state.zobrist_hash()
        if zhash in ZOBRIST_HASHES:
            current_state_static_val = ZOBRIST_HASHES[zhash]
        else:
            current_state_static_val = current_state.static_eval()
            ZOBRIST_HASHES[zhash] = current_state_static_val

        return [current_state_static_val, states_expanded, static_evals, num_ab_cutoffs, None]

    # else expand the state and look more moves ahead 
    else:
        states_expanded += 1
        # for each possible vacancy/move:
        #   make a new board after making that move
        #   swap whose turn it is
        #   Run DFS on the new board.
        for n, (i,j) in enumerate(vacancies):
            new_state = My_TTS_State(current_state.board)
            new_state.board[i][j] = who

            # calculate the alpha beta values for a given node
            if who == 'B':
                new_state.whose_turn = 'W'
                beta = min(beta, current_state_static_val)
            else:
                new_state.whose_turn = 'B'
                alpha = max(alpha, current_state_static_val)

            # check if we can prune the subtree
            if alpha_beta and beta <= alpha:
                num_ab_cutoffs += 1

                # NOTE: do I want to count the number of times I realize a cut can be made, or the number
                # of subtrees that are cut off. In this case, the two our different because each node
                # often has many more than two children
                #num_ab_cutoffs += len(vacancies) - n 
                break

            # if we cannot prune the subtree, traverse down it
            else:
                new_vacancies = [v for v in vacancies if not v == (i,j)]
                results = DFS(new_state, new_vacancies,  max_depth - 1, use_default_move_ordering, alpha_beta=alpha_beta, time_limit=time_limit - (time.time() - start_time), alpha=alpha, beta=beta)

                if results == None: # we are running out of time!
                    return None

                # black is minimizer so they will choose the child with LOWEST static eval
                if who == 'B': 
                    if results[0] < current_state_static_val:
                        current_state_static_val = results[0]
                        best_move = (i,j)

                else: # white is maximizer
                    if results[0] > current_state_static_val:
                        current_state_static_val = results[0]
                        best_move = (i,j)
                        
                states_expanded += results[1]
                static_evals += results[2]
                num_ab_cutoffs += results[3]


    return [current_state_static_val, states_expanded, static_evals, num_ab_cutoffs, best_move]





# ======================================================== Testing Code


'''
K = 3
inital_board = \
            [['W', '-', '-', '-'],
            ['-', '-', '-', '-'],
            ['-', '-', '-', '-'],
            [' ', '-', 'B', '-']]

init_state = My_TTS_State(inital_board)
init_state.whose_turn = 'B'

#print("static_eval: ", init_state.static_eval())


#start = time.time()
#print("[current_state_static_val, n_states_expanded, static evals, max_depth, num_ab cutoffs ]:", parameterized_minimax(init_state, use_iterative_deepening_and_time = True, max_ply = 10, alpha_beta=True, time_limit = 1))
#print(time.time() - start)
start = time.time()
print("eval, expand, eval count, max depth, ab cuts:", \
        parameterized_minimax(init_state, 
            use_iterative_deepening_and_time = False, 
            max_ply = 10, 
            alpha_beta=True,
            use_custom_static_eval_function =False , use_default_move_ordering=True))
print(time.time() - start)
'''
