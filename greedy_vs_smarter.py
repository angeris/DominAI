'''
TODO:
Fix list assignment index out of range
Who won the game? Say it
'''


from domino import Dominoes, Domino
from algorithms.p_negamax import ProbabilisticNegaMax
import random

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
    print my_tiles
    possible_moves = [PASS_DOMINO]
    print actions
    for t in my_tiles:
        if t in actions:
            print "ADDING"
            print t
            possible_moves.append(t)
    print possible_moves
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
        max_move, max_score = pnm.p_negamax(5, 0)
        game.update(max_move[0], placement=max_move[1])
        print "I played a " + str(max_move[0]) + ", yay!"
    return tiles

def setupGame():
    print 'Welcome.'
    tiles = []
    for i in range(7):
        for j in range(i, 7):
            tiles.append((i, j))
    while True:
        my_tiles_input = raw_input('Enter my tiles (e.g. 45) seperated by spaces: ').split()
        if len(my_tiles_input) == 7:
            break
        else:
            print "I need 7 tiles!"
    my_tiles = []
    for t in my_tiles_input:
        my_tiles.append(tuple([int(num) for num in t]))
    print 'I have:', my_tiles
    print
    print 'Players are numbered as the following:'
    print '(0 = me, 1 = opponent on my right,'
    print '2 = partner across from me, 3 = opponent on my left)'
    players_tiles = {}
    for i in range(1, 4):
        while True:
            my_tiles_input = raw_input('Enter my tiles (e.g. 45) seperated by spaces: ').split()
            if len(my_tiles_input) == 7:
                break
            else:
                print "I need 7 tiles!"
        this_players_tiles = []
        for t in my_tiles_input:
            this_players_tiles.append(tuple([int(num) for num in t]))
        players_tiles[i] = set(map(lambda x:Domino(*x), this_players_tiles))
    while True:
        starter = int(raw_input('Who is starting? '))
        if starter < 4 and starter >= 0:
            break
        else:
            print "Not valid, try again"
    print "Player " + str(starter) + " is starting."
    if starter > 0:
        start_tile = greedyStarts(players_tiles[starter])
        print "I placed a " + str(start_tile)
        players_tiles[starter].remove(start_tile)
        start_tile = start_tile.vals
    else:
        start_tile = greedyStarts(my_tiles)
        print "I placed a " + str(start_tile)
    print
    return (Dominoes(tiles, my_tiles, starter, start_tile), players_tiles)

def greedyStarts(my_tiles):
    maximum = 0
    for domino in my_tiles:
        if domino.vals[1] + domino.vals[0] > maximum:
            maximum = domino.vals[1] + domino.vals[0]
            ret = domino
    return ret

if __name__ == '__main__':
    game, players_tiles = setupGame()
    while not game.is_end():
        player = game.curr_player
        tiles = greedyPlays(game, players_tiles) if player > 0 else smartPlays(game, players_tiles)
        print "Player " + str(player) + " just played, ends of tiles " + \
            "are " + str(game.ends[0]) + " and " + str(game.ends[1])
        print
        game.debugging_fml()
    print "Game ended."