'''
CPSC 415 -- Homework #3 chess strategy
Sandra Shtabnaya, University of Mary Washington, fall 2019
'''
import random
from chess_player import ChessPlayer
from copy import deepcopy

MIN = None
MAX = None

class ashtabna_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        super().__init__(board, color)

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        global MAX, MIN # make assignments global
        MAX = self.color
        MIN = negate_color(MAX)
        tree = GameTree(self.board, MAX)
        tree.compute()
        return random.choice(self.board.get_all_available_legal_moves(self.color))

def negate_color(color):
    if color == "black":
        return "white"
    return "black"

# data structure for storing nodes in game tree
class State:

    # default is no parent (root)
    def __init__(self, board, color, parent=None):
        self.state = board
        self.parent = parent
        self.color = color
        self.children = []

    def add_child(self, child):
        self.children.append(child)


# data structure for computing chess game tree
class GameTree:

    def __init__(self, board, color):
        self.root = State(board, color)
        self.MAX_DEPTH = 2

    # generates game tree using initial state
    def compute(self):
        possible_moves = self.root.state.get_all_available_legal_moves(MAX)
        self.build(self.root, possible_moves, 0)

    def build(self, root, moves, depth):

        # base case
        if depth == self.MAX_DEPTH:
            return

        # adds current root's children
        # print("finding all children for " + root.color)
        for move in moves[0:5]:
            # print("can try " + str(move) + " for " + root.color)
            board = deepcopy(root.state)
            board.make_move(move[0], move[1])
            color = negate_color(root.color)
            child = State(board, color, root)
            root.add_child(child)

        depth += 1

        for child in root.children:
            self.build(child, child.state.get_all_available_legal_moves(negate_color(root.color)), depth)