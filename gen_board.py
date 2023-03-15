import numpy as np
import time
import sys

class Tree:
    def __init__(self, value):
        self.val = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        return child

class State:
    def __init__(self, board_size):
        self.board_size: int = board_size
        self.children: dict = {}
        self.board: np.array = np.full((board_size, board_size), 1)
        self.parent: State = None
        self.node_number: int = None

    def print_tree_nodes(self, level=0):
        print('\t' * level + repr(self.node_number))
        for child in self.children:
            node = self.children[child]
            node.print_tree_nodes(level + 1)

    def print_tree_boards(self, node, level=0):
        print('\t' * level + repr(self.print_board(node, level)))
        for child in self.children:
            node = self.children[child]
            node.print_tree_boards(node, level + 1)

    def print_board(self, node, level=0):
        board = node.board
        for i in range(self.board_size):
            print('\t' * level + str(board[i, 0:self.board_size-i]))

class Peg:
    def __init__(self, board_size: int, empty_space: list[int]):
        self.board_size: int = board_size
        self.initial_empty_space: list[int] = empty_space
        self.completed_moves: list[State] = []
        self.frontier: list = []
        self.won: bool = False
        self.nodes: dict = {}
        self.initial_state: State = None

        ## 0 1 2 3 4 
        #0 x x x x x
        #1 x x x x
        #2 x x x
        #3 x x
        #4 x
        #

        self.create_initial_state()

    def create_initial_state(self):
        '''Instantiates the initial state and adds it to the dictionary of nodes'''
        self.initial_state = State(self.board_size)
        self.initial_state.board[self.initial_empty_space[0], self.initial_empty_space[1]] = 0
        self.initial_state.node_number = 0
        self.nodes[self.initial_state.node_number] = self.initial_state

    def create_new_node(self, action: list, parent: State):
        '''Creates a new instance of State and adds it to the dictionary of nodes'''
        # create instance of State
        new_state = State(self.board_size)

        # make the board from the parent and then apply the move
        new_state.parent = parent
        new_state.board = parent.board.copy()
        new_state.board = self.move(action, new_state)

        # use the dict keys to create a new node_number then add to dict
        keys = list(self.nodes.keys())
        new_state.node_number = keys[-1] + 1
        self.nodes[new_state.node_number] = new_state

        # add as child to the parent node
        parent.children[new_state.node_number] = new_state

        return new_state
    
    def check_OoB(self, i: int, j: int):
        '''Checks if a suggested move is out of bounds (OoB)'''
        if i+j > self.board_size-1:
            return False
        else:
            return True

    def check_move(self, state: State):
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
                
    def move(self, action, state: State):
        state.board[action[0],action[1]] = 0
        state.board[action[2],action[3]] = 0
        state.board[action[4],action[5]] = 1
        return state.board

    def get_completed_moves(self):
        # last state
        keys = list(self.nodes.keys())
        final_state = self.nodes[keys[-1]]
        self.completed_moves.append(final_state)

        # trace upwards via parents
        while self.completed_moves[-1] != self.initial_state:
            self.completed_moves.append(self.completed_moves[-1].parent)
        self.completed_moves.reverse()

    def print_tree_nodes(self):
        self.initial_state.print_tree_nodes()

    def print_tree_boards(self):
        self.initial_state.print_tree_boards(self.initial_state)

    def print_last_board(self):
        keys = list(self.nodes.keys())
        self.initial_state.print_board(self.nodes[keys[-1]])

    def print_completed_moves(self):
        for move in self.completed_moves:
            print()
            repr(self.initial_state.print_board(move))

def dfs(board_size: int, initial_empty_space: list[int]):
    '''Depth First Search dfsGame'''
    dfsGame = Peg(board_size, initial_empty_space)

    print("\nSTARTING BOARD\n")
    dfsGame.print_last_board()

    # start frontier with initial state
    dfsGame.frontier.append(dfsGame.initial_state)
    
    while dfsGame.frontier:
        # get last state in frontier
        state = dfsGame.frontier.pop()

        # check how many pins are left accounting for the lower triangle of the array
        if (state.board == 1).sum() == 1 + (dfsGame.board_size * (dfsGame.board_size - 1))/2:
            dfsGame.get_completed_moves()
            print((state.board==1).sum())
            print("\n\n---GAME WON---")
            # print("printing tree of nodes:\n")
            # dfsGame.print_tree_nodes()
            # print("\nprinting tree of boards:\n")
            # dfsGame.print_tree_boards()
            print("LAST BOARD\n")
            dfsGame.print_last_board()
            print("\nGAME PLAY")
            dfsGame.print_completed_moves()
            return
        
        # get possible moves and if not already in frontier, create and add to frontier
        dfsGame.check_move(state)
        for move in dfsGame.valid_moves:
            if move not in dfsGame.frontier:
                new_node = dfsGame.create_new_node(move, state)
                dfsGame.frontier.append(new_node)

    print("\nGAME LOST - no solution")
    print("\nprinting last board:\n")
    dfsGame.print_last_board()

def Dijkstra(self):
    self.frontier
    last_move = self.completed_moves[-1]
    
    while self.won == False:
        # get the possible moves
        valid_moves = self.check_move()

        # get next move from the frontier
        move = self.frontier.pop()
    
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
    sys.setrecursionlimit(2000)
    board_size = 5
    empty_space = [0, 0]

    # play game with Depth First Search
    dfs(board_size, empty_space)

    
    

