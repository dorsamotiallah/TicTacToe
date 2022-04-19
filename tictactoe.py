import math
import random
import copy

board = [[ ' ' for i in range(3) ] for j in range(3)]
turn = True #computer turn 

def show_board():
    for b in range(len(board)):
        print(f' {board[b][0]} '+'|'+f' {board[b][1]} '+'|'+f' {board[b][2]} ')
        if(b<2):
            print('-'*11)
            
def intro():
    print('TIC-TAC-TOE')
    print('cell numbers are like below during game you are gonna be asked for the cell you wanna put your symbol,please use these indexes.')
    for b in range(len(board)):
        print(f' {1+b*3} '+'|'+f' {2+b*3} '+'|'+f' {3+b*3} ')
        if(b<2):
            print('-'*11)
    print("your symbol is 'O'")
    print("ENJOY LOSING HAHAHAHA...")
    print('*'*24)

def human_plays():
    global board
    inp = int(input("it's your turn, please insert number of your move: "))
    row = 0
    col = 0
    while(not (1<=inp<=9)):
        inp = int(input("ValueError,please insert a valid move: "))
    if(1<=inp<=3):
        row = 0
    elif(4<=inp<=6):
        row = 1
    elif(7<=inp<=9):
        row = 2

    if(inp%3 == 0):
       col = 2
    elif(inp%3 == 2):
        col = 1
    else:
        col = 0
        
    while(board[row][col]== 'X'):
        inp = int(input("you can not move to where your opponent is,please insert your move again: "))
        
        if(1<=inp<=3):
            row = 0
        elif(4<=inp<=6):
            row = 1
        elif(7<=inp<=9):
            row = 2

        if(inp%3 == 0):
           col = 2
        elif(inp%3 == 2):
            col = 1
        else:
            col = 0
        
    while(board[row][col]== 'O'):
        inp = int(input("You can not have two symbol at one cell, please insert a valid move: "))
        if(1<=inp<=3):
            row = 0
        elif(4<=inp<=6):
            row = 1
        elif(7<=inp<=9):
            row = 2

        if(inp%3 == 0):
           col = 2
        elif(inp%3 == 2):
            col = 1
        else:
            col = 0
    
    board[row][col] = 'O'

def computer_plays():
    global board
    if(board_empty(board)):
        corners=[1,3,7,9]
        init =0 
        init = random.choice(corners)
        if(init == 1):
            board[0][0] = 'X'
        elif(init == 3):
            board[0][2] = 'X'
        elif(init == 7):
            board[2][0] = 'X'
        elif(init == 9):
            board[2][2] = 'X'
    else:
        v = - math.inf
        best_move = (-1,-1)
        for child in children(board):#child is a tuple of i,j as indexes
            board[child[0]][child[1]] = 'X'
            thisvalue = alpha_beta_pruning_minmax(board,-math.inf,math.inf,False)#child is minimizing
            board[child[0]][child[1]] = ' '
            if(thisvalue > v):
                v = thisvalue
                best_move = child
        board[best_move[0]][best_move[1]] = 'X'


    
def children(state):# if player == True it means it's computer
    #without any smart order ////  
    res = []
    for i in range(3):
        for j in range(3):
            if(state[i][j] == ' '):
                res.append((i,j))
    return res
                
                
def x_wins(state):
    #row
    for i in range(3):
        if(state[i][0] == state[i][1] and state[i][1] == state[i][2]):
            if(state[i][1] == 'X'):
                return True
    #column
    for i in range(3):
        if(state[0][i] == state[1][i] and state[1][i] == state[2][i]):
            if(state[1][i] == 'X'):
                return True
    #diagonal
    if((state[1][1] == state[0][2] and state[1][1] == state[2][0]) or (state[1][1] == state[0][0] and state[1][1] == state[2][2])):
        if(state[1][1] == 'X'):
            return True
    return False

def o_wins(state):
    #row
    for i in range(3):
        if(state[i][0] == state[i][1] and state[i][1] == state[i][2]):
            if(state[i][1] == 'O'):
                return True
    #column
    for i in range(3):
        if(state[0][i] == state[1][i] and state[1][i] == state[2][i]):
            if(state[1][i] == 'O'):
                return True
    #diagonal
    if((state[1][1] == state[0][2] and state[1][1] == state[2][0]) or (state[1][1] == state[0][0] and state[1][1] == state[2][2])):
        if(state[1][1] == 'O'):
            return True
    return False
        
def board_full(state):
    for i in range(3):
        if(state[i][0]==' ' or state[i][1]==' ' or state[i][2]==' '):
            return False
    return True

def board_empty(state):
    for i in range(3):
        if(state[i][0]!=' ' or state[i][1]!=' ' or state[i][2]!=' '):
            return False
    return True

def empty_spaces(state):#so it can be done in fewer steps
    count = 0
    for i in range(3):
        for j in range(3):
            if(state[i][j] == ' '):
                count += 1
    return count

def max_value(state,a,b):
    v = -math.inf
    #new = copy.deepcopy(board)
    for child in children(state):
        state[child[0]][child[1]] = 'X' #computer is X and it wanna maximize 
        v =max(v,alpha_beta_pruning_minmax(state,a,b,False))#child minimizes
        state[child[0]][child[1]] = ' '
        if(v >= b): #prune
            return v
        a = max(a,v)
    return v

def min_value(state,a,b):
    v = math.inf
    #new = copy.deepcopy(board)
    for child in children(state):
        state[child[0]][child[1]] = 'O' #opponent is O and it wanna minimize 
        v =min(v, alpha_beta_pruning_minmax(state,a,b,True))#child wanna maximize
        state[child[0]][child[1]] = ' '
        if(v <= a):
            return v
        b = min(b,v)
    return v

def alpha_beta_pruning_minmax(state,alpha,beta,max_min):
    
    if (x_wins(state)):
        return 1 *(empty_spaces(state)+1) #+1 for spaces before choosing this option.
    if (o_wins(state)):
        return -1 * (empty_spaces(state)+1)
    if(board_full(state)):
        return 0
    
    if(max_min):#if it's maximising it's True
        return max_value(state,alpha,beta)
    else:
        return min_value(state,alpha,beta)

if __name__ == "__main__":
    intro()
    computer_plays()
    show_board()
    turn = False
    print('#'*19)
    while(not board_full(board)):
        if(x_wins(board)):
            priint('Computer won!')
            exit()
        if(o_wins(board)):
            print('You won!')
            exit()
        
        if(turn):
            computer_plays()
            turn = False
        else:
            human_plays()
            turn = True
        show_board()
        print('#'*19)
        
    print("it's a tie !")
          
