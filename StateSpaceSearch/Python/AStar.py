'''AStar.py 
Yu Fu
Apr 22, 2015
CSE 415 Assignment 3 Part II / 3

A-Star Search of a problem space.
The Problem should be given in a separate Python
file using the "QUIET" file format.

AStar.py will accept three arguments:
The first argument is the name of a problem template.
The second argument is the name of a heuristic evaluation function.
The third argument is the name of a puzzle instance file
that contains a particular initial state.

Examples of Usage:
python3 AStar.py EightPuzzleWithHeuristics h_euclidean puzzle2a.py
'''

import sys
import queue as Q

if len(sys.argv) < 4:
  print("Invalid number of arguments")

import importlib
Problem = importlib.import_module(sys.argv[1])

IS_filename = sys.argv[3].split(".")[0]
IS = importlib.import_module(IS_filename)

print("\nWelcome to A-Star Search with heuristic function " + sys.argv[2])
COUNT = None
BACKLINKS = {}

def heuristic(s):
  if sys.argv[2] == "h_euclidean":
    return Problem.h_euclidean(s)
  elif sys.argv[2] == "h_hamming":
    return Problem.h_hamming(s)
  elif sys.argv[2] == "h_manhattan":
    return Problem.h_manhattan(s)
  else:
    print("Incorrect heuristic function input")
    return

def runAstar():
  initial_state = IS.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(Problem.DESCRIBE_STATE(initial_state))
  global COUNT, BACKLINKS
  COUNT = 0
  BACKLINKS = {}
  Astar(initial_state)
  print(str(COUNT)+" states examined.")

def Astar(initial_state):
  global COUNT, BACKLINKS

  OPEN_PQ = Q.PriorityQueue()
  OPEN_PQ.put((heuristic(initial_state), initial_state))
  OPEN_LIST = []
  OPEN_LIST.append(initial_state)
  CLOSED = []
  BACKLINKS[Problem.HASHCODE(initial_state)] = -1

  while OPEN_LIST != []:
    S_tuple = OPEN_PQ.get()
    S = S_tuple[1]
    step = S_tuple[0] - heuristic(S)

    OPEN_LIST.remove(S)
    CLOSED.append(S)

    if Problem.GOAL_TEST(S):
      print(Problem.GOAL_MESSAGE_FUNCTION(S))
      print("COUNT = "+str(COUNT))
      print("len(OPEN)="+str(len(OPEN_LIST)))
      print("len(CLOSED)="+str(len(CLOSED)))
      backtrace(S)
      return

    COUNT += 1
    if (COUNT % 32)==0:
       print(".",end="")
       if (COUNT % 128)==0:
         print("COUNT = "+str(COUNT))
         print("len(OPEN)="+str(len(OPEN_LIST)))
         print("len(CLOSED)="+str(len(CLOSED)))

    L = []
    for op in Problem.OPERATORS:
      # Optionally uncomment the following when debugging
      # a new problem formulation.
      #print("Trying operator: " + op.name)
      if op.precond(S):
        new_state = op.state_transf(S)
        #print(Problem.DESCRIBE_STATE(new_state))
        if not occurs_in(new_state, CLOSED):
          L.append(new_state)
          BACKLINKS[Problem.HASHCODE(new_state)] = S
          # Uncomment for debugging:
          #print(Problem.DESCRIBE_STATE(new_state))

    repeat = -1
    for i in range(len(L)):
      for j in range(len(OPEN_LIST)):
        if Problem.DEEP_EQUALS(L[i], OPEN_LIST[j]):
          repeat = i; break
    if repeat != -1:
      del L[repeat]

    for s2 in L:
      OPEN_PQ.put((step+1+heuristic(s2), s2))

    OPEN_LIST = OPEN_LIST + L


def backtrace(S):
  global BACKLINKS

  path = []
  while not S == -1:
    path.append(S)
    S = BACKLINKS[Problem.HASHCODE(S)]
  path.reverse()
  print("Solution path (length = " + str(len(path)-1) + "):")
  for s in path:
    print(Problem.DESCRIBE_STATE(s))
  return path    
  
def occurs_in(s1, lst):
  for s2 in lst:
    if Problem.DEEP_EQUALS(s1, s2): return True
  return False

if __name__=='__main__':
  runAstar()
