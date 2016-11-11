from copy import copy


'''
Initial implementation of the dominoes game.

There are likely better ways of organizing/passing/storing
information about the current state of the game and memory of
the game. (should/will edit for p-progress/p-final)

In general, the following indices/ints correspond to the following
players: 0 = me, 1 = first opp, 2 = partner, 3 = third opp.
In the game, I sit opposite my partner and we play counter-clockwise,
hence this numbering of players.
'''
class Domino():
    def __init__(self, a, b):
        self.vals = (a,b) if a<b else (b,a)
        self.curr_hash = hash(self.vals)
    def __hash__(self):
        return self.curr_hash
    def __eq__(self, other):
        return self.vals == other.vals
    def __leq__(self, other):
        if self.vals[0] < 0:
            raise Exception('Why are you doing this')
        return self.vals[0]+self.vals[1] <= other.vals[0]+other.vals[1]
    def __str__(self, other):
        return str(self.vals) if self.vals[0] >= 0 else 'PASS'
    def __contains__(self, a):
        return a in self.vals
    def _get_other(self, a):
        # For now (while debugging)
        assert a in self
        return self.vals[0] if self.vals[1]==a else self.vals[1]


PASS_DOMINO = Domino(-1,-1)
PASS_STR = 'PASS'

def _renormalize(arr):
    total = sum(arr)
    if total <= 0: raise ZeroDivisonError('Array is not normalizable')
    total = float(total)
    return map(lambda x:x/total, arr)
class Dominoes(object):
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
            - alg (function): the algorithm I am using to beat humans.
        '''
        assert 0 <= starter <= 3

        self.tiles = set(map(lambda x:Domino(*x), game_tiles))
        self.my_tiles = set(map(lambda x:Domino(*x), my_tiles))

        self.dominos_played = [None for i in range(self.tiles)]
        self.dominos_played[0] = Domino(*self.start_tile)
        self.last_play = 0

        self.ends = [start_tile[0], start_tile[1]]

        u_third = [0,1./3,1./3,1./3]
        u_one = [1,0,0,0]

        self.probabilities = {d:(copy(u_third) if d not in self.my_tiles else
                                 copy(u_one)) for d in self.tiles}

        self.curr_player = (starter+1)%4


    def get_player(self, curr_play):
        return (idx + self.starter) % 4

    def actions(self):
        '''
        @params
            - state tuple
        @returns
            - returns possible moves (set of tuples, (domino, placement))
            that could be placed given the open ends of dominoes on the table.
        '''
        possible_moves = []
        for t in self.tiles:
            if (self.ends[0] in t or self.ends[1] in t) and self.probabilities[t][self.curr_player] > 0:
                possible_moves.append(t)
        return possible_moves

    def is_end(self):
        '''
        @params
            - state tuple
        @returns
            - Has the previous player run out of dominoes? (bool)
        '''
        if len(self.tiles)==0:
            return True
        if self.last_play >= 3:
            return all(map(lambda x:x==PASS_DOMINO,
                           self.dominos_played[self.last_play-3:self.last_play+1]))
        return False

    def _is_valid(self, t):
        return self.ends[0] in t or self.ends[1] in t

    def update(self, move, placement=None):
        '''
        @params
            - move (tuple): valid move e.g. ((2, 3), 3) or 'pass'
            In example, (2, 3) is a domino and 3 is the end you
            wish to attach to the dominoes on the table.
            - player (int)
            - state (tuple)
        @returns
            - state, with open ends of dominoes on table modified
            as necessary
        '''
        move = Domino(*move)
        if move == PASS_STR or move == PASS_DOMINO:
            possible_moves = self.actions()
            for t in possible_moves:
                self.probabilities[t][self.curr_player] = 0
                _renormalize(self.probabilities[t])
            self.dominos_played.append(PASS_DOMINO)
        else:
            assert self._is_valid(move)
            self.dominos_played.append(move)
            self.probabilities[t][self.curr_player] = 1
            _renormalize(self.probabilities[t])
            if placement is None:
                assert (self.ends[0] in move)^(self.ends[1] in move)
                if self.ends[0] in move:
                    self.ends[0] = move._get_other(self.ends[0])
                else:
                    self.ends[1] = move._get_other(self.ends[1])
            else:
                self.ends[placement] = move._get_other(self.ends[placement])


        self.curr_player = (self.curr_player+1)%4
        self.last_play += 1


