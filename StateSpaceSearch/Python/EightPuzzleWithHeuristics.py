'''EightPuzzleWithHeuristics.py
Yu Fu
Apr 22, 2015
CSE 415 Assignment 3 Part II / 4

A QUIET Solving Tool problem formulation of Eight Puzzle,
with Heuristic functions which can be used for A-star search.

QUIET = Quetzal User Intelligence Enhancing Technology.
The XML-like tags used here serve to identify key sections of this 
problem formulation.  

CAPITALIZED constructs are generally present in any problem
formulation and therefore need to be spelled exactly the way they are.
Other globals begin with a capital letter but otherwise are lower
case or camel case.
'''

import itertools
import math

#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Eight Puzzle with Heuristics"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Yu Fu']
PROBLEM_CREATION_DATE = "22-APR-2015"
PROBLEM_DESC=\
'''This formulation of the Eight Puzzle with Heuristics problem
uses generic Python 3 constructs and has been tested with Python 3.4.
It is designed to work according to the QUIET tools interface.
'''
#</METADATA>

#<COMMON_CODE>
def DEEP_EQUALS(s1, s2):
  if len(s1) != len(s2):
    return False
  for i in range(len(s1)):
    if s1[i] != s2[i]:
      return False
  return True

def DESCRIBE_STATE(state):
  # Produces a textual description of a state.
  # Might not be needed in normal operation with GUIs.
  txt = ""
  for i in range(N_size):
    for j in range(N_size):
      txt += str(state[i * N_size + j]) + " "
    txt += "\n"
  return txt

def HASHCODE(s):
  '''The result should be an immutable object such as a string
  that is unique for the state s.'''
  return str(s)

def h_euclidean(s):
  '''The sum of the euclidean distance for each tile from its
     location in state s to its location in the goal state.'''
  sum = 0
  for i in range(N_size * N_size):
    (p_goal_x, p_goal_y) = indexTo2D(s[i])
    (p_now_x, p_now_y) = indexTo2D(i)
    sum += (math.sqrt(math.pow(p_goal_x-p_now_x, 2) + math.pow(p_goal_y-p_now_y, 2)))
  return sum

def h_hamming(s):
  '''The number of tiles that, in state s, are not 
     where they should end up in the goal state.'''
  count = 0
  for i in range(N_size * N_size):
    if s[i] != i:
      count += 1
  return count     

def h_manhattan(s):
  '''Sum of for each tile, how rows it is away from 
     its goal state row plus how many columns it is 
     away from its goal state column.'''
  sum = 0
  for i in range(N_size * N_size):
    (p_goal_x, p_goal_y) = indexTo2D(s[i])
    (p_now_x, p_now_y) = indexTo2D(i)
    sum += (math.fabs(p_goal_x-p_now_x) + math.fabs(p_goal_y-p_now_y))
  return sum

def indexTo2D(i):
    return (i % N_size, i / N_size)

def copy_state(s):
  # Performs an appropriately deep copy of a state,
  # for use by operators in creating new states.
  return s[:]

def can_move(s, From, To):
  '''Tests whether it's legal to move a number in state s
     from the From position to To position.'''
  try:
    # From or To out of block boundary
    if From < 0 or From >= (N_size * N_size) or To < 0 or To >= (N_size * N_size):
      return False
    # Empty block in From position
    if s[From] == 0:
      return False
    # Not empty block in To position
    if s[To] != 0:
      return False
    # From position at leftmost side and trying to move left
    if From % N_size == 0 and To == From - 1:
      return False 
    # From position at rightmost side and trying to move right
    if From % N_size == N_size - 1 and To == From + 1:
      return False
    return True
  except (Exception) as e:
    print(e)

def move(s, From, To):
  '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the number
     from the From position to the To position (should be 0).'''
  new_s = copy_state(s) # start with a deep copy.
  new_s[To] = s[From]
  new_s[From] = s[To]
  return new_s # return new state

def goal_test(s):
  '''If the state equals to [0, 1, 2, 3, ...], 
     then s is the goal state.'''
  for i in range(N_size * N_size):
    if s[i] != i:
      return False
  return True

def goal_message(s):
  return "The Puzzle is solved!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

#</COMMON_CODE>

#<COMMON_DATA>
N_size = 3
#</COMMON_DATA>

#<INITIAL_STATE>
# puzzle0:
# CREATE_INITIAL_STATE = lambda : [0, 1, 2, 3, 4, 5, 6, 7, 8]
# puzzle1a:
# CREATE_INITIAL_STATE = lambda : [1, 0, 2, 3, 4, 5, 6, 7, 8]
# puzzle2a:
# CREATE_INITIAL_STATE = lambda : [3, 1, 2, 4, 0, 5, 6, 7, 8]
# puzzle4a:
# CREATE_INITIAL_STATE = lambda : [1, 4, 2, 3, 7, 0, 6, 8, 5]
#</INITIAL_STATE>

#<OPERATORS>
block_combinations = []
for p in range(N_size * N_size):
  block_combinations += [(p, p-1), (p, p+1), (p, p-N_size), (p, p+N_size)]
OPERATORS = [Operator("Move number from block " + str(p) + " to " + str(q),
                      lambda s,p=p,q=q: can_move(s,p,q),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s,p=p,q=q: move(s,p,q))
             for (p,q) in block_combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<STATE_VIS>
if 'BRYTHON' in globals():
 from TowersOfHanoiVisForBrython import set_up_gui as set_up_user_interface
 from TowersOfHanoiVisForBrython import render_state_svg_graphics as render_state
# if 'TKINTER' in globals(): from TicTacToeVisForTKINTER import set_up_gui
#</STATE_VIS>

HEURISTICS = {'h_euclidean': h_euclidean, 'h_hamming':h_hamming, 'h_manhattan':h_manhattan}