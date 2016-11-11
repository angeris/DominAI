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

class Dominoes(object):
    def __init__(self, game_tiles, my_tiles, starter, alg):
        '''
        @params:
            - game_tiles (list of tuples of ints): each tuple has two
            values representing a domino in the game. This list contains
            all dominoes in the game. The first value is less or equal
            to the second value in the domino tuple.
            - my_tiles (list of tuples of ints): the seven dominoes
            that I begin with in the game.
            - starter (int): Who is starting the game?
            0 = me, 1 = first opp, 2 = partner, 3 = third opp.
            - alg (function): the algorithm I am using to beat humans.
        '''
        self.tiles = game_tiles
        self.my_tiles = my_tiles
        self.starter = starter
        self.moveMaker = alg

        # my tiles, tiles of opp1, tiles of partner, tiles of opp2
        self.placed_tiles = [[], [], [], []]
        # passes: me, opp1, partner, opp2
        self.passes = [set(), set(), set(), set()]

    def getKnowledge(self):
        '''
        @returns:
            - a tuple consisting of:
            placed_tiles (list of lists) and passes (list of sets)
            What tiles have been placed by whom on the table? What values
            do people not have?
        '''
        return (self.placed_tiles, self.passes)

    def startState(self):
        '''
        @return
            - a state (tuple): who is playing (int) and the open
            ends of dominoes (tuple of ints)
        '''
        return (self.starter, (6, 6))

    def actions(self, state):
        '''
        @params
            - state tuple
        @returns
            - returns possible moves (set of tuples, (domino, placement))
            that could be placed given the open ends of dominoes on the table.
        '''
        options = state[1]
        res = set()
        vals = set(options)
        for v in vals:
            for t in game.tiles:
                if t[0] == v or t[1] == v:
                    res.add((t, v))
        return res

    def isEnd(self, state):
        '''
        @params
            - state tuple
        @returns
            - Has the previous player run out of dominoes? (bool)
        '''
        player = state[0]
        return len(self.placed_tiles[player]) == 7

    def update(self, player, move, state):
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
        options = list(state[1])
        if move == 'pass':
            self.passes[player] |= set(options)
            return state
        # else
        placed_domino = move[0]
        placement = move[1]
        if placed_domino[0] == placement:
            new_end = placed_domino[1]
        else:
            new_end = placed_domino[0]
        assert (player == state[0])
        if options[0] == placement:
            options[0] = new_end
        else:
            options[1] = new_end
        state = (player, options)
        self.placed_tiles[player].append(placed_domino)
        if player == 0: # I just played, must update myself
            self.my_tiles.remove(placed_domino)
        return state
