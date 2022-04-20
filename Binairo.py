from copy import deepcopy
import math
import random
import State
import Cell

def check_Adjancy_Limit(state: State):

    #check rows
    for i in range(0,state.size):
        for j in range(0,state.size-2):
            if(state.board[i][j].value.upper()==state.board[i][j+1].value.upper() and 
            state.board[i][j+1].value.upper()==state.board[i][j+2].value.upper() and
            state.board[i][j].value !='_'and 
            state.board[i][j+1].value !='_'and
            state.board[i][j+2].value !='_' ):
                
                return False
    #check cols
    for j in range(0,state.size): # cols
        for i in range(0,state.size-2): # rows
            if(state.board[i][j].value.upper()==state.board[i+1][j].value.upper() 
            and state.board[i+1][j].value.upper()==state.board[i+2][j].value.upper() 
            and state.board[i][j].value !='_'
            and state.board[i+1][j].value !='_'
            and state.board[i+2][j].value !='_' ):
               
                return False
    
    return True

def check_circles_limit(state:State): # returns false if number of white or black circles exceeds board_size/2
    #check in rows
    for i in range(0,state.size): # rows
        no_white_row=0
        no_black_row=0
        for j in range(0,state.size): # each col
            # if cell is black or white and it is not empty (!= '__')
            if (state.board[i][j].value.upper()=='W' and state.board[i][j].value != '_'): no_white_row+=1
            if (state.board[i][j].value.upper()=='B' and state.board[i][j].value != '_'): no_black_row+=1
        if no_white_row > state.size/2 or no_black_row > state.size/2:
            
            return False
        no_black_row=0
        no_white_row=0

    # check in cols
    for j in range(0,state.size):#cols
        no_white_col=0
        no_black_col=0
        for i in range(0,state.size): # each row
            # if cell is black or white and it is not empty (!= '__')
            if (state.board[i][j].value.upper()=='W' and state.board[i][j].value != '_'): no_white_col+=1
            if (state.board[i][j].value.upper()=='B' and state.board[i][j].value != '_'): no_black_col+=1
        if no_white_col > state.size/2 or no_black_col > state.size/2:
            
            return False
        no_black_col=0
        no_white_col=0
    
    return True

def is_unique(state:State): # checks if all rows are unique && checks if all cols are unique
    # check rows
    for i in range(0,state.size-1):
        for j in range(i+1,state.size):
            count = 0
            for k in range(0,state.size):
                if(state.board[i][k].value.upper()==state.board[j][k].value.upper()
                and state.board[i][k].value!='_'
                and state.board[j][k].value!='_'):
                    count+=1
            if count==state.size:
                
                return False
            count=0

    # check cols
    for j in range(0,state.size-1):
        for k in range(j+1,state.size):
            count_col =0 
            for i in range(0,state.size):
                 if(state.board[i][j].value.upper()==state.board[i][k].value.upper()
                 and state.board[i][j].value != '_'
                 and state.board[i][k].value != '_' ):
                    count_col+=1
            if count_col == state.size:
               
                return False
            count_col=0 
   
    return True

def is_assignment_complete(state:State): # check if all variables are assigned or not
    for i in range(0,state.size):
        for j in range(0,state.size):
            if(state.board[i][j].value == '_'): # exists a variable wich is not assigned (empty '_')
                
                return False

    
    return True

def is_consistent(state:State):
    
    return check_Adjancy_Limit(state) and check_circles_limit(state) and is_unique(state)

def check_termination(state:State):
    return is_consistent(state) and is_assignment_complete(state)

def backtrack(state: State):
    return recursive_backtrack(state)

def recursive_backtrack(state: State):
    if is_assignment_complete(state):
        state.print_board()
        return
    
    # get next unassigned variable
    # cell = select_unassigned_variable(state)
    cell = mrv(state)
    
    for value in cell.domain:
        cell.value = value
        if is_consistent(state):
            newState = deepcopy(state)
            if forward_checking(newState, cell.x, cell.y):
                recursive_backtrack(newState)
    
    
def select_unassigned_variable(state: State) -> Cell:
    for i in reversed(state.board):
        for j in reversed(i):
            if j.value == '_':
                return j
    return None

def mrv(state: State) -> Cell:
    min = 1000000
    selectedCell = None
    
    for aRow in state.board:
        for aCell in aRow:
            if aCell.value == '_' and len(aCell.domain) < min:
                selectedCell = aCell
                min = len(aCell.domain)            
            
    return selectedCell

def forward_checking(state: State, i: int, j: int) -> bool:
    randomNumber = random.randint(1, 3)
    
    if randomNumber % 3 == 0:
        for index in range(i, state.size):
            for jIndex in range(j, state.size):
                if state.board[index][jIndex] == '_':
                    for value in state.board[index][jIndex].domain:
                        state.board[index][jIndex].value = value
                        if not is_consistent(state):
                            state.board[index][jIndex].domain.remove(value)
                        if len(state.board[index][jIndex].domain) == 0:
                            return False
                        elif len(state.board[index][jIndex].domain) == 1:
                            state.board[index][jIndex].value = state.board[index][jIndex].domain[0]
                        else:
                            state.board[index][jIndex].value = '_'
        return True
    else: return True
