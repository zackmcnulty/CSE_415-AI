'''timed_tts_game_master.py based on game_master.py

A game administration program for running matches of game-playing agents
that play "Toro-Tile Straight" which is a game that requires placing
tiles in a toroidal space to try to form a straight line of a certain
length.

This game master DOES time the moves of the players.
If a player's move takes too long, that player loses the game.

(C) S. Tanimoto, Jan. 25, 2018.
University of Washington.
'''

TIME_PER_MOVE = 0.5 # default time limit is half a second.
USE_HTML = True

import sys
if sys.argv==[''] or len(sys.argv)<3:
  print("Usage: python3 game_master.py Game_Type PlayerA PlayerB TIME_PER_MOVE")
  print("  for example:")
  print("python3 game_master.py Tetra_Toro_Game_Type PlayerSkeletonA PlayerSkeletonB 2.5")
  exit(0)
if len(sys.argv) > 3:
  TIME_PER_MOVE = float(sys.argv[4])

#from Gold_Rush_Game_Type import K, GAME_TYPE, INITIAL_BOARD
game_type_module_name = sys.argv[1]
import importlib
GTM = importlib.import_module(game_type_module_name)
INITIAL_BOARD = GTM.INITIAL_BOARD
K = GTM.K
GAME_TYPE = GTM.GAME_TYPE

player1 =importlib.import_module(sys.argv[2])
player2 =importlib.import_module(sys.argv[3])

from TTS_State import TTS_State

INITIAL_STATE = TTS_State(INITIAL_BOARD)

def count_blanks(state): # Find the limit on how many turns can be made from this state.
  c = 0; b = state.board
  for i in range(len(b)):
    for j in range(len(b[0])): c += 1
  return c

TURN_LIMIT = count_blanks(INITIAL_STATE) # draw if no moves left.

from TTS_win_tester import get_win
if USE_HTML: import game_to_html as gameToHTML

CURRENT_PLAYER = 'W'
N = len(INITIAL_STATE.board[0])    # height of board
M = len(INITIAL_STATE.board[0][0]) # width of board

FINISHED = False
def runGame():
    currentState = INITIAL_STATE
    print('The Gamemaster says, "Players, introduce yourselves."')
    print('     (Playing White:) '+player1.who_am_i())
    print('     (Playing Black:) '+player2.who_am_i())

    if USE_HTML:
        gameToHTML.startHTML(player1.moniker(), player1.who_am_i(),
                             player2.moniker(), player2.who_am_i(), GAME_TYPE, K, 1)
    try:
        p1comment = player1.get_ready(INITIAL_STATE, K, 'W', player2.moniker())
    except:
        report = 'Player 1 ('+player1.moniker()+' failed to prepare, and loses by default.'
        print(report)
        if USE_HTML: gameToHTML.reportResult(report)
        report = 'Congratulations to Player 2 ('+player2.moniker()+')!'
        print(report)
        if USE_HTML: gameToHTML.reportResult(report)
        if USE_HTML: gameToHTML.endHTML()
        return
    try:
        p2comment = player2.get_ready(INITIAL_STATE, K, 'B', player1.moniker())
    except:
        report = 'Player 2 ('+player2.moniker()+' failed to prepare, and loses by default.'
        print(report)
        if USE_HTML: gameToHTML.reportResult(report)
        report = 'Congratulations to Player 1 ('+player1.moniker()+')!'
        print(report)
        if USE_HTML: gameToHTML.reportResult(report)
        if USE_HTML: gameToHTML.endHTML()
        return
        return
    
                    
    print('The Gamemaster says, "Let\'s Play!"')
    print('The initial state is...')

    currentRemark = "The game is starting."
    if USE_HTML: gameToHTML.stateToHTML(currentState)

    WhitesTurn = True
    name = None
    global FINISHED
    FINISHED = False
    turnCount = 0
    printState(currentState)
    while not FINISHED:
        who = currentState.whose_turn
        global CURRENT_PLAYER
        CURRENT_PLAYER = who
        if WhitesTurn:
            playerResult = timeout(player1.take_turn,args=(currentState, currentRemark, TIME_PER_MOVE), kwargs={}, timeout_duration=TIME_PER_MOVE, default=(None,"I give up!"));
            name = player1.moniker()
            WhitesTurn = False
        else:
            playerResult = timeout(player2.take_turn,args=(currentState, currentRemark, TIME_PER_MOVE), kwargs={}, timeout_duration=TIME_PER_MOVE, default=(None,"I give up!"));
            name = player2.moniker()
            WhitesTurn = True
        if not playerResult: 
            print("No move could be found.")
            break
        moveAndState, currentRemark = playerResult
        if moveAndState==None:
            FINISHED = True; continue
        move, currentState = moveAndState
        if move==False:
            print("No move could be found.")
            break
        moveReport = "In turn "+str(turnCount)+", move is by "+who+" to "+str(move)
        print(moveReport)
        utteranceReport = name +' says: '+currentRemark
        print(utteranceReport)
        if USE_HTML: gameToHTML.reportResult(moveReport)
        if USE_HTML: gameToHTML.reportResult(utteranceReport)
        possibleWin = get_win(currentState, move, K)
        if possibleWin != "No win":
            FINISHED = True
            printState(currentState)
            if USE_HTML: gameToHTML.stateToHTML(currentState, finished=True)
            print(possibleWin)
            if USE_HTML: gameToHTML.reportResult(possibleWin)
            if USE_HTML: gameToHTML.endHTML()
            return
        printState(currentState)
        if USE_HTML: gameToHTML.stateToHTML(currentState)
        turnCount += 1
        if turnCount == TURN_LIMIT: FINISHED=True
    #printState(currentState)
    #if USE_HTML: gameToHTML.stateToHTML(currentState)
    who = currentState.whose_turn
    print("Game over; it's a draw.")
    if USE_HTML: gameToHTML.reportResult("Game Over; it's a draw")
    if USE_HTML: gameToHTML.endHTML()

def printState(s):
    global FINISHED
    board = s.board
    M = len(board[0])
    who = s.whose_turn
    horizontalBorder = "+"+3*M*"-"+"+"
    print(horizontalBorder)
    for row in board:
        print("|",end="")
        for item in row:
            print(" "+item+" ", end="") 
        print("|")
    print(horizontalBorder)
    if not FINISHED:
      print("It is "+who+"'s turn to move.\n")

import sys
import time
def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    '''This function will spawn a thread and run the given function using the args, kwargs and 
    return the given default value if the timeout_duration is exceeded 
    ''' 
    import threading
    class PlayerThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = default
        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except Exception as e:
                print("The agent threw an exception, or there was a problem with the time.")
                print(sys.exc_info())
                print(e[2])
                self.result = default

    pt = PlayerThread()
    pt.start()
    started_at = time.time()
    #print("take_turn started at: " + str(started_at))
    pt.join(timeout_duration)
    ended_at = time.time()
    #print("take_turn ended at: " + str(ended_at))
    diff = ended_at - started_at
    print("Used %0.4f seconds in take_turn, out of %0.4f" % (diff, timeout_duration))
    if pt.isAlive():
        print("Took too long.")
        print("We are now terminating the game.")
        print("Player "+CURRENT_PLAYER+" loses.")
        if USE_HTML: gameToHTML.reportResult("Player "+CURRENT_PLAYER+" took too long (%0.4f seconds) and thus loses." % diff)
        if USE_HTML: gameToHTML.endHTML()
        exit()
    else:
        #print("Within the time limit -- nice!")
        return pt.result

    
runGame()
