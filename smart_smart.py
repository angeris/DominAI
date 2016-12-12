from domino import Dominoes, Domino
from algorithms.p_negamax import ProbabilisticNegaMax
import random
from copy import deepcopy
import sys
from numpy.random import choice

PASS_STR = 'PASS'
PASS_DOMINO = Domino(-1,-1)

def newSmartPlays(game, tiles, player):
    curr_game = game[player]
    actions = curr_game.possible_actions(0)
    if len(actions) == 1:
        for g in games:
            g.update(actions[0][0])
        print "I played a " + str(actions[0][0]) + ", yay!"
        if not actions[0][0] == PASS_DOMINO:
            tiles[player].remove(actions[0][0])
    else:
        pnm = ProbabilisticNegaMax(curr_game)
        depth = int(5*(2**(1./3*int(len(curr_game.dominos_played)/4))))
        print "DEPTH"
        print depth
        max_move, max_expectation = None, None
        for a in actions:
            curr_expectation = calculate_expectation(curr_game, depth, a)
            if max_move is None or max_expectation < curr_expectation:
                max_move, max_expectation = a, curr_expectation
                print 'new max found with expectation : {}'.format(max_expectation)
        # max_move, max_score = pnm.p_negamax(6,0)
        for g in games:
            g.update(max_move[0], placement=max_move[1])
        print "I played a " + str(max_move[0]) + ", yay!"
        if not max_move[0] == PASS_DOMINO:
            tiles[player].remove(max_move[0])
    return tiles

def oldSmartPlays(game, tiles, player):
    curr_game = game[player]
    actions = curr_game.possible_actions(0)
    if len(actions) == 1:
        for g in games:
            g.update(actions[0][0])
        print "I played a " + str(actions[0][0]) + ", yay!"
        if not actions[0][0] == PASS_DOMINO:
            tiles[player].remove(actions[0][0])
    else:
        pnm = ProbabilisticNegaMax(curr_game)
        depth = int(5*(2**(1./3*int(len(curr_game.dominos_played)/4))))
        print "DEPTH"
        print depth
        max_move, max_score = pnm.p_negamax_ab(depth, depth, -float("inf"), float("inf"), 0)
        # max_move, max_score = pnm.p_negamax(6,0)
        for g in games:
            g.update(max_move[0], placement=max_move[1])
        print "I played a " + str(max_move[0]) + ", yay!"
        if not max_move[0] == PASS_DOMINO:
            tiles[player].remove(max_move[0])
    return tiles

def calculate_expectation(game, depth, move, samples=50):
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

def setupGame(r):
    print 'Welcome.'
    tiles = []
    for i in range(7):
        for j in range(i, 7):
            tiles.append((i, j))
    random.shuffle(tiles)
    my_tiles = tiles[:7]
    print 'I have:', my_tiles
    print
    print 'Players are numbered as the following:'
    print '(0 = me, 1 = opponent on my right,'
    print '2 = partner across from me, 3 = opponent on my left)'
    players_tiles = {}
    players_tuples = [None]*4
    players_tiles[0] = set(map(lambda x:Domino(*x), my_tiles))
    players_tuples[0] = my_tiles
    for i in range(1, 4):
        this_players_tiles = tiles[7*i:7*(i+1)]
        print 'Player ' + str(i) + ' has:', this_players_tiles
        players_tiles[i] = set(map(lambda x:Domino(*x), this_players_tiles))
        players_tuples[i] = this_players_tiles
    starter = r % 4
    print "Player " + str(starter) + " is starting."
    print
    return ((Dominoes(tiles, my_tiles, starter),
        Dominoes(tiles, players_tuples[1], (starter-1)%4),
        Dominoes(tiles, players_tuples[2], (starter-2)%4),
        Dominoes(tiles, players_tuples[3], (starter-3)%4)),
        players_tiles)

def computeScore(game, players_tiles):
    player_pips = [0]*4
    # count tiles of each player
    for t in game.my_tiles:
        if t not in game.dominos_played:
            player_pips[0] += sum(t.vals)
    for i in range(1, 4):
        for t in players_tiles[i]:
            if t not in game.dominos_played:
                player_pips[i] += sum(t.vals)

    for i in range(4):
        print 'Player {} has pips {}'.format(i, player_pips[i])
    if (player_pips[0] == 0 or player_pips[2] == 0 or
        player_pips[0]+player_pips[2] < player_pips[1] + player_pips[3]):
        print 'I win!'
        return 'won'
    if (player_pips[1] == 0 or player_pips[3] == 0 or
        player_pips[0]+player_pips[2] > player_pips[1] + player_pips[3]):
        print 'I lose :('
        return 'lost'
    if player_pips[0]+player_pips[2] == player_pips[1] + player_pips[3]:
        print 'we tied?!'
        return 'tie'
    print "SCORES:"
    print "smart + greedy", score_us
    print "greedy + greedy", score_opp
    if score_us < score_opp:
        return "won"
    elif score_opp < score_us:
        return "lost"
    else:
        return "tie"
    for t in game.my_tiles:
        if t not in game.dominos_played:
            score_us += sum(t.vals)
    for i in range(1, 4):
        for t in players_tiles[i]:
            if t not in game.dominos_played:
                if i % 2 == 0:
                    score_us += sum(t.vals)
                else:
                    score_opp += sum(t.vals)
    print 'score is : {}'.format(q)
    return 'won' if q>0 else 'lost'

def get_dominoes_list(game, player, player_tiles):
    if player == 0:
        my_tiles = []
        for t in game.my_tiles:
            if t not in game.dominos_played:
                my_tiles.append(t)
        return my_tiles
    return [t for t in player_tiles[player] if t not in game.dominos_played]
random.seed(100)

if __name__ == '__main__':
    results = []
    for r in range(100):
        print "----PLAYING ROUND---- ", r
        games, players_tiles = setupGame(r)
        while not games[0].is_end():
            player = games[0].curr_player
            tiles = oldSmartPlays(games, players_tiles, player) if player%2==1 else newSmartPlays(games, players_tiles, player)
            print "Player " + str(player) + " just played, ends of tiles " + \
                "are " + str(games[0].ends[0]) + " and " + str(games[0].ends[1])
            print 'Remaining dominoes : {}'.format(sorted(list(players_tiles[player])))
            print
        results.append(computeScore(games[0], players_tiles))
        print "Game ended."
    print "---STATS YAY---"
    print "Number of wins:", results.count("won")
    print "Number of losses:", results.count("lost")
    print "Number of ties:", results.count("tie")
