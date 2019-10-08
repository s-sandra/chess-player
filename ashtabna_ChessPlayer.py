'''
CPSC 415 -- Homework #3 chess strategy
Sandra Shtabnaya, University of Mary Washington, fall 2019
'''
import random
import math
from chess_player import ChessPlayer
from copy import deepcopy
import time
import bisect

piece_values = {'k':50000, 'q':700, 's':600, 'r':500, 'b':300, 'n':300, 'f':300, 'p':100}
WIN = 100000
z_table = None # table of zobrist keys
t_table = {} # transposition table

class ashtabna_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        super().__init__(board, color)
        self.MIN = None
        self.MAX = None
        self.TIME_LIMIT = 5000 # maximum amount of time spent searching is 5 seconds (5000 milliseconds)
        self.current_time = lambda: int(round(time.time() * 10000))
        self.END_TIME = self.current_time() + self.TIME_LIMIT
        self.make_zobrist_table()

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        self.MAX = self.color
        self.MIN = negate_color(self.MAX)
        root = State(self.board, self.MAX)
        move = self.choose_move(root, self.TIME_LIMIT)

        if move is None:
            return random.choice(self.board.get_all_available_legal_moves(self.color))
        return move

    def make_zobrist_table(self):
        global z_table
        piece_count = len(self.board)
        cell_count = (piece_count / 4)**2
        row_count = int(math.sqrt(cell_count))
        # 16 different kinds of pieces, row_count by row_count sized board
        z_table = [[[random.randint(1, 2 ** cell_count - 1) for i in range(16)] for j in range(row_count + 1)] for k in range(row_count + 1)]

    def choose_move(self, root, time):
        depth = 0
        end_time = self.current_time() + time
        best_move = None

        # iterative deepening search
        while self.current_time() < end_time:
            # try seeing more moves ahead, if there is time
            eval, move = self.minimax(root, float("-inf"), float("inf"), depth, end_time)
            best_move = move
            depth += 1

            if eval == WIN:
                return move

        return best_move

    def minimax(self, state, alpha, beta, depth, time_limit):

        global t_table
        best_move = None
        z_key = generate_zobrist_key(state.board)

        # if leaf node or endgame
        if self.current_time() >= time_limit or depth == 0 or state.eval == WIN:
            t_table[z_key] = HashEntry(best_move, state.eval, "EXACT", depth)
            return state.eval, best_move

        if z_key in t_table: # if we've already evaluated this chess board before
            entry = t_table[z_key]

            if entry.depth >= depth:
                if entry.type == "MAX":
                    if entry.score > alpha:
                        alpha = entry.score
                elif entry.type == "MIN":
                    if entry.score < beta:
                        beta = entry.score
                else:
                    return entry.score, entry.move

        if state.color == self.MAX:
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
                    t_table[z_key] = HashEntry(best_move, best_child, "MAX", depth)
                    break # prune

            t_table[z_key] = HashEntry(best_move, best_child, "EXACT", depth)
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

                if beta <= alpha:
                    t_table[z_key] = HashEntry(best_move, best_child, "MIN", depth)
                    break # prune

        t_table[z_key] = HashEntry(best_move, best_child, "EXACT", depth)
        return best_child, best_move


def generate_zobrist_key(board):
    key = 0
    for square, piece in board.items():
        piece_notation = piece.get_notation()
        row = ord(square[0]) - 97
        col = int(square[1])
        piece_val = index_for(piece_notation)
        key ^= z_table[row][col][piece_val]
    return key

def index_for(piece):
    if piece == 'P':
        return 0
    elif piece == 'p':
        return 8
    elif piece == 'N':
        return 1
    elif piece == 'n':
        return 9
    elif piece == 'B':
        return 2
    elif piece == 'b':
        return 10
    elif piece == 'R':
        return 3
    elif piece == 'r':
        return 11
    elif piece == 'S':
        return 4
    elif piece == 's':
        return 12
    elif piece == 'f':
        return 13
    elif piece == 'F':
        return 5
    elif piece == 'Q':
        return 6
    elif piece == 'q':
        return 14
    elif piece == 'K':
        return 7
    elif piece == 'k':
        return 15
    else:
        return -1

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


# data structure for transposition table entry
class HashEntry:

    def __init__(self, move, eval, type, depth):
        self.move = move
        self.score = eval
        self.type = type
        self.depth = depth


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
        key = generate_zobrist_key(child.board)
        if key in t_table: # children we've already evaluated should be ordered first
            self.children.append(child)
        else:
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