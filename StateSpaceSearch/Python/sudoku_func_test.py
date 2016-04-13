def h_remaining(s):
    sum = 0
    for ib in range(size_of_sudoku * size_of_sudoku):
        for ic in range(size_of_sudoku * size_of_sudoku):
            choice_list = [x + 1 for x in range(size_of_sudoku * size_of_sudoku)]
            (row, col) = get_coordinate(ib, ic)
            exist_list = get_col(s, col) + get_row(s, row) + get_block(s, ib)
            for x in exist_list:
                try:
                    choice_list.remove(x)
                except ValueError:
                    pass
            h_value = len(choice_list)
            sum += h_value
    return sum

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

def can_add(s, num, index_of_block, index_of_cell):
    '''Tests whether it's legal to add a number in 
       given cell with index2 in block with index1.'''
    # Test if given number is valid.
    if num > size_of_sudoku * size_of_sudoku and num < 1:
        raise ValueError('Input number out of range.')
    # Test if it is a empty cell in given position.
    if s[index_of_block][index_of_cell] != 0:
        raise ValueError('The given cell is not empty.')
    # Test if there is repeat numbers in the same row, column and block
    coordinate = get_coordinate(index_of_block, index_of_cell)
    col = coordinate[0]
    row = coordinate[1]
    num_col = get_col(s, col)
    num_row = get_row(s, row)
    num_block = get_block(s, index_of_block)
    print(num_col)
    print(num_row)
    print(num_block)
    num_col[row] = num
    num_row[col] = num
    num_block[index_of_cell] = num
    print(num_col)
    print(num_row)
    print(num_block)
    if repeat_test(num_col) or repeat_test(num_row) or repeat_test(num_block):
        return False
    else:
        return True

def copy_state(s):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = []
    for x in range(size_of_sudoku * size_of_sudoku):
        news.append([])
    for i in range(size_of_sudoku * size_of_sudoku):
        news[i]=s[i][:]
    return news

def goal_test(s):
    '''If there is no zeros in the given state then it's a goal.'''
    for block in s:
        for cell in block:
            if cell == 0:
                return False
    return True

size_of_sudoku = 3

s=[[5, 3, 1, 6, 2, 4, 0, 9, 8],\
                                 [2, 7, 4, 1, 9, 5, 3, 0, 0],\
                                [0, 0, 0, 3, 0, 7, 1, 6, 2],\
                                 [8, 1, 2, 4, 5, 6, 7, 0, 3],\
                             [5, 6, 0, 8, 0, 3, 0, 2, 1],\
                                 [4, 0, 3, 0, 2, 1, 5, 0, 6],\
                                 [1, 6, 0, 2, 0, 0, 3, 4, 5],\
                                 [0, 3, 0, 4, 1, 9, 6, 8, 2],\
                                 [2, 8, 4, 6, 3, 5, 0, 7, 9]]

print(h_remaining(s))
