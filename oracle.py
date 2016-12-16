from domino import Dominoes, Domino
from algorithms.p_negamax import ProbabilisticNegaMax
import random
from copy import deepcopy
import sys
from numpy.random import choice

PASS_STR = 'PASS'
PASS_DOMINO = Domino(-1,-1)

def greedyPlays(game, tiles):
    '''
    @params:
        - game (Dominoes)
    '''
    games = game
    game, ogame = games
    print str(game.curr_player) + "'s turn!"
    player = game.curr_player
    actions = game.possible_actions(None, False)
    my_tiles = tiles[player]
    possible_moves = [PASS_DOMINO]
    for t in my_tiles:
        if t in actions:
            possible_moves.append(t)
    maximum = -1
    ret = possible_moves[0]
    print possible_moves
    for domino in possible_moves:
        if domino.vals[1] + domino.vals[0] > maximum:
            maximum = domino.vals[1] + domino.vals[0]
            ret = domino
    if (game.ends[0] in ret and game.ends[1] in ret and game.ends[0] != game.ends[1]):
        placement = random.choice((0, 1))
        game.update(ret, None, placement)
        ogame.update(ret, None, placement)

    else:
        game.update(ret, None)
        ogame.update(ret, None)
    if ret != PASS_DOMINO:
        tiles[player].remove(ret)
    print "I played a " + str(ret) + ", yay!"
    return tiles

def smartPlays(game, tiles, player):
    player /= 2
    curr_game = game[player]
    other_game = game[1-player]
    actions = curr_game.possible_actions(0)
    if len(actions) == 1:
        curr_game.update(actions[0][0])
        other_game.update(actions[0][0])
        print "I played a " + str(actions[0][0]) + ", yay!"
        if not actions[0][0] == PASS_DOMINO:
            tiles[2*player].remove(actions[0][0])
    else:
        pnm = ProbabilisticNegaMax(curr_game)
        depth = int(8*(2**(1./2*int(len(curr_game.dominos_played)/4))))
        print "DEPTH"
        print depth
        # uncomment out the line below for oldSmartPlayer:
        max_move, max_score = pnm.p_negamax_ab(depth, depth, -float("inf"), float("inf"), 0)

        # max_move, max_score = pnm.p_negamax(6,0)
        curr_game.update(max_move[0], placement=max_move[1])
        other_game.update(max_move[0], placement=max_move[1])
        print "I played a " + str(max_move[0]) + ", yay!"
        if not max_move[0] == PASS_DOMINO:
            tiles[2*player].remove(max_move[0])
    return tiles

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
    return ((Dominoes(tiles, my_tiles, starter), Dominoes(tiles, players_tuples[2], (starter+2)%4)), players_tiles)

def greedyStarts(my_tiles):
    maximum = 0
    for domino in my_tiles:
        if type(domino) == tuple:
            domino = Domino(*domino)
        if domino.vals[1] + domino.vals[0] > maximum:
            maximum = domino.vals[1] + domino.vals[0]
            ret = domino
    return ret

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
random.seed(1234)

def reveal_tiles(games, players_tiles):
    for i in range(4):
        for t in players_tiles[i]:
            games[0].probabilities[t] = [0]*4
            games[0].probabilities[t][i] = 1
            games[1].probabilities[t] = [0]*4
            games[1].probabilities[t][(i+2)%4] = 1

if __name__ == '__main__':
    results = []

    for r in range(100):
        print "----PLAYING ROUND---- ", r
        games, players_tiles = setupGame(r)
        reveal_tiles(games, players_tiles)
        while not games[0].is_end():
            player = games[0].curr_player
            tiles = greedyPlays(games, players_tiles) if player%2==1 else smartPlays(games, players_tiles, player)
            print "Player " + str(player) + " just played, ends of tiles " + \
                "are " + str(games[0].ends[0]) + " and " + str(games[0].ends[1])
            print 'Remaining dominoes : {}'.format(sorted(list(players_tiles[player])))
            print
            print 'PLAYER 0 GAME ------'
            games[0].debugging_fml()
            print 'PLAYER 1 GAME ------'
            games[1].debugging_fml()
        results.append(computeScore(games[0], players_tiles))
        print "Game ended."
    print "---STATS YAY---"
    print "Number of wins:", results.count("won")
    print "Number of losses:", results.count("lost")
    print "Number of ties:", results.count("tie")
