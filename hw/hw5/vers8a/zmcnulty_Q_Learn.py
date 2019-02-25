'''zmcnulty_Q_Learn.py

Rename this file using your own UWNetID, and rename it where it is imported
in TOH_MDP.py 
Implement Q-Learning in this file by completing the implementations
of the functions whose stubs are present.
Add or change code wherever you see #*** ADD OR CHANGE CODE HERE ***

This is part of the UW Intro to AI Starter Code for Reinforcement Learning.

'''

import numpy as np

# Edit the returned name to ensure you get credit for the assignment.
def student_name():
   return "McNulty, Zachary" # For an autograder.

STATES=None; ACTIONS=None; UQV_callback=None; Q_VALUES=None
is_valid_goal_state=None; Terminal_state = None
USE_EXPLORATION_FUNCTION = None
INITIAL_STATE = None
def setup(states, actions, q_vals_dict, update_q_value_callback,\
    goal_test, terminal, use_exp_fn=False):
    '''This method is called by the GUI the first time a Q_Learning
    menu item is selected. It may be called again after the user has
    restarted from the File menu.
    Q_VALUES starts out with all Q-values at 0.0 and a separate key
    for each (s, a) pair.'''
    global STATES, ACTIONS, UQV_callback, Q_VALUES, is_valid_goal_state
    global USE_EXPLORATION_FUNCTION, Terminal_state
    STATES = states
    ACTIONS = actions
    Q_VALUES = q_vals_dict
    UQV_callback = update_q_value_callback
    is_valid_goal_state = goal_test
    Terminal_state = terminal
    USE_EXPLORATION_FUNCTION = use_exp_fn

    if USE_EXPLORATION_FUNCTION:
#*** ADD OR CHANGE CODE HERE ***
         # Change this if you implement an exploration function:
         print("You have not implemented an exploration function")

PREVIOUS_STATE = None
LAST_ACTION = None
def set_starting_state(s):
    '''This is called by the GUI when a new episode starts.
    Do not change this function.'''
    global INITIAL_STATE, PREVIOUS_STATE
    print("In Q_Learn, setting the starting state to "+str(s))
    INITIAL_STATE = s
    PREVIOUS_STATE = s

ALPHA = 0.5
CUSTOM_ALPHA = False
EPSILON = 0.5
CUSTOM_EPSILON = False
GAMMA = 0.9
def set_learning_parameters(alpha, epsilon, gamma):
    ''' Called by the system. Do not change this function.'''
    global ALPHA, EPSILON, CUSTOM_ALPHA, CUSTOM_EPSILON, GAMMA
    ALPHA = alpha
    EPSILON = epsilon
    GAMMA = gamma
    if alpha < 0: CUSTOM_ALPHA = True
    else: CUSTOM_ALPHA = False
    if epsilon < 0: CUSTOM_EPSILON = True
    else: CUSTOM_EPSILON = False

def update_Q_value(previous_state, previous_action, new_value):
    '''Whenever your code changes a value in Q_VALUES, it should
    also call this method, so the changes can be reflected in the
    display.
    Do not change this function.'''
    UQV_callback(previous_state, previous_action, new_value)

# NOTE: Have to use the "Show Q values" option for the update to be shown
def handle_transition(action, new_state, r):
    '''When the user drives the agent, the system will call this function,
    so that you can handle the learning that should take place on this
    transition.'''
    global PREVIOUS_STATE, ALPHA, GAMMA, Q_VALUES

#*** ADD OR CHANGE CODE HERE ***
    
    new_value = (1 - ALPHA)*Q_VALUES[(PREVIOUS_STATE, action)] + ALPHA * (r + GAMMA * max([Q_VALUES[(new_state, a_prime)] for a_prime in ACTIONS]))

    Q_VALUES[(PREVIOUS_STATE, action)] = new_value

    # You should call update_Q_value before returning.  E.g.,
    update_Q_value(PREVIOUS_STATE, action, new_value)
    
    PREVIOUS_STATE = new_state
    return # Nothing needs to be returned.

def choose_next_action(s, r, terminated=False):
     '''When the GUI or engine calls this, the agent is now in state s,
     and it receives reward r.
     If terminated==True, it's the end of the episode, and this method
      can just return None after you have handled the transition.

     Use this information to update the q-value for the previous state
     and action pair.  
     
     Then the agent needs to choose its action and return that.

     '''
     global INITIAL_STATE, PREVIOUS_STATE, LAST_ACTION, Q_VALUES
     global EPSILON, ALPHA
     # Unless s is the initial state, compute a new q-value for the
     # previous state and action.
     if not (s==INITIAL_STATE):
         # Compute your update here.
         # if CUSTOM_ALPHA is True, manage the alpha values over time.
         # Otherwise go with the fixed value.
#*** ADD OR CHANGE CODE HERE ***

         if CUSTOM_ALPHA:
             ALPHA = max(0.5, 1 - len([q for q in Q_VALUES if Q_VALUES[q] == 0]) / len(Q_VALUES))
         
         handle_transition(LAST_ACTION, s, r)
         
     # Now select an action according to your Q-Learning criteria, such
     # as expected discounted future reward vs exploration.
     if terminated: return None

     if USE_EXPLORATION_FUNCTION:
         # Change this if you implement an exploration function:
#*** ADD OR CHANGE CODE HERE ***
         print("You have not implemented an exploration function")

     # If EPSILON > 0, or CUSTOM_EPSILON is True,
     # then use epsilon-greedy learning here.
     # In order to access q-values, simply get them from the dictionary, e.g.,
     # some_qval = Q_VALUES[(some_state, some_action)]
     elif EPSILON > 0 or CUSTOM_EPSILON:
         
         # If we have a time-varying epislon, update the Epsilon value
         # want a compromise between exploration and exploitation
         # This function simply counts the fraction of unknown/unvisited states
         # and uses that as epsilon
         # lots of unknown Q vals = high epsilon = high exploration
         if CUSTOM_EPSILON:
            EPSILON = len([q for q in Q_VALUES if Q_VALUES[q] == 0]) / len(Q_VALUES)

         if is_valid_goal_state(s): next_action = 'Exit'
         elif np.random.rand() < EPSILON:
             # act randomly
             next_action = np.random.choice([a for a in ACTIONS if not a == 'Exit'])
         else:
             # follow policy
             extract_policy([s], ACTIONS)
             next_action = Policy[s]


#*** ADD OR CHANGE CODE HERE ***     
     LAST_ACTION = next_action # remember this for next time
     PREVIOUS_STATE = s        #    "       "    "   "    "
     return next_action

Policy = {}
def extract_policy(S, A):
   '''Return a dictionary mapping states to actions. Obtain the policy
   using the q-values most recently computed.
   Ties between actions having the same (s, a) value can be broken arbitrarily.
   Reminder: goal states should map to the Exit action, and no other states
   should map to the Exit action.
   '''
   global Policy, Q_VALUES
   #Policy = {}
#*** ADD OR CHANGE CODE HERE ***     
   
   for s in S:
       if is_valid_goal_state(s):
            Policy[s] = 'Exit'
       elif s == Terminal_state:
            Policy[s] = None
       else:
            Policy[s] = max([a for a in A if not a == 'Exit'], key=lambda a: Q_VALUES[(s,a)])

   return Policy
