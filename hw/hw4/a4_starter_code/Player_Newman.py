'''PlayerSkeletonA.py
An agent that plays Toro-Tile Straight,
but rather poorly.

'''

from TTS_State import TTS_State

def take_turn(current_state, last_utterance, time_limit):

    # Compute the new state for a move.
    # Start by copying the current state.
    new_state = TTS_State(current_state.board)
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
    return "Newman"

def who_am_i():
    return "I'm Newman Doeknot, a newbie Toro-Tile Straight agent."

def get_ready(initial_state, k, who_i_play, player2Nickname):
    return "OK"


