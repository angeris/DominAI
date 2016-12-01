from copy import copy
from itertools import product
from algorithms.negamax import ZeroSumGame, NegaMax
from algorithms.p_negamax import ZeroSumBayesGame, ProbabilisticNegaMax

'''
Implemention of game, version 2.0

In general, the following indices/ints correspond to the following
players: 0 = me, 1 = first opp, 2 = partner, 3 = third opp.
'''

PASS_STR = 'PASS'

class Domino():
    def __init__(self, a, b):
        '''
        @params 
            - a, b: values on a domino
        A domino's values are always in increasing order
        '''
        self.vals = (a,b) if a<b else (b,a)
        self.curr_hash = hash(self.vals)
    def __hash__(self):
        return self.curr_hash
    def __eq__(self, other):
        if other == PASS_STR: return self.vals[0] < 0
        return self.vals == other.vals
    def __leq__(self, other):
        if self.vals[0] < 0:
            # domino is a pass domino
            raise Exception('Why are you doing this')
        return self.vals[0]+self.vals[1] <= other.vals[0]+other.vals[1]
    def __str__(self):
        return str(self.vals) if self.vals[0] >= 0 else PASS_STR
    def __contains__(self, a):
        return a in self.vals
    def _get_other(self, a):
        # For now (while debugging)
        assert a in self
        return self.vals[0] if self.vals[1]==a else self.vals[1]
    def __repr__(self):
        return str(self)

PASS_DOMINO = Domino(-1,-1)
MACHINE_TEAM = 0

def _renormalize(arr):
    '''
    @param
        - arr (list): probabilities that needs to be renormalized
    '''
    total = sum(arr)
    if total <= 0: raise ZeroDivisonError('Array is not normalizable')
    total = float(total)
    return map(lambda x:x/total, arr)


class Dominoes(ZeroSumBayesGame):
    def __init__(self, game_tiles, my_tiles, starter, start_tile):
        '''
        @params:
            - game_tiles (set of tuples of ints): each tuple has two
            values representing a domino in the game. This list contains
            all dominoes in the game. The first value is less or equal
            to the second value in the domino tuple.
            - my_tiles (list of tuples of ints): the seven dominoes
            that I begin with in the game.
            - starter (int): Who is starting the game?
            0 = me, 1 = first opp, 2 = partner, 3 = third opp.
            - start_tile (tuples of int): the starting tile in the game
        '''
        assert 0 <= starter <= 3

        self.tiles = set(map(lambda x:Domino(*x), game_tiles))
        self.my_tiles = set(map(lambda x:Domino(*x), my_tiles))

        self.dominos_played = [None for i in range(len(self.tiles))]
        self.dominos_played[0] = Domino(*start_tile)
        self.last_play = 0

        self.ends = [start_tile[0], start_tile[1]]

        u_third = [0,1./3,1./3,1./3]    # starting probabilities of tiles I don't have
        u_one = [1,0,0,0]   # probabilities of tiles I do have

        self.probabilities = {d:(copy(u_third) if d not in self.my_tiles else
                                 copy(u_one)) for d in self.tiles}

        self.probabilities[self.dominos_played[0]] = [0]*4
        self.probabilities[self.dominos_played[0]][starter] = 1

        self.curr_player = (starter+1)%4
        self.tiles.remove(self.dominos_played[0])

    def is_end(self):
        '''
        @returns: is the game over?
        '''
        if len(self.tiles)==0:
            return True
        if self.last_play >= 3:
            # everyone has passed
            return all(map(lambda x:x==PASS_DOMINO,
                           self.dominos_played[self.last_play-3:self.last_play+1]))
        return False

    def make_probabilistic_move(self, player, move):
        raise NotImplemented('literally what the fuck')
        
    def undo_move(self, player, move):
        raise NotImplemented('literally what the fuck')

    def possible_actions(self, curr_player=None):
        '''
        @returns
            - returns possible moves (list of Dominos)
            that could be placed given the open ends of dominoes on the table.
        '''
        if curr_player is None:
            curr_player = self.curr_player
        if curr_player == 0:
            possible_moves = []
            for t in self.my_tiles:
                if self._is_valid(t) and self.probabilities[t][self.curr_player] > 0:
                    possible_moves.append(t)
            return possible_moves + [PASS_DOMINO]

        possible_moves = []
        for t in self.tiles:
            if self._is_valid(t) and self.probabilities[t][self.curr_player] > 0:
                possible_moves.append(t)
        return possible_moves + [PASS_DOMINO]

    def evaluate(self, player):
        raise NotImplemented('literally what the fuck')

    def get_next_player(self, player):
        return (self.curr_player+1)%4

    def debugging_fml(self):
        # prints things so that I can see everything that is wrong
        print "Tiles left:"
        print self.tiles
        print "\nDominos_played:"
        print self.dominos_played
        print "\nEnds on table:"
        print self.ends
        print "\nProbabilities:"
        for d in self.probabilities:
            print d, self.probabilities[d]
        print "\nCurrent player:"
        print self.curr_player
        print


    def get_player(self, curr_play):
        '''
        @param
            - curr_play: index of dominos_played. 0 at the beginning of the game
        '''
        return (curr_play + self.starter) % 4

    def _is_valid(self, t):
        '''
        @returns: is the move valid?
        '''
        return self.ends[0] in t or self.ends[1] in t

    def _assign_prob(self, domino, player):
        return self.probabilities[domino][player] if domino is not None else 1

    def probability_actions(self, curr_player=None):
        if curr_player is None:
            curr_player = self.curr_player
        possible_moves = self.actions(curr_player)
        def ap(d):
            return (d, self._assign_prob(d, curr_player))
        return map(ap, possible_moves)

    def win(self, team):
        if not self.is_end():
            return False

    def update(self, move, placement=None):
        '''
        @params
            - move (tuple): valid move e.g. (2, 3) or 'PASS'/(-1, -1)
            - placement: if there are multiple options for placement
            specify which index
        '''
        if type(move) == tuple:
            move = Domino(*move)
        assert type(move)==Domino
        if move == PASS_DOMINO:
            possible_moves = self.actions()
            for t in possible_moves:
                self.probabilities[t][self.curr_player] = 0
                self.probabilities[t] = _renormalize(self.probabilities[t])
            self.dominos_played[self.last_play + 1] = PASS_DOMINO
        else:
            assert self._is_valid(move)
            self.dominos_played[self.last_play + 1] = move
            self.probabilities[move] = [0]*4
            self.probabilities[move][self.curr_player] = 1
            if placement is None:
                assert (self.ends[0] in move)^(self.ends[1] in move)&(self.ends[0] != self.ends[1])
                if self.ends[0] in move:
                    self.ends[0] = move._get_other(self.ends[0])
                else:
                    self.ends[1] = move._get_other(self.ends[1])
            else:
                self.ends[placement] = move._get_other(self.ends[placement])
            self.tiles.remove(move)
        self.curr_player = (self.curr_player+1)%4
        self.last_play += 1

