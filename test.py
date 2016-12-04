from domino import NegaMax, ZeroSumGame
import random

class WeirdGame(ZeroSumGame):
    def __init__(self, nums=10):
        self.pile = nums
    def is_end(self):
        return self.pile==0
    def evaluate(self, player):
        return -1*self.is_end()
    def possible_actions(self, player):
        return [1,self.pile/2]
    def make_move(self, player, move):
        self.pile -= move
    def undo_move(self, player, move):
        self.pile += move
    def get_next_player(self, player):
        return 1^player


alpha = -1000
beta = 1000
DEPTH = 40

random.seed(1)

for i in range(100):
    game = WeirdGame(random.randint(0,100))
    nm = NegaMax(game)

    while not game.is_end():
        print 'current pile {}'.format(game.pile)
        c = 1
        if c not in game.possible_actions(0):
            print 'how about no'
            continue
        game.make_move(0, c)
        if game.is_end():
            print 'you win, asshole'
            break
        # move, score = nm.negamax(DEPTH, 0)
        move, score = nm.negamax_ab(DEPTH, alpha, beta, 0)
        # print 'normal score = {} | ab score = {}'.format(score, ab_score)
        print 'performing move {} with score {}'.format(move, score)
        # assert score == ab_score
        game.make_move(0, move)
        if game.is_end():
            print 'I win, you suck'
            break
