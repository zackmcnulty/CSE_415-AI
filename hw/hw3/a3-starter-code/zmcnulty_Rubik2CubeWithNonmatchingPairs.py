'''
The idea is count the number of horizontal pairs that don't match in color
'''


from zmcnulty_Rubik2Cube import *

# NOT admissable

def h(S):
    state_str = "".join([c for c in str(S) if c.isdigit()])

    nonmatching_pairs = 0
    for pair in zip(state_str[::2], state_str[1::2]):
        if pair[0] != pair[1]:
            nonmatching_pairs += 1

    return nonmatching_pairs

