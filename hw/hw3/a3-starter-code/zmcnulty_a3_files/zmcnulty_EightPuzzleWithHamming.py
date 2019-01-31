'''
Zachary McNulty (zmcnulty, 1636402)

zmcnulty_EightPuzzleWithHamming.py

usage: python3 zmcnulty_AStar.py zmcnulty_EightPuzzleWithHamming.py

This is an extended version of EightPuzzle.py that incorporates
a heuristic and is thus compatible with A* search.
The heuristic defined here is a simple Hamming function: it
counts the number of tiles out of place in the 8 puzzle.


'''

from EightPuzzle import *


# S is my given state in the eight puzzle problem formulation
def h(s):
    out_of_place = 0
    goal_state = [[0,1,2], [3,4,5], [6,7,8]]
    for i, row in enumerate(s.b):
        for j,tile in enumerate(row):
            
            # dont count the blank tile
            if tile != 0 and goal_state[i][j] != tile:
                out_of_place += 1

    return out_of_place
