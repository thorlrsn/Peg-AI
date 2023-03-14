import numpy as np
import time
import sys
from PrettyPrintTree.PrettyPrint import PrettyPrintTree

class Tree:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        return child

class State:
    def __init__(self, board_size):
        self.children: dict = {}
        self.board = np.full((board_size, board_size),3)
        self.parent: State = None
        self.node_number: int = np.nan

class Peg:
    def __init__(self):
        # change to user input after development
        self.board_size = 5
        self.completed_moves = []
        self.frontier = []
        self.won = False
        self.state_dictionary = {}
        self.nodes = []

        ## 0 1 2 3 4 
        #0 x x x x x
        #1 x x x x
        #2 x x x
        #3 x x
        #4 x
        #

        # instantiate initial state and update nodes
        initial_state = State(self.board_size)
        self.state_dictionary[0] = initial_state
        self.nodes.append(0)

        for i in range(self.board_size):
            initial_state.board[i,0:self.board_size-i] = 1

        # setting random empty position, will be hardcoded for development
        self.state_dictionary[0].board[1,2] = 0

        self.print_board(initial_state)

    # Checking if the move is out of bounds (OoB)
    def check_OoB(self, i, j):
        if i+j > self.board_size-1:
            return False
        else:
            return True
    
    def board_return(self, state):
        return state.board
    
    # Illustrating the self.board in a nice way
    def print_board(self, state):
        for i in range(self.board_size):
            print(state.board[i, 0:self.board_size-i])


    def num_pegs(self, state):
        return np.count_nonzero(state.board == 1)

    def check_move(self, state):
        # valid_moves = np.array([0,0,0,0,0,0])
        self.valid_moves = []
        # checking if each peg can move
        for i in range(self.board_size):
            for j in range(self.board_size):
                # checking move
                # S we want (2,0) (i,j) to print((4,0))
                if state.board[i,j] == 1 and i+2 < self.board_size and state.board[i+2,j] == 0 and state.board[i+1,j] == 1 and self.check_OoB(i, j):
                    self.valid_moves.append([i,j,i+1,j,i+2,j])
                # N 
                if state.board[i,j] == 1 and i-2 >= 0 and state.board[i-2,j] == 0 and state.board[i-1,j] == 1 and self.check_OoB(i, j):
                    self.valid_moves.append([i,j,i-1,j,i-2,j])
                # E
                if state.board[i,j] == 1 and j+2 < self.board_size and state.board[i,j+2] == 0 and state.board[i,j+1] == 1 and self.check_OoB(i, j):
                    self.valid_moves.append([i,j,i,j+1,i,j+2])
                # W 
                if state.board[i,j] == 1 and j-2 >= 0 and state.board[i,j-2] == 0 and state.board[i,j-1] == 1 and self.check_OoB(i, j):
                    self.valid_moves.append([i,j,i,j-1,i,j-2])
                # SW
                if state.board[i,j] == 1 and i+2 < self.board_size and j-2 >= 0 and state.board[i+2,j-2] == 0 and state.board[i+1,j-1] == 1 and self.check_OoB(i, j):
                    self.valid_moves.append([i,j,i+1,j-1,i+2,j-2])
                # NE
                if state.board[i,j] == 1 and i-2 >= 0 and j+2 < self.board_size and state.board[i-2,j+2] == 0 and state.board[i-1,j+1] == 1 and self.check_OoB(i, j):
                    self.valid_moves.append([i,j,i-1,j+1,i-2,j+2])
        return self.valid_moves
                

    def move(self, action, state):
        print("MOVING :: ", action)
        state.board[action[0],action[1]] = 0
        state.board[action[2],action[3]] = 0
        state.board[action[4],action[5]] = 1
        self.print_board(state)
        self.completed_moves.append(action)


    def undo_move(self, state):
        print("UNDO")
        action = self.completed_moves.pop()
        self.print_board(state)


    # depth-first search
    def dfs(self):
        # get initial state
        parent_state = self.state_dictionary[0]

        # pt = PrettyPrintTree(lambda x: x.children, lambda x: x.value)
        # tree = Tree(1)
        # child = tree.add_child(Tree(2))
        
        while self.won == False:
            # Starting by getting the possible moves
            valid_moves = self.check_move(parent_state)

            # If there are no possible moves, we have to move up the tree, tracing back our steps. This is done by 
            # using the undo function
            if len(valid_moves) == 0:
                parent_state = parent_state.parent
                self.undo_move(parent_state)
                valid_moves = self.check_move(parent_state) # Gotta update the valid moves
                while self.frontier[-1] not in valid_moves: # To make the newest frontier corresponds to a current valid move
                    parent_state = parent_state.parent
                    self.undo_move(parent_state)
                    valid_moves = self.check_move(parent_state)
            else: # appending new nodes to our frontier
                for ele in valid_moves:
                    self.frontier.append(ele)

            # Getting the next move from the frontier
            move = self.frontier.pop()

            # create child and add to dictionary
            new_state = State(self.board_size)
            keys = list(parent_state.children.keys())
            if keys:
                key = keys[-1] + 1
            else:
                key = 0
            parent_state.children = {key: new_state}
            new_state.parent = parent_state
            new_state.board = parent_state.board.copy()
            self.nodes.append(self.nodes[-1] + 1)

            self.move(move, new_state)
            parent_state = new_state 

            if self.num_pegs(new_state) == 1:
                print("Solution :: ",self.completed_moves)
                print("Length of solution :: ", len(self.completed_moves))
                self.won = True

            # pt(self.state_dictionary)
            # print()
            # print()

            # self.dfs()

    def Dijkstra(self):
        self.frontier
        last_move = self.completed_moves[-1]
        
        while self.won == False:
            # get the possible moves
            valid_moves = self.check_move()

            # get next move from the frontier
            move = self.frontier.pop()
    
if __name__ == "__main__":
    sys.setrecursionlimit(2000)
    board = Peg()
    board.dfs()

    
    

