'''TTS_State.py
S. Tanimoto, January 25, 2018.

This file includes functions to support building agents
that play Toro-Tile Straight.  It should be imported by
Python files that implement move generation,
static evaluation, holding matches between players,
etc.

'''
BLACK ="B"
WHITE ="W"
NORTH = 0; SOUTH = 1; WEST = 2; EAST = 3; NW = 4; NE = 5; SW = 6; SE = 7

# Default game type, normally overwritten:
NAME = 'Tetra-Toro'

INITIAL_BOARD = \
               [[' ','-',' ',' '],
                [' ','-',' ','-'],
                ['-','-',' ',' '],
                [' ',' ','-',' ']]
K = 4

#print("INITIAL_BOARD = "+str(INITIAL_BOARD))

class TTS_State:
    def __init__(self, board, whose_turn=WHITE):
        new_board = [r[:] for r in board]  # Deeply copy the board.
        #print("new_board is " + str(new_board))
        self.board = new_board
        self.whose_turn = whose_turn;

    def __str__(self): # Produce an ASCII display of the state.
        s = 'TTS_State([\n'
        nrows = len(self.board)
        for i,r in enumerate(self.board):
            s += '  '+str(r)
            if i<nrows-1: s += ",\n"
            else:
              s += "],\n"
        if self.whose_turn==WHITE: s += '  "W"'
        else: s += '  "B"'
        s += ")\n"
        return s

    def __eq__(self, other):
      try:
        if self.whose_turn != other.whose_turn: return False
      except Exception as e:
        return False
      try:
        b1 = self.board
        b2 = other.board
        for i in range(8):
          for j in range(8):
            if b1[i][j] != b2[i][j]: return False
        return True
      except Exception as e:
        return False

    def copy(self):
      return TTS_State(self.board, self.whose_turn)

    def __hash__(self):
      return (str(self)).__hash__()      

def test_starting_board():
  init_state = TTS_State(INITIAL_BOARD)
  print(init_state)

if __name__ == "__main__":
  test_starting_board()
