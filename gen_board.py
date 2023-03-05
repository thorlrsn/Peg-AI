import numpy as np

class Peg:

    def __init__(self):
        #change to userinput after development
        self.board_size = 5

        self.board = np.full((self.board_size,self.board_size),np.NaN)


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
        self.board[4,0] = 0

    # Checking if the move is out of bounds (OoB)
    def check_OoB(self, i, j):
        if i+j > self.board_size-1:
            return False
        else:
            return True
        
    # Illustrating the self.board in a nice way
    def print_board(self):
        for i in range(self.board_size):
            print(self.board[i,0:self.board_size-i])

    def num_pegs(self):
        return np.count_nonzero(self.board == 1)

    def move(self):
        # checking if each peg can move
        for i in range(self.board_size):
            for j in range(self.board_size):
                # checking move
                # S we want (2,0) (i,j) to print((4,0))
                if self.board[i,j] == 1 and i+2 < self.board_size and self.board[i+2,j] == 0 and self.board[i+1,j] == 1 and self.check_OoB(i, j):
                    print("S",i,j, " -> ", i+2, j)
                    self.board[i,j] = 0
                    self.board[i+1,j] = 0
                    self.board[i+2,j] = 1
                    self.print_board()
                    return self.board
                # N 
                elif self.board[i,j] == 1 and i-2 >= 0 and self.board[i-2,j] == 0 and self.board[i-1,j] == 1 and self.check_OoB(i, j):
                    print("N",i,j, " -> ", i-2, j)
                    self.board[i,j] = 0
                    self.board[i-1,j] = 0
                    self.board[i-2,j] = 1
                    self.print_board()
                    return self.board

                # E
                elif self.board[i,j] == 1 and j+2 < self.board_size and self.board[i,j+2] == 0 and self.board[i,j+1] == 1 and self.check_OoB(i, j):
                    print("E",i,j, " -> ", i, j+2)
                    self.board[i,j] = 0
                    self.board[i,j+1] = 0
                    self.board[i,j+2] = 1
                    self.print_board()
                    return self.board
                # W 
                elif self.board[i,j] == 1 and j-2 >= 0 and self.board[i,j-2] == 0 and self.board[i,j-1] == 1 and self.check_OoB(i, j):
                    print("W",i,j, " -> ", i, j-2)
                    self.board[i,j] = 0
                    self.board[i,j-1] = 0
                    self.board[i,j-2] = 1
                    self.print_board()
                    return self.board

                # SW
                elif self.board[i,j] == 1 and i+2 < self.board_size and j-2 >= 0 and self.board[i+2,j-2] == 0 and self.board[i+1,j-1] == 1 and self.check_OoB(i, j):
                    print("SW", i, j, " -> ", i+2, j-2)
                    self.board[i,j] = 0
                    self.board[i+1,j-1] = 0
                    self.board[i+2,j-2] = 1
                    self.print_board()
                    return self.board

                # NE
                elif self.board[i,j] == 1 and i-2 >= 0 and j+2 < self.board_size and self.board[i-2,j+2] == 0 and self.board[i-1,j+1] == 1 and self.check_OoB(i, j):
                    print("NE", i, j, " -> ", i-2, j+2)
                    self.board[i,j] = 0
                    self.board[i-1,j+1] = 0
                    self.board[i-2,j+2] = 1
                    self.print_board()
                    return self.board

if __name__ == "__main__":
    board = Peg()

    while board.num_pegs() > 1:
        board.move()
    

