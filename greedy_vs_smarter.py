'''
TODO:
Fix list assignment index out of range
    dominos_played can be of any length!! 
Who won the game? Say it
'''


from domino import Dominoes, Domino
from algorithms.p_negamax import ProbabilisticNegaMax
import random
from copy import deepcopy
import sys

PASS_STR = 'PASS'
PASS_DOMINO = Domino(-1,-1)

def greedyPlays(game, tiles):
    '''
    @params:
        - game (Dominoes)
    '''
    print str(game.curr_player) + "'s turn!"
    player = game.curr_player
    actions = game.possible_actions(None, False)
    my_tiles = tiles[player]
    possible_moves = [PASS_DOMINO]
    for t in my_tiles:
        if t in actions:
            possible_moves.append(t)
    maximum = 0
    ret = possible_moves[0]
    for domino in possible_moves:
        if domino.vals[1] + domino.vals[0] > maximum:
            maximum = domino.vals[1] + domino.vals[0]
            ret = domino
    if (game.ends[0] in ret and game.ends[1] in ret and game.ends[0] != game.ends[1]):
        placement = random.choice((0, 1))
        game.update(ret, None, placement)
    else:
        game.update(ret, None)
    if ret != PASS_DOMINO:
        tiles[player].remove(ret)
    print "I played a " + str(ret) + ", yay!"
    return tiles

def smartPlays(game, tiles):
    actions = game.possible_actions(0)
    if len(actions) == 1:
        game.update(actions[0][0])
        print "I played a " + str(actions[0][0]) + ", yay!"
    else:
        pnm = ProbabilisticNegaMax(game)
        depth = int(5*(2**(1./5*int(len(game.dominos_played)/4))))
        print "DEPTH"
        print depth
        max_move, max_score = pnm.p_negamax_ab(depth, depth, -float("inf"), float("inf"), 0)
        game.update(max_move[0], placement=max_move[1])
        print "I played a " + str(max_move[0]) + ", yay!"
    return tiles

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
    players_tiles[0] = set(map(lambda x:Domino(*x), my_tiles))
    for i in range(1, 4):
        this_players_tiles = tiles[7*i:7*(i+1)]
        print 'Player ' + str(i) + ' has:', this_players_tiles
        players_tiles[i] = set(map(lambda x:Domino(*x), this_players_tiles))
    starter = r % 4
    print "Player " + str(starter) + " is starting."
    if starter > 0:
        start_tile = greedyStarts(players_tiles[starter])
        print "I placed a " + str(start_tile)
        players_tiles[starter].remove(start_tile)
        start_tile = start_tile.vals
    else:
        start_tile = greedyStarts(my_tiles)
        print "I placed a " + str(start_tile)
        start_tile = start_tile.vals
    print
    return (Dominoes(tiles, my_tiles, starter, start_tile), players_tiles)

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
    score_opp = 0
    score_us = 0
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
    print "SCORES:"
    print "smart + greedy", score_us
    print "greedy + greedy", score_opp
    if score_us < score_opp:
        return "won"
    elif score_opp < score_us:
        return "lost"
    else:
        return "tie"

if __name__ == '__main__':
    results = []
    for r in range(1):
        print "----PLAYING ROUND---- ", r
        game, players_tiles = setupGame(r)
        while not game.is_end():
            player = game.curr_player
            tiles = greedyPlays(game, players_tiles) if player > 0 else smartPlays(game, players_tiles)
            print "Player " + str(player) + " just played, ends of tiles " + \
                "are " + str(game.ends[0]) + " and " + str(game.ends[1])
            print
        results.append(computeScore(game, players_tiles))
        print "Game ended."
    print "---STATS YAY---"
    print "Number of wins:", results.count("won")
    print "Number of losses:", results.count("lost")
    print "Number of ties:", results.count("tie")
