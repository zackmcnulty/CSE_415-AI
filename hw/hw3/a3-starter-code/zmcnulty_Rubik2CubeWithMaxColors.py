
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
   
    return max([len(front), len(back), len(right), len(left), len(up), len(down)]) - 1
