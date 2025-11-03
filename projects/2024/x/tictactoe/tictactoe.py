"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    The first player is X. The implementation is correct as per the test cases.
    """
    #raise NotImplementedError
    count_X = 0
    count_O = 0
    
    for row in board:
        for cell in row:
            if cell == X:
                count_X += 1
            elif cell == O:
                count_O += 1
    return X if count_O >= count_X else O
        


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #raise NotImplementedError
    #if terminal(board):
    #    return set()
    possible_actions = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    
    if terminal(board):
        return i, j
    return possible_actions




def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    i, j = action
    if not (0 <= i < len(board) and 0 <= j < len(board[0])):
        raise ValueError("Action out of bounds")
    
    if board[i][j] != EMPTY:
        raise ValueError("Cell is not empty")

    if player(board)==X:
        board_copy[i][j] = X
    else:
        board_copy[i][j] = O
    
    return board_copy
    

def check_winner(seq: list):
    if len(set(seq)) == 1:
        return seq[0]
    return None

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #raise NotImplementedError
    #1st row
    n = len(board)
    for row in board:
        result = check_winner(row)
        if result:
            return result
    
    for i in range(n):
        col = []
        for j in range(n):
            col.append(board[j][i])
        result = check_winner(col) 
        if result:
            return result
            
    diagonal = []
    anti_diagonal = []
    for i in range(n):
        diagonal.append(board[i][i])
        anti_diagonal.append(board[i][n - 1 - i])
        
    result = check_winner(diagonal) 
    if result:
        return result
    result = check_winner(anti_diagonal)
    if result: 
        return result
    return None




def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #raise NotImplementedError
    if winner(board):
        return True
    unnested_board = set()
    for row in board:
        for cell in row:
            unnested_board.add(cell)
    if EMPTY not in unnested_board:
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #raise NotImplementedError
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def max_value(board, alpha, beta):
    v = -float('inf')
    if terminal(board): # base case
        return utility(board), None, None
    
    for action in actions(board):
        max_node_val = min_value(result(board, action), alpha, beta)[0]
        if v < max_node_val:
            v = max_node_val
            i, j = action
            
            # beta cut-off
            alpha = max(alpha, v)
            if beta <= alpha:
                break
            
    return v, i, j

def min_value(board, alpha, beta):
    v = float('inf')
    if terminal(board): # base case
        return utility(board), None, None
    
    for action in actions(board):
        min_node_val = max_value(result(board, action), alpha, beta)[0]
        if v > min_node_val:
            v = min_node_val
            i, j = action
            
            # alpha cut-off
            beta = min(beta, v)
            if beta <= alpha:
                break
            
            
    return v, i, j



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #raise NotImplementedError
    if terminal(board):
        return None
    
    if player(board) == X:
        v, i, j = max_value(board, alpha=-float('inf'), beta=float('inf'))
        return i, j 
    else:
        v, i, j = min_value(board, alpha=-float('inf'), beta=float('inf')) 
        return i, j