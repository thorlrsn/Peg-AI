import numpy as np
import time
import sys
from collections import deque
import math

class State:
    def __init__(self, board_size):
        self.board_size: int = board_size
        self.children: dict = {}
        self.board: np.array = np.full((board_size, board_size), 1)
        self.parent: State = None
        self.node_number: int = None

        # Thor edit! init cost for state
        self.cost = 0

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
        self.moves_to_win: list[State] = []
        self.frontier: deque = deque([])
        self.frontier_cost: dict = {}
        self.expanded_states: deque = deque([])
        self.won: bool = False
        self.nodes: dict = {}
        self.initial_state: State = None

        # Thor edits!
        self.mid_coor = (self.board_size/4)-0.25

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

    def create_new_node(self, action: list, cost: int, parent: State, strategy: str):
        '''Creates a new instance of State and adds it to the dictionary of nodes'''
        # create instance of State
        new_state = State(self.board_size)

        # make the board from the parent and then apply the move
        new_state.parent = parent
        new_state.board = parent.board.copy()
        new_state.board = self.move(action, new_state)
        
        # Thor edit! 
        new_state.cost = new_state.parent.cost + cost
        
        # use the dict keys to create a new node_number then add to dict
        keys = list(self.nodes.keys())
        new_state.node_number = keys[-1] + 1
        self.nodes[new_state.node_number] = new_state
        
        # check if state already exists
        if np.any(np.all(new_state.board == self.expanded_states, axis=1)):
            self.expanded_states.append(new_state.board)
            if strategy == 'dfs':
                # push
                self.frontier.append(new_state)
            elif strategy == 'bfs':
                # enqueue
                self.frontier.appendleft(new_state)
            elif strategy == 'cost':
                self.frontier.append(new_state)
                self.frontier_cost[new_state.node_number] = new_state.cost

            # add as child to the parent node
            parent.children[new_state.node_number] = new_state
    
    def check_OoB(self, i: int, j: int):
        '''Checks if a suggested move is out of bounds (OoB)'''
        if i+j > self.board_size-1:
            return False
        else:
            return True

    def check_move(self, state: State):
        # valid_moves = np.array([0,0,0,0,0,0])
        valid_moves = []
        cost_moves = []
        # checking if each peg can move
        for i in range(self.board_size):
            for j in range(self.board_size):
                # checking move
                # S we want (2,0) (i,j) to print((4,0))
                if state.board[i,j] == 1 and i+2 < self.board_size and state.board[i+2,j] == 0 and state.board[i+1,j] == 1 and self.check_OoB(i, j):
                    valid_moves.append([i,j,i+1,j,i+2,j])
                    dist_to_mid_ori = math.sqrt((i-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    dist_to_mid_des = math.sqrt(((i+2)-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    if [i+2,j] == [4,0]:
                        cost_moves.append(3)
                    elif dist_to_mid_ori < dist_to_mid_des:
                        cost_moves.append(2)
                    elif dist_to_mid_ori > dist_to_mid_des:
                        cost_moves.append(1)
                    
                # N 
                if state.board[i,j] == 1 and i-2 >= 0 and state.board[i-2,j] == 0 and state.board[i-1,j] == 1 and self.check_OoB(i, j):
                    valid_moves.append([i,j,i-1,j,i-2,j])
                    dist_to_mid_ori = math.sqrt((i-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    dist_to_mid_des = math.sqrt(((i-2)-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    if [i-2,j] == [0,0]:
                        cost_moves.append(3)
                    elif dist_to_mid_ori < dist_to_mid_des:
                        cost_moves.append(2)
                    elif dist_to_mid_ori > dist_to_mid_des:
                        cost_moves.append(1)
                # E
                if state.board[i,j] == 1 and j+2 < self.board_size and state.board[i,j+2] == 0 and state.board[i,j+1] == 1 and self.check_OoB(i, j):
                    valid_moves.append([i,j,i,j+1,i,j+2])
                    dist_to_mid_ori = math.sqrt((i-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    dist_to_mid_des = math.sqrt((i-self.mid_coor)**2 + ((j+2)-self.mid_coor)**2)
                    if [i,j+2] == [0,4]:
                        cost_moves.append(3)
                    elif dist_to_mid_ori < dist_to_mid_des:
                        cost_moves.append(2)
                    elif dist_to_mid_ori > dist_to_mid_des:
                        cost_moves.append(1)
                # W 
                if state.board[i,j] == 1 and j-2 >= 0 and state.board[i,j-2] == 0 and state.board[i,j-1] == 1 and self.check_OoB(i, j):
                    valid_moves.append([i,j,i,j-1,i,j-2])
                    dist_to_mid_ori = math.sqrt((i-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    dist_to_mid_des = math.sqrt((i-self.mid_coor)**2 + ((j-2)-self.mid_coor)**2)
                    if [i,j-2] == [0,0]:
                        cost_moves.append(3)
                    elif dist_to_mid_ori < dist_to_mid_des:
                        cost_moves.append(2)
                    elif dist_to_mid_ori > dist_to_mid_des:
                        cost_moves.append(1)
                # SW
                if state.board[i,j] == 1 and i+2 < self.board_size and j-2 >= 0 and state.board[i+2,j-2] == 0 and state.board[i+1,j-1] == 1 and self.check_OoB(i, j):
                    valid_moves.append([i,j,i+1,j-1,i+2,j-2])
                    dist_to_mid_ori = math.sqrt((i-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    dist_to_mid_des = math.sqrt(((i+2)-self.mid_coor)**2 + ((j-2)-self.mid_coor)**2)
                    if [i+2,j-2] == [4,0]:
                        cost_moves.append(3)
                    elif dist_to_mid_ori < dist_to_mid_des:
                        cost_moves.append(2)
                    elif dist_to_mid_ori > dist_to_mid_des:
                        cost_moves.append(1)
                # NE
                if state.board[i,j] == 1 and i-2 >= 0 and j+2 < self.board_size and state.board[i-2,j+2] == 0 and state.board[i-1,j+1] == 1 and self.check_OoB(i, j):
                    valid_moves.append([i,j,i-1,j+1,i-2,j+2])
                    dist_to_mid_ori = math.sqrt((i-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    dist_to_mid_des = math.sqrt(((i-2)-self.mid_coor)**2 + ((j+2)-self.mid_coor)**2)
                    if [i-2,j+2] == [0,4]:
                        cost_moves.append(3)
                    elif dist_to_mid_ori < dist_to_mid_des:
                        cost_moves.append(2)
                    elif dist_to_mid_ori > dist_to_mid_des:
                        cost_moves.append(1)

        return valid_moves, cost_moves
           
    def move(self, action, state: State):
        state.board[action[0],action[1]] = 0
        state.board[action[2],action[3]] = 0
        state.board[action[4],action[5]] = 1
        return state.board

    def get_completed_moves(self, querystate):
        self.moves_to_win = []
        self.moves_to_win.append(querystate)

        # trace upwards via parents
        while self.moves_to_win[-1] != self.initial_state:
            self.moves_to_win.append(self.moves_to_win[-1].parent)
        self.moves_to_win.reverse()

    def print_tree_nodes(self):
        self.initial_state.print_tree_nodes()

    def print_tree_boards(self):
        self.initial_state.print_tree_boards(self.initial_state)

    def print_last_board(self):
        keys = list(self.nodes.keys())
        self.initial_state.print_board(self.nodes[keys[-1]])

    def print_completed_moves(self):
        for move in self.moves_to_win:
            print()
            repr(self.initial_state.print_board(move))

def graph_search(board_size: int, initial_empty_space: list[int], strategy: str):
    '''Graph Search Game'''
    game = Peg(board_size, initial_empty_space)

    print("\nSTARTING BOARD\n")
    game.print_last_board()

    # start frontier with initial state
    if strategy == 'dfs':
        # push
        game.frontier.append(game.initial_state)
    elif strategy == 'bfs':
        # enqueue
        game.frontier.appendleft(game.initial_state)
    
    elif strategy == 'cost':
        game.frontier.append(game.initial_state)
        game.frontier_cost[game.initial_state.node_number] = np.Inf
        


    # while len(game.expanded_states) < 20:
    while game.won == False:
        
        if strategy == 'dfs' or strategy == 'bfs':
        # get last state in frontier (dequeue/pop) and add to expanded_states and path to win
            state = game.frontier.pop()
        
        elif strategy == 'cost':
            # print(game.frontier_cost)
            list_of_costs = [min(game.frontier_cost, key=game.frontier_cost.get)]
            cheapest_state = None
            deepest_level = 0
            for key in list_of_costs:
                temp_state = game.nodes[key]
                game.get_completed_moves(temp_state)
                level = len(game.moves_to_win)
                if level >= deepest_level:
                    cheapest_state = temp_state
            state = cheapest_state
            del game.frontier_cost[state.node_number]
        
        game.expanded_states.append(state.board)

        # check how many pins are left accounting for the lower triangle of the array
        if (state.board == 1).sum() == 1 + (game.board_size * (game.board_size - 1))/2:
            game.get_completed_moves(game.nodes[list(game.nodes.keys())[-1]])
            print((state.board==1).sum())
            print("\n\n---GAME WON---")
            # print("printing tree of nodes:\n")
            # game.print_tree_nodes()
            # print("\nprinting tree of boards:\n")
            # game.print_tree_boards()
            print("LAST BOARD\n")
            game.print_last_board()
            print("\nGAME PLAY")
            game.print_completed_moves()
            return
        else:
            game.get_completed_moves(game.nodes[list(game.nodes.keys())[-1]])
            if len(game.expanded_states) % 100 == 0:
                print('level: ' + str(len(game.moves_to_win)) + ' nodes visited: ' + str(len(game.expanded_states)), "min cost", state.cost)
        
        # get possible moves and if not already in frontier, create and add to frontier
        valid_moves, cost_moves = game.check_move(state)
        for move, cost in zip(valid_moves, cost_moves):
            if move not in game.frontier:
                game.create_new_node(move, cost, state, strategy)
                # game.print_last_board()

        if not valid_moves:
            # dead end branch
            # print('dead end')
            del game.nodes[state.node_number]
            game.frontier_cost[state.parent.node_number] = state.parent.cost

        # game.get_completed_moves()
        # print('---------')
        # game.print_completed_moves()

    # print("\nGAME LOST - no solution")
    # print("\nprinting last board:\n")
    # game.print_last_board()
    print("printing tree of nodes:\n")
    game.print_tree_nodes()
    print("\nprinting tree of boards:\n")
    game.print_tree_boards()
    print("\nGAME PLAY")
    game.print_completed_moves()

def dfs(board_size: int, initial_empty_space: list[int]):
    """
    DOESNT WORK YET
    """
    game = Peg(board_size, initial_empty_space)

    print("\nSTARTING BOARD\n")
    game.print_last_board()

    # start frontier with initial state
    game.frontier.append(game.initial_state)

    while game.frontier:
        # get last state in frontier and add to expanded_states
        state = game.frontier.pop()
        game.expanded_states.append(state.board)

        # check how many pins are left accounting for the lower triangle of the array
        if (state.board == 1).sum() == 1 + (game.board_size * (game.board_size - 1))/2:
            game.get_completed_moves(game.nodes[list(game.nodes.keys())[-1]])
            print((state.board==1).sum())
            print("\n\n---GAME WON---")
            # print("printing tree of nodes:\n")
            # game.print_tree_nodes()
            # print("\nprinting tree of boards:\n")
            # game.print_tree_boards()
            print("LAST BOARD\n")
            game.print_last_board()
            print("\nGAME PLAY")
            game.print_completed_moves()
            return
        
        # get possible moves and if not already in frontier, create and add to frontier
        valid_moves = game.check_move(state)
        for move in valid_moves:
            if move not in game.frontier:
                game.create_new_node(move, state)

    print("\nGAME LOST - no solution")
    print("\nprinting last board:\n")
    game.print_last_board()

def bfs(board_size: int, initial_empty_space: list[int]):
    '''Bredth First Search game'''
    bfsGame = Peg(board_size, initial_empty_space)

    print("\nSTARTING BOARD\n")
    bfsGame.print_last_board()

    # start frontier with initial state
    bfsGame.frontier.appendleft(bfsGame.initial_state)
    
    while bfsGame.frontier:
        # get last state in frontier and add to start of expanded_states
        state = bfsGame.frontier.pop()
        bfsGame.expanded_states.append(state.board)

        # check how many pins are left accounting for the lower triangle of the array
        if (state.board == 1).sum() == 1 + (bfsGame.board_size * (bfsGame.board_size - 1))/2:
            bfsGame.get_completed_moves(bfsGame.nodes[list(bfsGame.nodes.keys())[-1]])
            print((state.board==1).sum())
            print("\n\n---GAME WON---")
            # print("printing tree of nodes:\n")
            # game.print_tree_nodes()
            # print("\nprinting tree of boards:\n")
            # game.print_tree_boards()
            print("LAST BOARD\n")
            bfsGame.print_last_board()
            print("\nGAME PLAY")
            bfsGame.print_completed_moves()
            return
        
        # get possible moves and if not already in frontier, create and add to frontier
        valid_moves = bfsGame.check_move(state)
        for move in valid_moves:
            if move not in bfsGame.frontier:
                bfsGame.create_new_node(move, state)

    print("\nGAME LOST - no solution")
    print("\nprinting last board:\n")
    bfsGame.print_last_board()

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
    board_size = 4
    empty_space = [0, 0]

    strategy = 'cost'

    # play game with Graph Search
    graph_search(board_size, empty_space, strategy)
