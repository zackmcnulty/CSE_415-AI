'''
Zachary McNulty (zmcnulty, 1636402)
zmcnulty_Rubik2CubeWithHamming.py

This is a modified version of zmcnulty_Rubik2Cube.py which is
compatible with A* search. As such, it defines a heuristic function.
In this case, the heuristic simply counts the number of faces
whose color do not match the color of the face they are currently
on (i.e. the number of faces out of place). 

'''

import time
from zmcnulty_Rubik2Cube import *


# Hamming Heuristic Function
# NOT admissiable in this problen. Consider the case where we are one turn away from the goal:
# many more than one face will be out of place
def h(S):

    # flatten the string representation of the cube into a unqiue string
    state_str = "".join([c for c in str(S) if c.isdigit()])
    goal_str = "111100225533002255334444" 
    
    count = 0
    for i, digit in enumerate(state_str):
        if digit != goal_str[i]:
            count += 1

    return count 


