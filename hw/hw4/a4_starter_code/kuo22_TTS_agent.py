from TTS_State import TTS_State
import time

USE_CUSTOM_STATIC_EVAL_FUNCTION = True
USE_DEFAULT_ORDER = False

k = 3
my_side = 'B'

BLACK = "B"
WHITE = "W"
opponent = {
            "B": "W",
            "W": "B"
            }

class MY_TTS_State(TTS_State):
    def static_eval(self):
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval(WHITE) - self.custom_static_eval(BLACK)
        else :
            return self.basic_static_eval(WHITE) - self.basic_static_eval(BLACK)

    def get_moves(self, color):
        if USE_DEFAULT_ORDER: 
            return self.basic_moves(color)
        else:
            return self.custom_moves(color)

    def basic_static_eval(self, color):
        global k
        value = 0
        other_color = opponent[color]
        x = len(self.board[0])
        y = len(self.board)

        for row in self.board:
            for i in range(x):
                pieces = 0
                blocked = False
                for j in range(k):
                    tile = row[(i + j) % x]
                    if tile == '-' or tile == other_color:
                        blocked = True
                        break
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == 2:
                    value += 1
        # print('horizontal ' + str(value))

        # Check all vertical lines
        for i in range(x):
            for j in range(y):
                pieces = 0
                blocked = False
                for t in range(k):
                    tile = self.board[(j + t) % y][i]
                    if tile == '-' or tile == other_color:
                        blocked = True
                        break
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == 2:
                    value += 1
        
        # print('vertical ' + str(value))

        # Check for diagonals going down-right
        for i in range(y):
            for j in range(x):
                pieces = 0
                blocked = False
                for t in range(k):
                    tile = self.board[(i + t) % y][(j + t) % x]
                    if tile == '-' or tile == other_color:
                        blocked = True
                        break
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == 2:
                    value += 1

        # print('down-right ' + str(value))
        # Check for diagonals going down-left
        for i in range(y):
            for j in range(x):
                pieces = 0
                blocked = False
                for t in range(k):
                    tile = self.board[(i + t) % y][(j - t) % x]
                    if tile == '-' or tile == other_color:
                        blocked = True
                        break
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == 2:
                    value += 1
        # print('down-left ' + str(value))
        return value

    def custom_static_eval(self, color):
        global k
        value = 0
        other_color = opponent[color]
        x = len(self.board[0])
        y = len(self.board)

        for row in self.board:
            for i in range(x):
                pieces = 0
                blocked = False
                for j in range(k):
                    tile = row[(i + j) % x]
                    if tile == '-' or tile == other_color:
                        blocked = True
                        break
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == k:
                    value += 1000000
                if pieces > 0:
                    value += 2 ** pieces
        # print('horizontal ' + str(value))

        # Check all vertical lines
        for i in range(x):
            for j in range(y):
                pieces = 0
                blocked = False
                for t in range(k):
                    tile = self.board[(j + t) % y][i]
                    if tile == '-' or tile == other_color:
                        blocked = True
                        break
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == k:
                    value += 1000000
                if pieces > 0:
                    value += 2 ** pieces
        
        # print('vertical ' + str(value))

        # Check for diagonals going down-right
        for i in range(y):
            for j in range(x):
                pieces = 0
                blocked = False
                for t in range(k):
                    tile = self.board[(i + t) % y][(j + t) % x]
                    if tile == '-' or tile == other_color:
                        blocked = True
                        break
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == k:
                    value += 1000000
                if pieces > 0:
                    value += 2 ** pieces

        # print('down-right ' + str(value))
        # Check for diagonals going down-left
        for i in range(y):
            for j in range(x):
                pieces = 0
                blocked = False
                for t in range(k):
                    tile = self.board[(i + t) % y][(j - t) % x]
                    if tile == '-' or tile == other_color:
                        blocked = True
                        break
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == k:
                    value += 1000000
                if pieces > 0:
                    value += 2 ** pieces
        # print('down-left ' + str(value))
        return value
    
    # Left to right, top to bottom
    def basic_moves(self, color):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if (self.board[i][j] == ' '):
                    new_state = MY_TTS_State(self.board)
                    new_state.board[i][j] = color
                    moves.append(new_state)
        return moves
    
    # Still left to right, but starts from the center rows up, then center rows down
    def custom_moves(self, color):
        moves = []
        for i in reversed(range(int(len(self.board) / 2))):
            for j in range(len(self.board[0])):
                if (self.board[i][j] == ' '):
                    new_state = MY_TTS_State(self.board)
                    new_state.board[i][j] = color
                    moves.append(new_state)

        for i in range(int(len(self.board) / 2), len(self.board)):
            for j in range(len(self.board[0])):
                if (self.board[i][j] == ' '):
                    new_state = MY_TTS_State(self.board)
                    new_state.board[i][j] = color
                    moves.append(new_state)
        return moves




def get_ready(initial_state, _k, what_side_i_play, opponent_moniker):
    global k, my_side
    k = _k
    my_side = what_side_i_play
    return "OK"

def who_am_i():
    return """I am Shrek, the most intelligent being in the swamp.  I am created
by Kuo (UW ID: kuo22), and I will beat you while throwing insults at you."""

def moniker():
    return 'Shrek'

utterance_count = 0

def take_turn(current_state, opponents_utterance, time_limit = 10):
    global start_time, time_lim, my_side, utterance_count
    start_time = time.perf_counter()
    time_lim = time_limit
    new_state = MY_TTS_State(current_state.board)

    # Utterances
    utterance = ["You are not good enough to beat me!",
                "I better not see you in this swamp again if you lose.",
                "Your moves are too easy to read.",
                "Even Donkey can play better than you!",
                "If by chance that I lose to you, it is because your moves are putting me to sleep.",
                "I better make this quick so I can hunt my dinner early.",
                "*Yawn* This match is boring.",
                "Maybe I should have you for dinner.",
                "This move should get you!",
                "Don't you think I don't know how to play this game just because of my look!",
                "Hah! You call that a move? I will show you a move."]
    # Fix up whose turn it will be.
    who = current_state.whose_turn
    new_who = 'B'  
    if who=='B': new_who = 'W'  

    best_state = None
    last_best = None

    current_max_ply = 1
    while current_max_ply <= 4:
        last_best = best_state
        best_state = best_move(0, current_max_ply, new_state, my_side, float("-inf"), float("inf"))
        current_max_ply += 1
        end_time = time.perf_counter()
        if end_time - start_time > time_limit * 0.90:
            best_state = last_best
            break   
    x = 0
    y = 0

    moved = False
    for i in range(len(new_state.board)):
        for j in range(len(new_state.board[0])):
            if new_state.board[i][j] != best_state.board[i][j]:
                x = j
                y = i
                moved = True
                break
        if moved:
            break
    
    best_state.whose_turn = new_who
    utterance_count += 1
    if not moved:
        return [[False, current_state], "I can't move, dummy!"]
    else:
        return [[(y,x), best_state], utterance[utterance_count % 11]]


# Best search for my agent. Modification of alpha-beta pruning with less overhead
def best_move(current_depth, max_ply, current_state, color, alpha, beta):
    global start_time, time_lim

    current_time = time.perf_counter()
    if current_time - start_time > time_lim * 0.90:
        return current_state

    moves = current_state.get_moves(color)
    if not moves or current_depth == max_ply:
        return current_state

    optimal_state = current_state
    for move in moves:
        state = best_move(current_depth + 1, max_ply, move, opponent[color], alpha, beta)
        move_value = state.static_eval()
        if color == WHITE:
            if move_value > alpha:
                alpha = move_value
                if current_depth == 0:
                    optimal_state = move
                else: 
                    optimal_state = state
        else:
            if move_value < beta:
                beta = move_value
                if current_depth == 0:
                    optimal_state = move
                else: 
                    optimal_state = state
        
        # Prune step
        if alpha >= beta:
            return optimal_state

    return optimal_state


eval_value = 0
states_expanded = 0
states_evaluated = 0
maximum_depth = 0
num_cutoff = 0
start_time = 0
time_lim =  False
optimal_value = 0

def parameterized_minimax(
       current_state=None,
       use_iterative_deepening_and_time = False,
       max_ply=2,
       use_default_move_ordering = False,
       alpha_beta=False, 
       time_limit=1.0,
       use_custom_static_eval_function=False):

    global USE_CUSTOM_STATIC_EVAL_FUNCTION, USE_DEFAULT_ORDER, eval_value, states_expanded, states_evaluated, maximum_depth, num_cutoff, start_time, time_lim, optimal_value

    start_time = time.perf_counter()
    time_lim = time_limit
    USE_CUSTOM_STATIC_EVAL_FUNCTION = use_custom_static_eval_function
    USE_DEFAULT_ORDER = use_default_move_ordering
    new_state = MY_TTS_State(current_state.board)
    best_state = None

    if alpha_beta:
        if use_iterative_deepening_and_time:
            current_max_ply = 1
            while current_max_ply <= max_ply:
                best_state = timed_minimax_pruning(0, current_max_ply, new_state, my_side, float("-inf"), float("inf"))
                current_max_ply += 1
                end_time = time.perf_counter()
                if end_time - start_time > time_limit * 0.9:
                    break
        else:
            best_state = minimax_pruning(0, max_ply, new_state, my_side, float("-inf"), float("inf"))
    else:
        if use_iterative_deepening_and_time:
            current_max_ply = 1
            while current_max_ply <= max_ply:
                best_state = timed_minimax_search(0, current_max_ply, new_state, my_side)
                current_max_ply += 1
                end_time = time.perf_counter()
                if end_time - start_time > time_limit * 0.9:
                    break   
        else:
            best_state = minimax_search(0, max_ply, new_state, my_side)
    eval_value = best_state.static_eval()
    print(str(best_state))
    end_time = time.perf_counter()
    print("time: " + str(end_time - start_time))
    return [eval_value, states_expanded, states_evaluated, maximum_depth, num_cutoff]

def minimax_search(current_depth, max_ply, current_state, color):
    global eval_value, states_expanded, states_evaluated, maximum_depth, num_cutoff

    if current_depth > maximum_depth:
        maximum_depth = current_depth

    # new_state = MY_TTS_State(current_state.board)
    moves = current_state.get_moves(color)
    if not moves or current_depth == max_ply:
        states_evaluated += 1
        return current_state
    states_expanded += 1
    optimal_value = 0
    if color == WHITE:
        optimal_value = float("-inf")
    else:
        optimal_value = float("inf")
    optimal_state = None
    for move in moves:
        state = minimax_search(current_depth + 1, max_ply, move, opponent[color])
        move_value = state.static_eval()
        if color == WHITE and move_value > optimal_value:
            optimal_state = state
            optimal_value = move_value
        if color == BLACK and move_value < optimal_value:
            optimal_state = state
            optimal_value = move_value
    return optimal_state

def timed_minimax_search(current_depth, max_ply, current_state, color):
    global eval_value, states_expanded, states_evaluated, maximum_depth, num_cutoff, start_time, time_lim

    current_time = time.perf_counter()
    if current_time - start_time > time_lim * 0.9:
        return current_state

    if current_depth > maximum_depth:
        maximum_depth = current_depth

    moves = current_state.get_moves(color)
    if not moves or current_depth == max_ply:
        states_evaluated += 1
        return current_state
    states_expanded += 1
    optimal_value = 0
    if color == WHITE:
        optimal_value = float("-inf")
    else:
        optimal_value = float("inf")
    optimal_state = None
    for move in moves:
        state = timed_minimax_search(current_depth + 1, max_ply, move, opponent[color])
        move_value = state.static_eval()
        if color == WHITE and move_value > optimal_value:
            optimal_state = state
            optimal_value = move_value
        if color == BLACK and move_value < optimal_value:
            optimal_state = state
            optimal_value = move_value
    return optimal_state

# Minimax with alpha-beta pruning
def minimax_pruning(current_depth, max_ply, current_state, color, alpha, beta):
    global states_expanded, states_evaluated, maximum_depth, num_cutoff

    if current_depth > maximum_depth:
        maximum_depth = current_depth
    
    moves = current_state.get_moves(color)
    if not moves or current_depth == max_ply:
        states_evaluated += 1
        return current_state

    states_expanded += 1
    optimal_state = current_state
    for move in moves:
        state = minimax_pruning(current_depth + 1, max_ply, move, opponent[color], alpha, beta)
        move_value = state.static_eval()
        if color == WHITE:
            if move_value > alpha:
                alpha = move_value
                optimal_state = state
        else:
            if move_value < beta:
                beta = move_value
                optimal_state = state
        
        # Prune step
        if alpha >= beta:
            num_cutoff += 1
            return optimal_state

    return optimal_state

def timed_minimax_pruning(current_depth, max_ply, current_state, color, alpha, beta):
    global states_expanded, states_evaluated, maximum_depth, num_cutoff, time, start_time, time_lim

    current_time = time.perf_counter()
    if current_time - start_time > time_lim * 0.9:
        return current_state

    if current_depth > maximum_depth:
        maximum_depth = current_depth
    
    moves = current_state.get_moves(color)
    if not moves or current_depth == max_ply:
        states_evaluated += 1
        return current_state

    states_expanded += 1
    optimal_state = current_state
    for move in moves:
        state = minimax_pruning(current_depth + 1, max_ply, move, opponent[color], alpha, beta)
        move_value = state.static_eval()
        if color == WHITE:
            if move_value > alpha:
                alpha = move_value
                optimal_state = state
        else:
            if move_value < beta:
                beta = move_value
                optimal_state = state
        
        # Prune step
        if alpha >= beta:
            num_cutoff += 1
            return optimal_state

    return optimal_state

# INITIAL_BOARD = \
#                 [[' ',' ',' ',' '],
#                 [' ','B',' ',' '],
#                 [' ',' ','B',' '],
#                 [' ',' ',' ',' ']]

# INITIAL_BOARD = \
#                 [[' ','B',' ',' ',' ']]


# INITIAL_BOARD = \
#                 [['W','W'],
#                 [' ',' '],
#                 [' ',' '],
#                 [' ',' ']]

# INITIAL_BOARD = \
#             [['W', '-', '-', '-'],
#             ['-', '-', ' ', '-'],
#             ['-', ' ', '-', '-'],
#             ['-', '-', 'B', '-']]

# INITIAL_BOARD = \
#                 [[' ',' ','W',' ',' ','-',' ',' '],
#                 ['B',' ','B','B',' ',' ','W',' '],
#                 [' ',' ',' ',' ','-',' ',' ',' ']]

# init_state = TTS_State(INITIAL_BOARD)
# new_state = MY_TTS_State(init_state.board)

# # print(new_state.static_eval())
# result = parameterized_minimax(current_state = new_state, use_iterative_deepening_and_time = False, use_default_move_ordering = False, max_ply = 4, alpha_beta=True, use_custom_static_eval_function=False, time_limit=5)
# print(str(result))
