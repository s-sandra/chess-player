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
CUT_OFF = 2

class ashtabna_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        super().__init__(board, color)

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        global MAX, MIN # make assignments global
        MAX = self.color
        MIN = negate_color(MAX)
        root = State(self.board, MAX)
        return self.minimax(root, float("-inf"), float("inf"), CUT_OFF)[1]

    def minimax(self, state, alpha, beta, height):

        best_move = state.move

        # if leaf node or endgame
        if height == 0 or state.state.is_king_in_checkmate(state.color):
            return state.eval, best_move

        if state.color == MAX:
            best_child = float("-inf")
            state.add_children(state.state.get_all_available_legal_moves(MAX))
            for child in reversed(state.children):
                eval = self.minimax(child, alpha, beta, height - 1)[0]
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
            state.add_children(state.state.get_all_available_legal_moves(MIN))
            for child in reversed(state.children):
                eval = self.minimax(child, alpha, beta, height - 1)[0]
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

    # adds child in ascending order
    def add_child(self, child):
        bisect.insort(self.children, child)

    def add_children(self, moves):
        for move in moves:
            board = deepcopy(self.state)
            board.make_move(move[0], move[1])
            state_eval = eval(board, self.color)
            color = negate_color(self.color)
            child = State(board, color, self, move, state_eval)
            self.add_child(child)

    # defines how to sort states
    def __lt__(self, other):
        return self.eval < other.eval