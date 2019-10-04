'''
CPSC 415 -- Homework #3 chess strategy
Sandra Shtabnaya, University of Mary Washington, fall 2019
'''
import random
from chess_player import ChessPlayer

class ashtabna_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        super().__init__(board, color)

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        return random.choice(self.board.get_all_available_legal_moves(self.color))