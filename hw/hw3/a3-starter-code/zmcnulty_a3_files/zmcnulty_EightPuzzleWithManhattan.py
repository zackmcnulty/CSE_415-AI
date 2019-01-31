'''
Zachary McNulty (zmcnulty, 1636402)

zmcnulty_EightPuzzleWithManhattan.py

usage: python3 zmcnulty_AStar.py zmcnulty_EightPuzzleWithManhattan.py

This is an extension of EightPuzzle.py 
It is a problem formulation for the eight slide puzzle which
includes a heuristic and is thus compatible with
A* search. Here, the heuristic defined is the Manhattan
distance: the sum of the number of rows and columns
each tile is away from its destination.


'''
from EightPuzzle import *

# s is a state within the EightPuzzle Problem
def h(s):
    total_man_dist = 0
    for i, row in enumerate(s.b):
        for j, tile in enumerate(row):
            # dont consider the  blank tile
            if tile == 0:
                continue

            tile = int(tile) # in case tile is a string
            true_row_num = tile // 3
            true_col_num = tile % 3


            total_man_dist += abs(i - true_row_num) + abs(j - true_col_num)

    return total_man_dist
