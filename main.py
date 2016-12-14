from domino import Dominoes, Domino
import random
from algorithms.p_negamax import ProbabilisticNegaMax
from copy import deepcopy
from numpy.random import choice

PASS_STR = 'PASS'
PASS_DOMINO = Domino(-1,-1)

# Controller
def setupGame():
    '''
    Enter the tiles that I have.
    Enter who is starting the game.
    A little bit of checking about validity of inputs
    and organizing/standardizing/cleaning
    but please don't input something too crazy.
    @returns
        - Dominoes
    '''
    print 'Welcome.'
    tiles = []
    for i in range(7):
        for j in range(i, 7):
            tiles.append((i, j))
    while True:
        my_tiles_input = raw_input('Enter one computer\'s tiles (e.g. 45) seperated by spaces: ').split()
        if len(my_tiles_input) == 7:
            break
        else:
            print "I need 7 tiles!"
    my_tiles = []
    for t in my_tiles_input:
        my_tiles.append(tuple([int(num) for num in t]))
    print 'I have:', my_tiles
    print
    while True:
        other_tiles_input = raw_input('Enter other computer\'s tiles (e.g. 45) seperated by spaces: ').split()
        if len(other_tiles_input) == 7:
            break
        else:
            print "I need 7 tiles!"
    other_tiles = []
    for t in other_tiles_input:
        other_tiles.append(tuple([int(num) for num in t]))
    print 'I have:', other_tiles
    print
    print 'Players are numbered as the following:'
    print '(0 = me, 1 = opponent on my right,'
    print '2 = partner across from me, 3 = opponent on my left)'
    while True:
        starter = int(raw_input('Who is starting? '))
        if starter < 4 and starter >= 0:
            break
        else:
            print "Not valid, try again"
    print "Player " + str(starter) + " is starting."
    print
    return (Dominoes(tiles, my_tiles, starter), Dominoes(tiles, other_tiles, (starter+2)%4))

def humanPlays(games, player):
    '''
    @params
        - games (tuple of Dominoes)
        - player (int)
    '''
    print 'Now, player ' + str(player) + ' is playing.'
    actions = games[0].possible_actions(player, False)
    while True:
        try: # lol this is dangerous
            print 'Write down your move (e.g. 23)'
            move = raw_input("").strip()
            if move == PASS_STR:
                games[0].update(PASS_DOMINO)
                games[1].update(PASS_DOMINO)
                print "You just passed."
                return
            move = list(move)
            move = tuple([int(v) for v in move])
        except KeyboardInterrupt:
            raise
        except:
            print "Something went wrong, try again"
        if (games[0].ends == [None, None]): 
            games[0].update(move)
            games[1].update(move)
            return 
        if (games[0].ends[0] in move and games[0].ends[1] in move
                and games[0].ends[0] != games[0].ends[1]):
            while True:
                print 'Specify placement for ', games[0].ends
                print '(0 for first end or 1 for second end):'
                placement = int(raw_input("").strip())
                if placement == 0 or placement == 1:
                    print "You played a " + str(move)
                    games[0].update(move, placement=placement)
                    games[1].update(move, placement=placement)
                    return
        if games[0].ends[0] in move or games[0].ends[1] in move:
            if Domino(*move) in actions:
                print "You played a " + str(move)
                games[0].update(move)
                games[1].update(move)
                return
        print "Move not valid"

def smartPlays(game, player):
    player /= 2
    curr_game = game[player]
    other_game = game[1-player]
    actions = curr_game.possible_actions(0)
    if len(actions) == 1:
        curr_game.update(actions[0][0])
        other_game.update(actions[0][0])
        print "I played a " + str(actions[0][0]) + ", yay!"
    else:
        pnm = ProbabilisticNegaMax(curr_game)
        depth = int(6*(2**(1./3*int(len(curr_game.dominos_played)/4))))
        print "DEPTH"
        print depth
        max_move, max_expectation = None, None
        for a in actions:
            curr_expectation = calculate_expectation(curr_game, depth, a)
            if max_move is None or max_expectation < curr_expectation:
                max_move, max_expectation = a, curr_expectation
                print 'new max found with expectation : {}'.format(max_expectation)

        # max_move, max_score = pnm.p_negamax(6,0)
        curr_game.update(max_move[0], placement=max_move[1])
        other_game.update(max_move[0], placement=max_move[1])
        print "I played a " + str(max_move[0]) + ", yay!"

def calculate_expectation(game, depth, move, samples=40):
    exp_total = 0.0
    remaining_dominoes = make_dominoes()
    players = range(4)
    pnm = ProbabilisticNegaMax(game)
    game.make_probabilistic_move(0, move)
    for t in game.dominos_played:
        if not t == PASS_DOMINO:
            remaining_dominoes.remove(t)
    for _ in range(samples):
        curr_dominoes = list(remaining_dominoes)
        random.shuffle(curr_dominoes)
        old_probabilities = deepcopy(game.probabilities)
        while curr_dominoes:
            curr_domino = curr_dominoes.pop()
            curr_domino_probs = game.probabilities[curr_domino]
            curr_assignment = choice(players, p=curr_domino_probs)
            game._update_probs(curr_domino, curr_assignment)
        exp_total += -pnm.p_negamax_ab(depth, depth, -float('inf'), float('inf'), 1)[1]
        game.probabilities = old_probabilities
    game.undo_move(0, move)
    exp_total /= samples
    return exp_total

def make_dominoes():
    return set(Domino(i,j) for i in range(7) for j in range(i,7))

if __name__ == '__main__':
    '''
    Plays one game.
    '''
    games = setupGame()
    while not games[0].is_end():
        player = games[0].curr_player
        humanPlays(games, player) if player%2==1 else smartPlays(games, player)
        print "Player " + str(player) + " just played, ends of tiles " + \
            "are " + str(games[0].ends[0]) + " and " + str(games[0].ends[1])
        print
    print "Game ended."
