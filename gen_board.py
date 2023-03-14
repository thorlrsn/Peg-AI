import numpy as np
import time
import sys
from PrettyPrint import PrettyPrintTree

class Tree:
    def __init__(self, value):
        self.val = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        return child

class Peg:

    def __init__(self):
        #change to userinput after development
        self.board_size = 5
        self.completed_moves = []
        self.frontier = []
        self.won = False
        self.board = np.full((self.board_size,self.board_size),3)
        self.move1 = []
        self.dictall = {}
        self.node_counter = 0
        self.next_node = 0
        self.current_path = []
        # self.pt = PrettyPrintTree(lambda x: x.children, lambda x: x.val)
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
        self.board[0,4] = 0
        


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
        # print("MOVING :: ",action)
        self.board[action[0],action[1]] = 0
        self.board[action[2],action[3]] = 0
        self.board[action[4],action[5]] = 1
        # self.print_board()
        self.completed_moves.append(action)

    def undo_move(self):
        # print("UNDO")
        action = self.completed_moves.pop()
        self.board[action[0],action[1]] = 1
        self.board[action[2],action[3]] = 1
        self.board[action[4],action[5]] = 0
        # self.print_board()

    def check_moves_and_add(self):
        valid_moves = self.check_move()
        
        for i in range(len(valid_moves)):
            temp = self.current_path.copy()
            temp.append(valid_moves[i])

            if self.node_counter == 0:
                self.dictall[self.node_counter] = { "Move" : temp}
                # print("Added dict",self.dictall[self.node_counter])
                self.node_counter += 1
            # check if path is already in dict
            else:
                found = False
                temp2 = {"Move" : temp}
                if temp2 not in self.dictall.values():
                    self.dictall[self.node_counter] = { "Move" : temp}
                    # print("Added dict",self.dictall[self.node_counter])
                    self.node_counter += 1

    # depth-first search
    def dfs(self):
        while self.won == False:
            
            # Starting by getting the possible moves
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

            # If the frontier is empty, so solution found.
            if len(self.frontier) == 0:
                print("There are no more moves left in the frontier!")
                break

            # Getting the next move from the frontier
            print(self.frontier)
            self.move1 = self.frontier.pop()
            self.move(self.move1)

            
            if self.num_pegs() == 1:
                print("Solution :: ",self.completed_moves)
                print("Length of solution :: ", len(self.completed_moves))
                self.won = True

            self.dfs()
    
    def dfs2(self):
        """
        DOESNT WORK YET
        """
        while self.won == False:
            # Starting by getting the possible moves
            self.check_moves_and_add()

            # If there are no possible moves, we have to move up the tree, tracing back our steps. This is done by 
            # using the undo function
            # if len(valid_moves) == 0:
            #     self.undo_move()
            #     valid_moves = self.check_move() # Gotta update the valid moves
            #     while self.frontier[-1] not in valid_moves: # To make the newest frontier corresponds to a current valid move
            #         self.undo_move()
            #         valid_moves = self.check_move()
            # else: # appending new nodes to our frontier
            #     for ele in valid_moves:
            #         self.frontier.append(ele)

            # Getting the next move from the frontier
            

            for i in range(len(self.dictall[self.next_node]["Move"])):
                # -1 means newest node
                move = self.dictall[-1]["Move"][i]
                # print("Moving to",move)
                self.move(move)
                self.current_path.append(move) 
                self.check_moves_and_add()
            # print(self.num_pegs())

            if self.num_pegs() == 2:
                print("Solution :: ",self.completed_moves)
                print("Length of solution :: ", len(self.completed_moves))
                self.won = True

            else:
                for i in range(len(self.dictall[self.next_node]["Move"])):
                    self.undo_move()
                    self.current_path = []

            self.next_node += 1
            print(self.node_counter,self.next_node)
            # print("Not goal state, moving to node", self.next_node)
            # print("Node",self.next_node, "has the path", self.dictall[self.next_node]["Move"])
            self.dfs2()


    # breadth-first search
    def bfs(self):
        while self.won == False:
            # Starting by getting the possible moves
            self.check_moves_and_add()

            # If there are no possible moves, we have to move up the tree, tracing back our steps. This is done by 
            # using the undo function
            # if len(valid_moves) == 0:
            #     self.undo_move()
            #     valid_moves = self.check_move() # Gotta update the valid moves
            #     while self.frontier[-1] not in valid_moves: # To make the newest frontier corresponds to a current valid move
            #         self.undo_move()
            #         valid_moves = self.check_move()
            # else: # appending new nodes to our frontier
            #     for ele in valid_moves:
            #         self.frontier.append(ele)

            # Getting the next move from the frontier
            

            for i in range(len(self.dictall[self.next_node]["Move"])):
                move = self.dictall[self.next_node]["Move"][i]
                # print("Moving to",move)
                self.move(move)
                self.current_path.append(move) 
                self.check_moves_and_add()
            print(self.num_pegs())

            if self.num_pegs() == 1:
                print("Solution :: ",self.completed_moves)
                print("Length of solution :: ", len(self.completed_moves))
                self.won = True

            else:
                for i in range(len(self.dictall[self.next_node]["Move"])):
                    self.undo_move()
                    self.current_path = []
                # print("Deleting node")
                del self.dictall[self.next_node]
                self.node_counter -= 1
                

            self.next_node += 1
            print(self.node_counter,self.next_node)
            # print("Not goal state, moving to node", self.next_node)
            # print("Node",self.next_node, "has the path", self.dictall[self.next_node]["Move"])
            self.bfs()

if __name__ == "__main__":
    sys.setrecursionlimit(8000)
    board = Peg()
    board.bfs()

    
    

