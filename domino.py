from copy import copy, deepcopy
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
        if other is None: return False
        if other == PASS_STR or other == PASS_DOMINO:
            return self.vals[0] < 0
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
    if total <= 0: raise ZeroDivisionError('Array is not normalizable')
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
        self.starter = starter

        self.dominos_played = []
        self.dominos_played.append(Domino(*start_tile))
        self.last_play = 0

        self.ends = [start_tile[0], start_tile[1]]

        u_third = [0,1./3,1./3,1./3]    # starting probabilities of tiles I don't have
        u_one = [1,0,0,0]   # probabilities of tiles I do have

        self.probabilities = {d:(copy(u_third) if d not in self.my_tiles else
                                 copy(u_one)) for d in self.tiles}

        self._update_probs(self.dominos_played[0], starter)

        self.curr_player = (starter+1)%4
        self.tiles.remove(self.dominos_played[0])

        # push and pop from this to get dictionaries of changed probabilities during negamax
        self.undoable_probs = []
        self.undoable_ends = [] # list of old self.ends

    def is_end(self):
        '''
        @returns: is the game over?
        '''
        # check if player has placed all dominoes:
        for i in range(4):
            if self._dom_played(i)==7:
                return True
        if len(self.tiles) == 0:
            return True
        if self.last_play > 3:
            # everyone has passed
            return all(map(lambda x:x==PASS_DOMINO,
                       self.dominos_played[self.last_play-3:self.last_play+1]))
        return False

    def make_probabilistic_move(self, player, move):
        placement = move[1]
        move = move[0]
        assert isinstance(move, Domino)
        self.undoable_ends.append(copy(self.ends))
        prob_of_move = self._assign_prob(move, player)
        self.undoable_probs.append(deepcopy(self.probabilities))
        self.update(move, player, placement)
        return prob_of_move

    def undo_move(self, player, move):
        move = move[0]
        self.dominos_played.pop()
        if move != PASS_DOMINO:
            self.tiles.add(move)
        self.probabilities = self.undoable_probs.pop()
        self.ends = self.undoable_ends.pop()
        self.curr_player = player
        self.last_play -= 1

    def possible_actions(self, curr_player=None, placements_included=True):
        '''
        @returns
            - returns possible moves (list of tuples, Dominos + placement int)
            that could be performed given the open ends of dominoes on the table.
        '''
        if curr_player is None:
            curr_player = self.curr_player
        possible_moves = []
        for t in self.tiles:
            if self._is_valid(t) and self.probabilities[t][curr_player] > 0:
                if placements_included:
                    if not (self.ends[0] in t)^(self.ends[1] in t) \
                            & (self.ends[0] != self.ends[1]):
                                possible_moves.append((t, 0))
                                possible_moves.append((t, 1))
                    else:
                        possible_moves.append((t, None))
                else:
                    possible_moves.append(t)
        if not possible_moves:
            return [(PASS_DOMINO, None)] if placements_included else [PASS_DOMINO]
        return possible_moves

    def evaluate(self, player):
        expectation_opp = 0
        expectation_us = 0
        for d in self.probabilities:
            if d not in self.dominos_played:
                probs = self.probabilities[d]
                value = sum(d.vals)
                expectation_opp += value*probs[(player + 1)%4] + value*probs[(player + 3)%4]
                expectation_us += value*probs[player] + value*probs[(player + 2)%4]
        # p_total = self._count_pieces(player)
        return expectation_opp - expectation_us #+ 6*(p_total[1] - p_total[0])

    def _count_pieces(self, player):
        rel_players = [(player + i - self.starter)%4 for i in range(4)]
        pieces_player = [self._dom_played(self.dominos_played[p::4]) for p in rel_players]
        return (pieces_player[0] + pieces_player[2], pieces_player[1] + pieces_player[3])

    def get_next_player(self, player):
        return (player + 1) % 4

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
        return self.probabilities[domino][player] if domino in self.probabilities else 1

    def probability_actions(self, curr_player=None):
        if curr_player is None:
            curr_player = self.curr_player
        possible_moves = self.possible_actions(curr_player)
        def ap(d):
            return (d, self._assign_prob(d[0], curr_player))
        return map(ap, possible_moves)

    def _dom_played(self, l):
        l = self.dominos_played[(l-self.starter)%4::4]
        return sum(map(lambda x:x!=PASS_DOMINO, l))

    def _get_score(self, player):
        # Gets opposing team score
        expectation_opp = 0
        for d in self.probabilities:
            if d not in self.dominos_played:
                probs = self.probabilities[d]
                value = sum(d.vals)
                expectation_opp += value*(probs[(player+1)%4]+probs[(player+3)%4])
        return expectation_opp

    def win_score(self, player):
        if not self.is_end():
            return False
        # rel_players = [(player + i - self.starter)%4 for i in range(4)]
        # for i, p in enumerate(rel_players):
            # if self._dom_played(self.dominos_played[p::4]) == 7:
                # return (1-2*((player-i)%2==0))*self._get_score(i)
        player_me = player
        player_teammate = (player+2)%4
        player_opp1 = (player+1)%4
        player_opp2 = (player+3)%4

        if self._dom_played(player_me)==7 or self._dom_played(player_teammate)==7:
            return self._get_score(player_me)
        if self._dom_played(player_opp1)==7 or self._dom_played(player_opp2)==7:
            return -self._get_score(player_opp1)

    def _update_probs(self, move, curr_player):
        def uncertain(d):
            return d != [1, 0, 0, 0] and d != [0, 1, 0, 0] \
                and d != [0, 0, 1, 0] and d != [0, 0, 0, 1]
        if move == PASS_DOMINO:
            possible_moves = self.possible_actions(placements_included=False)
            for t in possible_moves:
                if t != PASS_DOMINO and self.probabilities[t][curr_player] != 1:
                    self.probabilities[t][curr_player] = 0
                    self.probabilities[t] = _renormalize(self.probabilities[t])
        else:
            self.probabilities[move] = [0]*4
            self.probabilities[move][curr_player] = 1
        slots_per_person = {} # open slots per person
        for i in range(1, 4):
            played = self.dominos_played[(i - self.starter)%4::4]
            slots_per_person[i] = 7 - len(played) + played.count(PASS_DOMINO)
        for d in self.probabilities:
            if uncertain(self.probabilities[d]):
                for i in range(1, 4):
                    if self.probabilities[d][i] > 0:
                        self.probabilities[d][i] = slots_per_person[i]
                self.probabilities[d] = _renormalize(self.probabilities[d])

    def update(self, move, curr_player=None, placement=None):
        '''
        @params
            - move (tuple): valid move e.g. (2, 3) or 'PASS'/(-1, -1)
            - placement: if there are multiple options for placement
            specify which index
        '''
        if curr_player is None: curr_player = self.curr_player
        assert(curr_player == self.curr_player)
        if type(move) == tuple:
            move = Domino(*move)
        assert isinstance(move, Domino)
        '''
        warning/note:
        domino updating
        '''
        if move == PASS_DOMINO:
            self.dominos_played.append(PASS_DOMINO)
        else:
            assert self._is_valid(move)
            self.dominos_played.append(move)
            if placement is None:
                assert (self.ends[0] in move)^(self.ends[1] in move) \
                    &(self.ends[0] != self.ends[1]), "Placement"
                if self.ends[0] in move:
                    self.ends[0] = move._get_other(self.ends[0])
                else:
                    self.ends[1] = move._get_other(self.ends[1])
            else:
                self.ends[placement] = move._get_other(self.ends[placement])
            self.tiles.remove(move)
        self._update_probs(move, curr_player)
        self.curr_player = (curr_player+1)%4
        self.last_play += 1

    def is_equal(self, other):
        for i in range(len(self.dominos_played)):
            assert self.dominos_played[i] == other.dominos_played[i], "dominos_played don't match"
        for i in self.tiles:
            assert i in other.tiles, "tiles don't match"
        assert self.last_play == other.last_play, "last plays don't match"
        assert self.ends == other.ends, "ends don't match"
        assert self.curr_player == other.curr_player, "curr_players don't match"
        assert self.undoable_ends == other.undoable_ends, "undoable ends don't match"
        assert self.undoable_probs == other.undoable_probs, "undoable probs don't match"
        for d in self.probabilities:
            assert self.probabilities[d] == other.probabilities[d], 'probabilities don\'t match'

if __name__ == '__main__':
    '''
    Just for simulating a game and checking that I am not a total mess
    '''

    game_tiles = []
    for i in range(7):
        for j in range(i, 7):
            game_tiles.append((i, j))
    my_tiles_input = ['12', '34', '22', '00', '55', '33', '23']
    my_tiles = []
    for t in my_tiles_input:
        my_tiles.append(tuple([int(num) for num in t]))
    starter = 3
    start_tile = (6, 6)
    test = Dominoes(game_tiles, my_tiles, starter, start_tile)
    pnm = ProbabilisticNegaMax(test)
    max_move, max_score = pnm.p_negamax(6, 0)
    print max_move

    # print test.curr_player
    # c = deepcopy(test)
    # prob = test.make_probabilistic_move(3, (PASS_DOMINO,None))
    # print test.curr_player
    # prob = test.make_probabilistic_move(0, (Domino(4, 6), None))
    # print test.curr_player
    # test.undo_move(0, (Domino(4,6), None))
    # print test.curr_player
    # test.undo_move(3, (PASS_DOMINO, None))
    # print test.curr_player
    # c.is_equal(test)

