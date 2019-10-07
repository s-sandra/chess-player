'''
CPSC 415 -- Homework #3 chess strategy
Sandra Shtabnaya, University of Mary Washington, fall 2019
'''
import random
from chess_player import ChessPlayer
from copy import deepcopy
import time
import bisect

MIN = None
MAX = None
WIN = 100000
CUT_OFF = 2
piece_values = {'k':50000, 'q':700, 's':600, 'r':500, 'b':300, 'n':300, 'f':300, 'p':100}
TIME_LIMIT = 5000 # maximum amount of time spent searching is 5 seconds (5000 milliseconds)
current_time = lambda: int(round(time.time() * 10000))
END_TIME = current_time() + TIME_LIMIT
tt = {} # transposition table

class ashtabna_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        super().__init__(board, color)

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        global MAX, MIN # make assignments global
        MAX = self.color
        MIN = negate_color(MAX)
        root = State(self.board, MAX)
        move = self.choose_move(root, TIME_LIMIT)

        if move is None:
            return random.choice(self.board.get_all_available_legal_moves(self.color))
        return move

    def choose_move(self, root, time):
        depth = 1
        end_time = current_time() + time
        best_move = None

        # iterative deepening search
        while current_time() < end_time:
            # try seeing more moves ahead, if there is time
            eval, move = self.minimax(root, float("-inf"), float("inf"), depth, end_time)
            best_move = move
            depth += 1

            if eval == WIN:
                return move

        return best_move

    def minimax(self, state, alpha, beta, depth, time_limit):

        best_move = None

        # if leaf node or endgame
        if current_time() >= time_limit or depth == 0 or state.eval == WIN:
            return state.eval, best_move

        if state.color == MAX:
            best_child = float("-inf")
            state.expand()
            for child in reversed(state.children):
                eval = self.minimax(child, alpha, beta, depth - 1, time_limit)[0]
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
            state.expand()
            for child in reversed(state.children):
                eval = self.minimax(child, alpha, beta, depth - 1, time_limit)[0]
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

def piece_count(board, player):

    if board.is_king_in_checkmate(negate_color(player)):
        return WIN

    count = 0
    for square, piece in board.items():
        piece_notation = piece.get_notation()
        value = piece_values[piece_notation.lower()]

        # piece belongs to white
        if piece_notation.isupper():
            if player == "white":
                count += value # white gets points for white piece
            else:
                count += (-1 * value) # white loses points for black piece

        else: # piece belongs to black
            if player == "white":
                count += (-1 * value) # black gets points for black piece
            else:
                count += value # black loses points for white piece

    return count

def negate_color(color):
    if color == "black":
        return "white"
    return "black"


# data structure for storing nodes in game tree
class State:

    # default is no parent (root)
    def __init__(self, board, color, parent=None, move=None, eval=0):
        self.board = board
        self.parent = parent
        self.move = move # stores the move that created this state
        self.eval = eval
        self.color = color
        self.children = []

    # adds child in ascending order
    def add_child(self, child):
        bisect.insort(self.children, child)

    def expand(self):
        moves = self.board.get_all_available_legal_moves(self.color)
        for move in moves:
            board = deepcopy(self.board)
            board.make_move(move[0], move[1])
            state_eval = eval(board, self.color)
            color = negate_color(self.color)
            child = State(board, color, self, move, state_eval)
            self.add_child(child)

    # defines how to sort states
    def __lt__(self, other):
        return self.eval < other.eval