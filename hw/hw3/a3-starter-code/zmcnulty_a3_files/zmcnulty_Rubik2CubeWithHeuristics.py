'''
Zachary McNulty

zmcnulty_Rubik2CubeWithManhattan.py

usage:
    python3 zmcnulty_AStar.py zmcnulty_Rubik2CubeWithManhattan [# moves to shuffle cube with]

    This is a problem formulation for a 2 x 2 x 2 Rubik cube. It implements a
    heuristic and is thus compatible with A* Search. This heuristic is sort of
    a Manhattan heuristic extended to the Rubik cube: it counts the number of faces
    away each individual block face is from the cube face of its same color. i.e.
    this distance is either 0, 1, or 2. 0 = on the correct cube face already, 2 = on
    the cube face directly opposite correct face, 1 = any other cube face.

'''



from zmcnulty_Rubik2Cube import *


# Heuristic: count the number of turns each color is from its
# optimal face


def h(S):
      state_str = "".join([c for c in str(S) if c.isdigit()])
      up = list(state_str[:4])
      front = list(state_str[4:6])
      right = list(state_str[6:8])
      back = list(state_str[8:10])
      left = list(state_str[10:12])
      front.extend(state_str[12:14])
      right.extend(state_str[14:16])
      back.extend(state_str[16:18])
      left.extend(state_str[18:20])
      down = list(state_str[20:])
    
      count = 0

      # count colors two faces away from destination once (they get counted again in next step)
      count += (up.count('4')+ down.count('1')+ front.count('5')+ back.count('0')+ left.count('2')+ right.count('3'))

      # count colors one face away from destination
      count += 24 - (up.count('1')+ down.count('4')+ front.count('0')+ back.count('5')+ left.count('3')+ right.count('2'))
      
      return count

