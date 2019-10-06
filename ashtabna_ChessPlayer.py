'''
CPSC 415 -- Homework #3 chess strategy
Sandra Shtabnaya, University of Mary Washington, fall 2019
'''
import random
from chess_player import ChessPlayer
from copy import deepcopy
import bisect

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
        return self.minimax(tree.root, float("-inf"), float("inf"), tree.MAX_DEPTH)[1]

    def minimax(self, state, alpha, beta, depth):

        best_move = state.move

        # if leaf node or endgame
        if depth == 0 or state.state.is_king_in_checkmate(state.color):
            return state.eval, best_move

        if state.color == MAX:
            best_child = float("-inf")
            for child in state.children:
                eval = self.minimax(child, alpha, beta, depth - 1)[0]
                best_child = max(best_child, eval) # stores largest child value
                alpha = max(alpha, eval)

                # if this child is better
                if alpha == eval:
                    best_move = child.move

                if beta <= alpha:
                    break # prune

            return best_child, best_move

        else:
            best_child = float("inf")
            for child in state.children:
                eval = self.minimax(child, alpha, beta, depth - 1)[0]
                best_child = min(best_child, eval) # stores smallest child value
                beta = min(beta, eval)

                # if this child is better
                if beta == eval:
                    best_move = child.move

                if alpha >= alpha:
                    break # prune

            return best_child, best_move

def eval(state, player):
    return piece_count(state, player)

def piece_count(state, player):
    count = 0
    for square, piece in state.items():
        piece_notation = piece.get_notation()
        if piece_notation.isupper() and player == "white":
            count += 1
        elif piece_notation.islower() and player == "black":
            count += 1

    return count

def negate_color(color):
    if color == "black":
        return "white"
    return "black"

# data structure for storing nodes in game tree
class State:

    # default is no parent (root)
    def __init__(self, board, color, parent=None, move=None, eval=0):
        self.state = board
        self.parent = parent
        self.move = move # stores the move that created this state
        self.eval = eval
        self.color = color
        self.children = []

    # adds child in order
    def add_child(self, child):
        bisect.insort(self.children, child)

    # defines how to sort states
    def __lt__(self, other):
        return self.eval < other.eval


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
        for move in moves[0:5]:
            board = deepcopy(root.state)
            board.make_move(move[0], move[1])
            state_eval = eval(board, root.color)
            color = negate_color(root.color)
            child = State(board, color, root, move, state_eval)
            root.add_child(child)

        depth += 1

        for child in root.children:
            self.build(child, child.state.get_all_available_legal_moves(negate_color(root.color)), depth)