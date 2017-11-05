from __future__ import print_function

from easyAI import TwoPlayersGame
from easyAI.Player import Human_Player
from easyAI import id_solve


class TicTacToe( TwoPlayersGame ):

    def __init__(self, players):
        self.players = players
        self.board = [['.' for j in range(9)] for i in range(9)]
        self.tally = ['.' for _ in range(9)]
        self.nplayer = 1 # player 1 starts.

    def possible_moves(self):
        return [i+1 for i,e in enumerate(self.board) if e==0]

    def make_move(self, move):
        self.board[int(move)-1] = self.nplayer

    def unmake_move(self, move): # optional method (speeds up the AI)
        self.board[int(move)-1] = 0

    def lose(self):

        return any([all([(self.tally[c-1] == self.nopponent)
                      for c in line])
                      for line in [[1, 2, 3], [4 ,5, 6], [7, 8, 9],
                                   [1, 4, 7], [2 ,5, 8], [3, 6, 9],
                                   [1, 5, 9], [3 ,5, 7]]])

    def is_over(self):
        return (self.possible_moves() == []) or self.lose()

    def show(self):

        print()

        for i in range(0, 3):
            print(self.tally[i] + ' ', end='')
        print()

        for i in range(3, 6):
            print(self.tally[i] + ' ', end='')
        print()

        for i in range(6, 9):
            print(self.tally[i] + ' ', end='')

        print()
        print()

        for i in range(0, 3):
            for j in range(0, 3):
                print(self.board[i][j] + ' ' , end='')
            print('  ', end='')
        print()

        for i in range(0, 3):
            for j in range(3, 6):
                print(self.board[i][j] + ' ' , end='')
            print('  ', end='')
        print()

        for i in range(0, 3):
            for j in range(6, 9):
                print(self.board[i][j] + ' ' , end='')
            print('  ', end='')
        print()
        print()

        for i in range(3, 6):
            for j in range(0, 3):
                print(self.board[i][j] + ' ' , end='')
            print('  ', end='')
        print()

        for i in range(3, 6):
            for j in range(3, 6):
                print(self.board[i][j] + ' ' , end='')
            print('  ', end='')
        print()

        for i in range(3, 6):
            for j in range(6, 9):
                print(self.board[i][j] + ' ' , end='')
            print('  ', end='')
        print()
        print()

        for i in range(6, 9):
            for j in range(0, 3):
                print(self.board[i][j] + ' ' , end='')
            print('  ', end='')
        print()

        for i in range(6, 9):
            for j in range(3, 6):
                print(self.board[i][j] + ' ' , end='')
            print('  ', end='')
        print()

        for i in range(6, 9):
            for j in range(6, 9):
                print(self.board[i][j] + ' ' , end='')
            print('  ', end='')
        print()
        print()

    def scoring(self):
        return -100 if self.lose() else 0


if __name__ == "__main__":

    from easyAI import AI_Player, Negamax
    ai_algo = Negamax(6)
    TicTacToe([Human_Player(), AI_Player(ai_algo)]).play()

    # r, d, m = id_solve(TicTacToe, ai_depths=range(1,9), win_score=100)

    # print r, d, m
