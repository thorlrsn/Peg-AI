import numpy as np
import time
import sys

class Peg:

    def __init__(self):
        #change to userinput after development
        self.board_size = 5
        self.completed_moves = []
        self.frontier = []
        self.won = False
        self.board = np.full((self.board_size,self.board_size),3)

        ## 0 1 2 3 4 
        #0 x x x x x
        #1 x x x x
        #2 x x x
        #3 x x
        #4 x
        #

        # print(self.board[0][:])
        for i in range(self.board_size):
            # print(self.self.board_size-i)
            self.board[i,0:self.board_size-i] = 1

        # setting random empty position, will be hardcoded for development
        self.board[0,0] = 0

    # Checking if the move is out of bounds (OoB)
    def check_OoB(self, i, j):
        if i+j > self.board_size-1:
            return False
        else:
            return True
    
    def board_return(self):
        return self.board
    
    # Illustrating the self.board in a nice way
    def print_board(self):
        for i in range(self.board_size):
            print(self.board[i,0:self.board_size-i])

    def num_pegs(self):
        return np.count_nonzero(self.board == 1)

    def check_move(self):
        # valid_moves = np.array([0,0,0,0,0,0])
        self.valid_moves = []
        # checking if each peg can move
        for i in range(self.board_size):
            for j in range(self.board_size):
                # checking move
                # S we want (2,0) (i,j) to print((4,0))
                if self.board[i,j] == 1 and i+2 < self.board_size and self.board[i+2,j] == 0 and self.board[i+1,j] == 1 and self.check_OoB(i, j):
                    # print("S",i,j, " -> ", i+2, j)
                    # valid_moves = np.vstack([valid_moves, [i,j,i+1,j,i+2,j]])
                    self.valid_moves.append([i,j,i+1,j,i+2,j])
                # N 
                if self.board[i,j] == 1 and i-2 >= 0 and self.board[i-2,j] == 0 and self.board[i-1,j] == 1 and self.check_OoB(i, j):
                    # print("N",i,j, " -> ", i-2, j)   
                    # valid_moves = np.vstack([valid_moves, [i,j,i-1,j,i-2,j]])      
                    self.valid_moves.append([i,j,i-1,j,i-2,j])
                # E
                if self.board[i,j] == 1 and j+2 < self.board_size and self.board[i,j+2] == 0 and self.board[i,j+1] == 1 and self.check_OoB(i, j):
                    # print("E",i,j, " -> ", i, j+2)
                    # valid_moves = np.vstack([valid_moves, [i,j,i,j+1,i,j+2]])
                    self.valid_moves.append([i,j,i,j+1,i,j+2])
                # W 
                if self.board[i,j] == 1 and j-2 >= 0 and self.board[i,j-2] == 0 and self.board[i,j-1] == 1 and self.check_OoB(i, j):
                    # print("W",i,j, " -> ", i, j-2)
                    # valid_moves = np.vstack([valid_moves, [i,j,i,j-1,i,j-2]])
                    self.valid_moves.append([i,j,i,j-1,i,j-2])

                # SW
                if self.board[i,j] == 1 and i+2 < self.board_size and j-2 >= 0 and self.board[i+2,j-2] == 0 and self.board[i+1,j-1] == 1 and self.check_OoB(i, j):
                    # print("SW", i, j, " -> ", i+2, j-2)
                    # valid_moves = np.vstack([valid_moves, [i,j,i+1,j-1,i+2,j-2]])
                    self.valid_moves.append([i,j,i+1,j-1,i+2,j-2])

                # NE
                if self.board[i,j] == 1 and i-2 >= 0 and j+2 < self.board_size and self.board[i-2,j+2] == 0 and self.board[i-1,j+1] == 1 and self.check_OoB(i, j):
                    # print("NE", i, j, " -> ", i-2, j+2)
                    # valid_moves = np.vstack([valid_moves, [i,j,i-1,j+1,i-2,j+2]])
                    self.valid_moves.append([i,j,i-1,j+1,i-2,j+2])
        
        return self.valid_moves
                
    def move(self, action):
        print("MOVING :: ",action)
        self.board[action[0],action[1]] = 0
        self.board[action[2],action[3]] = 0
        self.board[action[4],action[5]] = 1
        self.print_board()
        self.completed_moves.append(action)


    def undo_move(self):
        print("UNDO")
        action = self.completed_moves.pop()
        self.board[action[0],action[1]] = 1
        self.board[action[2],action[3]] = 1
        self.board[action[4],action[5]] = 0
        self.print_board()

    # depth-first search
    def dfs(self):

        while self.won == False:
            # Starting by getting the possuble moves
            valid_moves = self.check_move()

            # If there are no possible moves, we have to move up the tree, tracing back our steps. This is done by 
            # using the undo function
            if len(valid_moves) == 0:
                self.undo_move()
                valid_moves = self.check_move() # Gotta update the valid moves
                while self.frontier[-1] not in valid_moves: # To make the newest frontier corresponds to a current valid move
                    self.undo_move()
                    valid_moves = self.check_move()
            else: # appending new nodes to our frontier
                for ele in valid_moves:
                    self.frontier.append(ele)

            # Getting the next move from the frontier
            move = self.frontier.pop()
            self.move(move) 
            
            if self.num_pegs() == 1:
                print("Solution :: ",self.completed_moves)
                print("Length of solution :: ", len(self.completed_moves))
                self.won = True

            self.dfs()

    def A_Star(self):
        self.frontier
        last_move = self.completed_moves[-1]

        goal_cost = 0
        
        while self.won == False:
            # get the possible moves
            valid_moves = self.check_move()

            # get next move from the frontier
            move = self.frontier.pop()
    
if __name__ == "__main__":
    sys.setrecursionlimit(2000)
    board = Peg()
    board.dfs()

    
    

