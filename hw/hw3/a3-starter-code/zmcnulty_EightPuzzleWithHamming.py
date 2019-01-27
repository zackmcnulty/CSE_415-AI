# comment and description of heuristic


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
