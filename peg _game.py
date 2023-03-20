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
        self.cost = 0
        self.SAX = 0
        self.effective_slack = 0

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
    def __init__(self, board_size: int, empty_space: list[int], strategy: str):
        self.board_size: int = board_size
        self.initial_empty_space: list[int] = empty_space
        self.moves_to_win: list[State] = []
        if strategy == 'SAX':
            self.frontier: dict = {}
            self.frontier_cost: dict = {}
        else:
            self.frontier: deque = deque([])
            self.frontier_cost: deque = deque([])
        self.expanded_states: deque = deque([])
        self.won: bool = False
        self.nodes: dict = {}
        self.initial_state: State = None
        self.mid_coor = (self.board_size/4)-0.25

        ## 0 1 2 3 4 
        #0 x x x x x
        #1 x x x x
        #2 x x x
        #3 x x
        #4 x
        #

        self.create_initial_state(strategy)

    def create_initial_state(self, strategy):
        '''Instantiates the initial state and adds it to the dictionary of nodes'''
        self.initial_state = State(self.board_size)
        self.initial_state.board[self.initial_empty_space[0], self.initial_empty_space[1]] = 0
        self.initial_state.node_number = 0
        self.nodes[self.initial_state.node_number] = self.initial_state
        if strategy == 'SAX':
            self.initial_state.SAX = self.calculate_SAX(self.initial_state)

    def create_new_node(self, action: list, cost: int, parent: State, strategy: str):
        '''Creates a new instance of State and adds it to the dictionary of nodes'''
        new_state = State(self.board_size)

        # make the board from the parent and then apply the move
        new_state.parent = parent
        new_state.board = parent.board.copy()
        new_state.board = self.move(action, new_state)
        if strategy == 'SAX':
            # calculate effective slack
            new_state.SAX = self.calculate_SAX(new_state)
            new_state.effective_slack = self.initial_state.SAX - new_state.SAX
            if new_state.parent == self.initial_state:
                if self.initial_empty_space == [0,0] or self.initial_empty_space == [0, 4] or self.initial_empty_space == [4, 0]:
                    # if initial position is in a corner
                    new_state.effective_slack += 1
            new_state.cost = new_state.effective_slack
        else:
            new_state.cost = new_state.parent.cost + cost
               
        # check if state already exists
        if np.any(np.all(new_state.board == self.expanded_states, axis=1)):
             # use the dict keys to create a new node_number then add to dict
            keys = list(self.nodes.keys())
            new_state.node_number = keys[-1] + 1
            self.nodes[new_state.node_number] = new_state

            if strategy == 'dfs':
                # push
                self.frontier.append(new_state)
            elif strategy == 'bfs':
                # enqueue
                self.frontier.appendleft(new_state)
            elif strategy == 'cost':
                self.frontier.append(new_state)
                self.frontier_cost.append(new_state.cost)
            elif strategy == 'SAX':
                if new_state.effective_slack >= 0 and new_state.SAX <= new_state.parent.SAX:
                    # only add if effective slack is not negative and SAX does not increase
                    self.frontier[new_state.node_number] = new_state
                    self.frontier_cost[new_state.node_number] = (new_state.effective_slack)
            # add as child to the parent node
            parent.children[new_state.node_number] = new_state

    def calculate_SAX(self, state: State):
        board = state.board
        S = 0
        A = 0
        X = 0
        if np.count_nonzero(board[1:3, 0] == 1) >= 2: S += 1
        if np.count_nonzero(board[0, 1:3] == 1) >= 2: S +=1
        if (np.count_nonzero(board[3,1] == 1) + np.count_nonzero(board[2,2]==1)+ np.count_nonzero(board[1,3]==1)) >= 2:
            S += 1

        A = board[2, 1] + board[1, 1] + board[1, 2]
        X = board[0, 0] + board[4, 0] + board[0, 4] + board[0, 2] + board[2, 0] + board[2, 2] 
        return S + A - X
    
    def check_OoB(self, i: int, j: int):
        '''Checks if a suggested move is out of bounds (OoB)'''
        if i+j > self.board_size-1:
            return False
        else:
            return True

    def check_move(self, state: State):
        valid_moves = []
        cost_moves = []
        cost_frac = 5*len(self.moves_to_win)
        cost_corner = 10
        cost_twds_cntr = 1
        cost_away_cntr = 5
        # checking if each peg can move
        for i in range(self.board_size):
            for j in range(self.board_size):
                # checking move
                # S we want (2,0) (i,j) to print((4,0))
                if state.board[i,j] == 1 and i+2 < self.board_size and state.board[i+2,j] == 0 and state.board[i+1,j] == 1 and self.check_OoB(i, j):
                    valid_moves.append([i,j,i+1,j,i+2,j])
                    dist_to_mid_ori = math.sqrt((i-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    dist_to_mid_des = math.sqrt(((i+2)-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    if [i+2,j] == [board_size-1,0]:
                        cost_moves.append(cost_corner-cost_frac)
                    elif dist_to_mid_ori < dist_to_mid_des:
                        cost_moves.append(cost_away_cntr-cost_frac)
                    elif dist_to_mid_ori >= dist_to_mid_des:
                        cost_moves.append(cost_twds_cntr-cost_frac)
                    
                # N 
                if state.board[i,j] == 1 and i-2 >= 0 and state.board[i-2,j] == 0 and state.board[i-1,j] == 1 and self.check_OoB(i, j):
                    valid_moves.append([i,j,i-1,j,i-2,j])
                    dist_to_mid_ori = math.sqrt((i-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    dist_to_mid_des = math.sqrt(((i-2)-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    if [i-2,j] == [0,0]:
                        cost_moves.append(cost_corner-cost_frac)
                    elif dist_to_mid_ori < dist_to_mid_des:
                        cost_moves.append(cost_away_cntr-cost_frac)
                    elif dist_to_mid_ori >= dist_to_mid_des:
                        cost_moves.append(cost_twds_cntr-cost_frac)
                # E
                if state.board[i,j] == 1 and j+2 < self.board_size and state.board[i,j+2] == 0 and state.board[i,j+1] == 1 and self.check_OoB(i, j):
                    valid_moves.append([i,j,i,j+1,i,j+2])
                    dist_to_mid_ori = math.sqrt((i-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    dist_to_mid_des = math.sqrt((i-self.mid_coor)**2 + ((j+2)-self.mid_coor)**2)
                    if [i,j+2] == [0,board_size-1]:
                        cost_moves.append(cost_corner-cost_frac)
                    elif dist_to_mid_ori < dist_to_mid_des:
                        cost_moves.append(cost_away_cntr-cost_frac)
                    elif dist_to_mid_ori >= dist_to_mid_des:
                        cost_moves.append(cost_twds_cntr-cost_frac)
                # W 
                if state.board[i,j] == 1 and j-2 >= 0 and state.board[i,j-2] == 0 and state.board[i,j-1] == 1 and self.check_OoB(i, j):
                    valid_moves.append([i,j,i,j-1,i,j-2])
                    dist_to_mid_ori = math.sqrt((i-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    dist_to_mid_des = math.sqrt((i-self.mid_coor)**2 + ((j-2)-self.mid_coor)**2)
                    if [i,j-2] == [0,0]:
                        cost_moves.append(cost_corner-cost_frac)
                    elif dist_to_mid_ori < dist_to_mid_des:
                        cost_moves.append(cost_away_cntr-cost_frac)
                    elif dist_to_mid_ori >= dist_to_mid_des:
                        cost_moves.append(cost_twds_cntr-cost_frac)
                # SW
                if state.board[i,j] == 1 and i+2 < self.board_size and j-2 >= 0 and state.board[i+2,j-2] == 0 and state.board[i+1,j-1] == 1 and self.check_OoB(i, j):
                    valid_moves.append([i,j,i+1,j-1,i+2,j-2])
                    dist_to_mid_ori = math.sqrt((i-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    dist_to_mid_des = math.sqrt(((i+2)-self.mid_coor)**2 + ((j-2)-self.mid_coor)**2)
                    if [i+2,j-2] == [board_size-1,0]:
                        cost_moves.append(cost_corner-cost_frac)
                    elif dist_to_mid_ori < dist_to_mid_des:
                        cost_moves.append(cost_away_cntr-cost_frac)
                    elif dist_to_mid_ori >= dist_to_mid_des:
                        cost_moves.append(cost_twds_cntr-cost_frac)
                # NE
                if state.board[i,j] == 1 and i-2 >= 0 and j+2 < self.board_size and state.board[i-2,j+2] == 0 and state.board[i-1,j+1] == 1 and self.check_OoB(i, j):
                    valid_moves.append([i,j,i-1,j+1,i-2,j+2])
                    dist_to_mid_ori = math.sqrt((i-self.mid_coor)**2 + (j-self.mid_coor)**2)
                    dist_to_mid_des = math.sqrt(((i-2)-self.mid_coor)**2 + ((j+2)-self.mid_coor)**2)
                    if [i-2,j+2] == [0,board_size-1]:
                        cost_moves.append(cost_corner-cost_frac)
                    elif dist_to_mid_ori < dist_to_mid_des:
                        cost_moves.append(cost_away_cntr-cost_frac)
                    elif dist_to_mid_ori >= dist_to_mid_des:
                        cost_moves.append(cost_twds_cntr-cost_frac)
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
            time.sleep(0.1 )
            repr(self.initial_state.print_board(move))

def graph_search(board_size: int, initial_empty_space: list[int], strategy: str):
    '''Graph Search Game'''
    game = Peg(board_size, initial_empty_space, strategy)

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
        game.frontier_cost.append(game.initial_state.cost)
    
    elif strategy == 'SAX':
        game.frontier[game.initial_state.node_number] = game.initial_state
        game.frontier_cost[game.initial_state.node_number] = game.initial_state.cost

    # while len(game.expanded_states) < 20:
    while game.won == False:
        
        if strategy == 'dfs' or strategy =='bfs':
            # get last state in frontier (dequeue/pop)
            state = game.frontier.pop()
        
        elif strategy == 'cost':
            # get minimum cost state
            min_value = min(game.frontier_cost)
            key = game.frontier_cost.index(min_value)
            state = game.frontier[key]
            del game.frontier[key]
            del game.frontier_cost[key]

        elif strategy == 'SAX': 
            # get maximum SAX state
            list_of_costs = [max(game.frontier_cost, key=game.frontier_cost.get)]  
            cheapest_state = None
            deepest_level = 0
            for key in list_of_costs:
                temp_state = game.nodes[key]
                game.get_completed_moves(temp_state)
                level = len(game.moves_to_win)
                if level > deepest_level:
                    cheapest_state = temp_state
            state = cheapest_state
            del game.frontier[state.node_number]
            del game.frontier_cost[state.node_number]
        
        game.expanded_states.append(state.board)

        # check how many pins are left accounting for the lower triangle of the array
        if (state.board == 1).sum() == 1 + (game.board_size * (game.board_size - 1))/2:
            game.get_completed_moves(game.nodes[list(game.nodes.keys())[-1]])
            print(((state.board == 1).sum() - (game.board_size * (game.board_size - 1))/2))
            print("\n\n---GAME WON---")
            print("LAST BOARD\n")
            game.print_last_board()
            print("\nGAME PLAY")
            game.print_completed_moves()
            et = time.time()
            if strategy == 'dfs' or strategy == 'bfs':
                print('Compute time', round((et-st),2),'level: ' + str(len(game.moves_to_win)) + ' nodes visited: ' + str(len(game.expanded_states)), "current node", state.node_number, "frontier", len(game.frontier), "num pegs", (state.board == 1).sum() - (game.board_size * (game.board_size - 1))/2)
            elif strategy == 'cost' or strategy == 'SAX':
                print('Compute time', round((et-st),2),'level: ' + str(len(game.moves_to_win)) + ' nodes visited: ' + str(len(game.expanded_states)), "current node", state.node_number, "frontier", len(game.frontier), "num pegs", (state.board == 1).sum() - (game.board_size * (game.board_size - 1))/2, "current cost", state.cost)
    
            return
        else:
            game.get_completed_moves(game.nodes[list(game.nodes.keys())[-1]])
            
            if len(game.expanded_states) % 1000 == 0:
                if strategy == 'dfs' or strategy == 'bfs':
                    print('level: ' + str(len(game.moves_to_win)) + ' nodes visited: ' + str(len(game.expanded_states)), "current node", state.node_number, "frontier", len(game.frontier), "num pegs", (state.board == 1).sum() - (game.board_size * (game.board_size - 1))/2)
                elif strategy == 'cost' or strategy == 'SAX':
                    print('level: ' + str(len(game.moves_to_win)) + ' nodes visited: ' + str(len(game.expanded_states)), "current node", state.node_number, "frontier", len(game.frontier), "num pegs", (state.board == 1).sum() - (game.board_size * (game.board_size - 1))/2, "current cost", state.cost)
        
        # get possible moves and if not already in frontier, create and add to frontier
        valid_moves, cost_moves = game.check_move(state)
        for move, cost in zip(valid_moves, cost_moves):
            game.create_new_node(move, cost, state, strategy)

        if not valid_moves:
            # dead end branch
            del game.nodes[state.node_number]

    print("\nGAME LOST - no solution")
    print("\nprinting last board:\n")
    game.print_last_board()

if __name__ == "__main__":
    ## 0 1 2 3 4 
    #0 x x x x x
    #1 x x x x
    #2 x x x
    #3 x x
    #4 x
    
    sys.setrecursionlimit(2000)

    board_size = 5
    empty_space = [0, 0]
    stategies = ['dfs', 'bfs', 'cost', 'SAX']
    st = time.time()

    graph_search(board_size, empty_space, stategies[0])
