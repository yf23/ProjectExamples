'''Sudoku.py
A QUIET Solving Tool problem formulation.
QUIET = Quetzal User Intelligence Enhancing Technology.
The XML-like tags used here serve to identify key sections of this 
problem formulation.  

CAPITALIZED constructs are generally present in any problem
formulation and therefore need to be spelled exactly the way they are.
Other globals begin with a capital letter but otherwise are lower
case or camel case.
'''
#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Sudoku"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Yu Fu', 'Yinghe Chen']
PROBLEM_CREATION_DATE = "28-APR-2015"
PROBLEM_DESC=\
'''This formulation of the Sudoku problem uses generic
Python 3 constructs and has been tested with Python 3.4.
It is designed to work according to the QUIET tools interface.
'''
#</METADATA>

#<COMMON_CODE>
def DEEP_EQUALS(s1, s2):
    num_of_index = size_of_sudoku * size_of_sudoku
    for i_b in range(num_of_index):
        for i_c in range(num_of_index):
            if s1[i_b][i_c] != s2[i_b][i_c]:
                return False
    return True

def DESCRIBE_STATE(state):
    # Produces a textual description of a state.
    # Might not be needed in normal operation with GUIs.
    txt = "\n"
    block_divider = ""
    for i in range(2 * size_of_sudoku * size_of_sudoku - 1):
        block_divider += "-"
    block_divider += "\n"
    row_count = 0
    for x in range(size_of_sudoku * size_of_sudoku):
        if row_count != 0 and row_count % size_of_sudoku == 0:
            txt += block_divider
        row = get_row(state, x)
        ind_count = 0
        for a in row:
            ind_count += 1
            div = " "
            if ind_count % size_of_sudoku == 0 \
               and ind_count / size_of_sudoku != size_of_sudoku:
                div = "|"
            if a == 0:
                txt += " " + div
            else:
                txt += str(a) + div
        txt += "\n"
        row_count += 1
    return txt

def HASHCODE(s):
    '''The result should be an immutable object such as a string
    that is unique for the state s.'''
    return str(s)

def h_euclidean(s):
    constraint_level = 0
    for i in range(size_of_sudoku * size_of_sudoku):
        count1 = 0
        count2 = 0
        col = get_col(s, i)
        row = get_row(s, i)
        for j in range (len(col)):
            if (col[j] == 0):
                count1 += 1
        for k in range (len(row)):
            if (row[k] == 0):
                count2 += 1
        constraint_level += count1 * count1 + count2 * count2
    return constraint_level

def h_remaining(s):
    '''Return the sum of remaining numbers have not been put into the sudoku.'''
    goal_sum = sum([x + 1 for x in range(size_of_sudoku * size_of_sudoku)])\
               * size_of_sudoku * size_of_sudoku
    s_sum = 0
    for block in s:
        for cell in block:
            s_sum += cell
    return goal_sum - s_sum

def copy_state(s):
    '''Performs an appropriately deep copy of a state,
       for use by operators in creating new states.'''
    news = []
    for x in range(size_of_sudoku * size_of_sudoku):
        news.append([])
    for i in range(size_of_sudoku * size_of_sudoku):
        news[i]=s[i][:]
    return news

def can_add(s, num, index_of_block, index_of_cell):
    '''Tests whether it's legal to add a number in 
       given cell inside given block.'''
    # Test if given number is valid.
    if num > size_of_sudoku * size_of_sudoku and num < 1:
        return False
    # Test if it is a empty cell in given position.
    if s[index_of_block][index_of_cell] != 0:
        return False
    # Test if there is repeat numbers in the same row, column and block
    coordinate = get_coordinate(index_of_block, index_of_cell)
    col = coordinate[0]
    row = coordinate[1]
    num_col = get_col(s, col)
    num_row = get_row(s, row)
    num_block = get_block(s, index_of_block)
    num_col[row] = num
    num_row[col] = num
    num_block[index_of_cell] = num
    if repeat_test(num_col) or repeat_test(num_row) or repeat_test(num_block):
        return False
    else:
        return True

def add(s, num, index_of_block, index_of_cell):
    '''Assuming it's legal to add the number, this computes
       the new state resulting from adding the number to
       given cell inside given block.'''
    news = copy_state(s)                          # Start with a deep copy
    news[index_of_block][index_of_cell] = num     # Add the number to new state
    return news                                   # Return new state

def goal_test(s):
    '''If there is no zeros in the given state then it's a goal.'''
    for block in s:
        for cell in block:
            if cell == 0:
                return False
    return True

def goal_message(s):
    return "The Sudoku is solved!"

def repeat_test(l):
    '''If the given list has repeat numbers other than 0.
       Return True if there is any repeat.'''
    listOfCount = [0] * size_of_sudoku * size_of_sudoku
    for i in l:
        if i > 0:
            listOfCount[i - 1] += 1
    for j in listOfCount:
        if j > 1:
            return True
    return False

def get_row(s, row):
    '''Return a list of numbers in the given row.'''
    block_list = [x + size_of_sudoku * int(row / size_of_sudoku) for x in range(size_of_sudoku)]
    index_list = [x + size_of_sudoku * int(row % size_of_sudoku) for x in range(size_of_sudoku)]
    nums = []
    for i in block_list:
        for j in index_list:
            nums.append(s[i][j])
    return nums

def get_col(s, col):
    '''Return a list of numbers in the given column.'''
    init_ind = []
    for i in range(size_of_sudoku):
        init_ind.append(size_of_sudoku * i)
    block_list = [x + int(col / size_of_sudoku) for x in init_ind]
    index_list = [x + int(col % size_of_sudoku) for x in init_ind]
    nums = []
    for i in block_list:
        for j in index_list:
            nums.append(s[i][j])
    return nums

def get_block(s, block):
    '''Return a list of number in the given block.'''
    return s[block][:]

def get_coordinate(index_of_block, index_of_cell):
    '''Return the coordinate of given index of block
       and index of cell.'''
    x_cell = int(index_of_cell % size_of_sudoku)
    y_cell = int(index_of_cell / size_of_sudoku)
    x_block = int(index_of_block % size_of_sudoku)
    y_block = int(index_of_block / size_of_sudoku)
    x = x_block * size_of_sudoku + x_cell
    y = y_block * size_of_sudoku + y_cell
    return (x, y)

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
size_of_sudoku = 3
#</COMMON_DATA>

#<INITIAL_STATE>
# answer is
# 1 4 5 |3 2 7 |6 9 8 
# 8 3 9 |6 5 4 |1 2 7 
# 6 7 2 |9 1 8 |5 4 3 
# ------+------+------
# 4 9 6 |1 8 5 |3 7 2 
# 2 1 8 |4 7 3 |9 5 6 
# 7 5 3 |2 9 6 |4 8 1 
# ------+------+------
# 3 6 7 |5 4 2 |8 1 9 
# 9 8 4 |7 6 1 |2 3 5 
# 5 2 1 |8 3 9 |7 6 4 
CREATE_INITIAL_STATE = lambda : [[1, 4, 5, 0, 3, 9, 6, 7, 2],\
                                 [3, 0, 7, 6, 5, 4, 9, 1, 8],\
                                 [6, 0, 8, 1, 2, 7, 5, 4, 3],\
                                 [4, 9, 6, 2, 1, 8, 7, 5, 3],\
                                 [1, 8, 5, 4, 7, 3, 2, 9, 6],\
                                 [3, 7, 2, 9, 5, 6, 4, 8, 1],\
                                 [3, 0, 7, 9, 0, 4, 5, 2, 1],\
                                 [5, 4, 2, 7, 6, 0, 8, 3, 9],\
                                 [8, 1, 9, 2, 3, 5, 7, 6, 0]]
#</INITIAL_STATE>

#<OPERATORS>
move_combinations = []
for i_b in range(size_of_sudoku * size_of_sudoku):
    for i_c in range(size_of_sudoku * size_of_sudoku):
        for num in range(size_of_sudoku * size_of_sudoku):
            move_combinations.append([num + 1, i_b, i_c])

OPERATORS = [Operator("Add number " + str(comb[0]) + " to block " + str(comb[1]) + ", cell " + str(comb[2]),
                      lambda s, num=comb[0], ib=comb[1], ic=comb[2]: can_add(s, num, ib, ic),
                      lambda s, num=comb[0], ib=comb[1], ic=comb[2]: add(s, num, ib, ic))
             for comb in move_combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<STATE_VIS>
def render_state(s):
    return DESCRIBE_STATE(s)
#</STATE_VIS>

HEURISTICS = {'h_remaining': h_remaining, 'h_euclidean': h_euclidean}