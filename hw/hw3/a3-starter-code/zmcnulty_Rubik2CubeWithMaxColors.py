'''
Zachary McNulty (zmcnulty, 1636402)

This is an extension of zmcnulty_Rubik2Cube.py

It is a problem formula for the 2 x 2 x 2 Rubik Cube and
defines a heuristic. As such, it is compatible with
A* Search. In this case, the heuristic defined is to
count the maximum number of colors on any one face.
'''
import time
from zmcnulty_Rubik2Cube import *

# Heuristic: let the heuristic be the max number of colors on one face minus 1

def h(S):
    state_str = "".join([c for c in str(S) if c.isdigit()])
    up = set(state_str[:4])
    front = set(state_str[4:6])
    right = set(state_str[6:8])
    back = set(state_str[8:10])
    left = set(state_str[10:12])
    front.update(state_str[12:14])
    right.update(state_str[14:16])
    back.update(state_str[16:18])
    left.update(state_str[18:20])
    down = set(state_str[20:])
   
    return sum([len(front), len(back), len(right), len(left), len(up), len(down)]) - 6
