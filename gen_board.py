import numpy as np


#change to userinput after development
board_size = 5

board = np.full((board_size,board_size),np.NaN)


## 0 1 2 3 4 
#0 x x x x x
#1 x x x x
#2 x x x
#3 x x
#4 x
#

# print(board[0][:])
for i in range(board_size):
    # print(board_size-i)
    board[i,0:board_size-i] = 1

# setting random empty position, will be hardcoded for development
board[2,2] = 0

# Illustrating the board in a nice way
for i in range(board_size):
    print(board[i,0:board_size-i])

# checking if each peg can move
for i in range(board_size):
    for j in range(board_size):
        # checking move
        # S we want (2,0) (i,j) to print((4,0))
        if i+2 < board_size and board[i+2,j] == 0 and board[i+1,j] == 1:
            print("S",i,j)
        # N 
        elif i-2 >= 0 and board[i-2,j] == 0 and board[i-1,j] == 1:
            print("N",i,j)
        # E
        if j+2 < board_size and board[i,j+2] == 0 and board[i,j+1] == 1:
            print("E",i,j)
        # W 
        elif j-2 >= 0 and board[i,j-2] == 0 and board[i,j-1] == 1:
            print("W",i,j)

        # SW
        elif i+2 < board_size and j-2 >= 0 and board[i+2,j-2] == 0 and board[i+1,j-1] == 1:
            print("SW", i, j)

        # NE
        elif i-2 >= 0 and j+2 < board_size and board[i-2,j+2] == 0 and board[i-1,j+1] == 1:
            print("NE", i, j)
