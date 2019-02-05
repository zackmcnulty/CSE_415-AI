'''game_master.py
Simple game administration, for basic testing of game-playing agents
that play "Toro-Tile Straight" which is a game that requires placing
tiles in a toroidal space to try to form a straight line of a certain
length.

This game master does not time the moves of the players.

(C) S. Tanimoto, Jan. 25, 2018.
University of Washington.
'''

USE_HTML = True

from TTS_State import TTS_State

import sys
if sys.argv==[''] or len(sys.argv)<3:
  print("Usage: python3 game_master.py Tetra_Toro_Game_Type PlayerA PlayerB")
  exit(0)

game_type_module_name = sys.argv[1]
import importlib
GTM = importlib.import_module(game_type_module_name)
INITIAL_BOARD = GTM.INITIAL_BOARD
K = GTM.K
GAME_TYPE = GTM.GAME_TYPE

player1 =importlib.import_module(sys.argv[2])
player2 =importlib.import_module(sys.argv[3])

import TTS_win_tester

if USE_HTML: import game_to_html as html

# from Tetra_Toro_Game_Type import INITIAL_BOARD, GAME_TYPE, K

def calculate_max_turns(b):
  "How many ' ' characters are in the board representation?"
  count = 0
  for row in b:
    for elt in row:
      if elt==' ': count+=1
  return count

TURN_LIMIT = calculate_max_turns(INITIAL_BOARD)

TIME_PER_MOVE = 10

N = len(INITIAL_BOARD[0])    # height of board
M = len(INITIAL_BOARD[0][0]) # width of board

INITIAL_STATE = TTS_State(INITIAL_BOARD)

FINISHED = False
def runGame():
    currentState = INITIAL_STATE
    print('The Gamemaster says, "Our game type for this match is: '+GAME_TYPE+'"')
    print('The Gamemaster says, "Players, introduce yourselves."')
    print('     (Playing White:) '+player1.who_am_i())
    print('     (Playing Black:) '+player2.who_am_i())

    if USE_HTML:
        html.startHTML(player1.moniker(), player1.who_am_i(),
                       player2.moniker(), player2.who_am_i(), GAME_TYPE, K, 1)
    try:
        p1comment = player1.get_ready(INITIAL_STATE, K, 'W', player2.moniker())
    except Exception as e:
        report = 'Player 1 ('+player1.moniker()+' failed to prepare, and loses by default.'
        print(report)
        if USE_HTML: html.reportResult(report)
        report = 'Congratulations to Player 2 ('+player2.moniker()+')!'
        print(report)
        if USE_HTML: html.reportResult(report)
        if USE_HTML: html.endHTML()
        print(e)
        return
    try:
        p2comment = player2.get_ready(INITIAL_STATE, K, 'B', player1.moniker())
    except Exception as e:
        report = 'Player 2 ('+player2.moniker()+' failed to prepare, and loses by default.'
        print(report)
        if USE_HTML: html.reportResult(report)
        report = 'Congratulations to Player 1 ('+player1.moniker()+')!'
        print(report)
        if USE_HTML: html.reportResult(report)
        if USE_HTML: html.endHTML()
        print(e)
        return
                    
    print('The Gamemaster says, "Let\'s Play!"')
    print('The initial state is...')

    currentRemark = "The game is starting."
    if USE_HTML: html.stateToHTML(currentState)

    WhitesTurn = True
    name = None
    global FINISHED
    FINISHED = False
    turnCount = 0
    printState(currentState)
    while not FINISHED:
        who = currentState.whose_turn
        if WhitesTurn:
            playerResult = player1.take_turn(currentState, currentRemark, TIME_PER_MOVE)
            name = player1.moniker()
            WhitesTurn = False
        else:
            playerResult = player2.take_turn(currentState, currentRemark, TIME_PER_MOVE)
            name = player2.moniker()
            WhitesTurn = True
        moveAndState, currentRemark = playerResult
        if moveAndState==None:
            FINISHED = True; continue
        move, currentState = moveAndState
        moveReport = "In turn "+str(turnCount)+", move is by "+who+" to "+str(move)
        print(moveReport)
        utteranceReport = name +' says: '+currentRemark
        print(utteranceReport)
        if USE_HTML: html.reportResult(moveReport)
        if USE_HTML: html.reportResult(utteranceReport)
        possibleWin = TTS_win_tester.get_win(currentState, move, K)
        if possibleWin != "No win":
            FINISHED = True
            printState(currentState)
            if USE_HTML: html.stateToHTML(currentState, finished=True)
            print(possibleWin)
            if USE_HTML: html.reportResult(possibleWin)
            if USE_HTML: html.endHTML()
            return
        printState(currentState)
        if USE_HTML: html.stateToHTML(currentState)
        turnCount += 1
        if turnCount == TURN_LIMIT: FINISHED=True
    #printState(currentState)
    #if USE_HTML: html.stateToHTML(currentState)
    who = currentState.whose_turn
    print("Game over; it's a draw.")
    if USE_HTML: html.reportResult("Game Over; it's a draw")
    if USE_HTML: html.endHTML()

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
    
runGame()
