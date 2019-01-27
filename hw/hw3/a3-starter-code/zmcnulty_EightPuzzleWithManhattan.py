
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
