'''zmcnulty_Farmer_Fox.py
by Zachary McNulty
Assignment 2, in CSE 415, Winter 2019.
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

#<METADATA>
# necessary or not?
#</METADATA>

#<COMMONDATA>
#</COMMONDATA>

#<COMMONCODE>

LEFT = 0 # index location storing objects on left side
RIGHT = 1 # index location storing objects on right side
abbr_converter = {"F":"Farmer", "f":"fox", "c":"chicken", "g", "grain", "":"nothing"}

class State:

    def __init__(self, start_state = None):
        if start_state = None:
            start_state = ["Fcfg", ""]

        # Keeps track of objects on each side of river:
        # left side = state[0], right side = state[1]

        # self.state always stores letters/objects for each side in
        # sorted order according to sorted(object)
        self.state = start_state

    def __eq__(self, other):
        if self.state[LEFT] != other.state[LEFT] or self.state[RIGHT] != other.state[RIGHT]:
            return False
        else:
            return True

    def __str__(self):
        txt = "\nObjects on the left bank: " + " ".join([ abbr_converter[o] for o in self.state[LEFT] ]) + "\n"
        txt += "Objects on the right bank: " + " ".join([ abbr_converter[o] for o in self.state[RIGHT] ]) + "\n" 
        return txt 

    def __hash__(self):
       return (self.__str__()).__hash__() 

    def copy(self):
        copy = State()
        copy.state[LEFT] = self.state[LEFT]
        copy.state[RIGHT] = self.state[RIGHT]
        return copy

    # objects = what objects to move
    # direction = what direction to move them (i.e. 0 take from the left bank and move to the right)
    def can_move(self, objects, direction):

        # all objects we aim to move must be on the side we move them from
        for obj in objects:
            if obj not in self.state[direction]:
                return False
        else:
            return True 

    # objects = string of the abbreviated objects to move across river: i.e. Fcg = move Farmer, chicken, and grain
    # direction = which way to move across river : 0 -> move left to right, 1 -> move right to left
    def move(self, objects, direction):
        # remove from this side
        self.state[direction] = "".join(sorted([o for o in self.state[direction] if o not in objects))

        # and place on other side of river
        self.state[1-direction] = "".join(sorted(self.state[1-direction] + objects]))


# where s is a State
def goal_test(s):
    '''
    If all the objects are on the RIGHT, then we are in a goal state.
    '''
    if len(self.state[LEFT]) == 0:
        return True

def goal_message(s):
    return "Congratulations on keeping your chicken alive and unfed!"





class Operator:

    # name is a string that uniquely defines operator
    # precondition is a function that evaluates true or false base on State
    # state_change is a function that defines how the operator changes the state (if valid)
    def  __init__(self, name, precond, state_change):
        self.name = name
        self.precond = precond
        self.state_change = state_change

    # s is a State; checks if operator valid in current state
    def is_applicable(self, s):
        return self.precond(s)

    # s is a State; applys operator to given state and returns new state
    def apply(self, s):
        return self.state_change(s)

#</COMMONCODE>


#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State()
#<\INITIAL_STATE>

#<OPERATORS>
possible_moves = ["F", "Fc", "Fg", "Ff"]

OPERATORS = [Operator(
    # string definition
    "Move the " + " and the ".join([abbr_converter[o]] for o in move) + "from the " + direction[0] + " to the " + direction[1] "side of the river."
    
    # precondition
    lambda s, d=int(direction[0] == "right"): s.can_move(move, d)

    # move
    lambda s, d=int(direction[0] == "right"): s.move(move, d)
    )
        
    for move in possible_moves for direction in [("left", "right"), ("right", "left")]]

#<\OPERATORS>

#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
