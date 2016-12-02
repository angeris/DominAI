from domino import Dominoes, Domino
import random
from algorithms.p_negamax import ProbabilisticNegaMax

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
    while True:
        starter = int(raw_input('Who is starting? '))
        if starter < 4 and starter >= 0:
            break
        else:
            print "Not valid, try again"
    print "Player " + str(starter) + " is starting."
    if starter > 0:
        print 'Write down your move (e.g. 23):'
        move = raw_input("").strip()
        start_tile = tuple([int(v) for v in move])
    else:
        start_tile = greedyStarts(my_tiles)
        print "I placed a " + str(start_tile)
    print
    return Dominoes(tiles, my_tiles, starter, start_tile)

def humanPlays(game, player):
    '''
    @params
        - game (Dominoes)
        - player (int)
    '''
    print 'Now, player ' + str(player) + ' is playing.'
    actions = game.possible_actions(None, False)
    while True:
        try: # lol this is dangerous
            print 'Write down your move (e.g. 23)'
            move = raw_input("").strip()
            if move == PASS_STR:
                game.update(PASS_DOMINO, player)
                print "You just passed."
                return
            move = list(move)
            move = tuple([int(v) for v in move])
        except KeyboardInterrupt:
            raise
        except:
            print "Something went wrong, try again"
        if (game.ends[0] in move and game.ends[1] in move
                and game.ends[0] != game.ends[1]):
            while True:
                print 'Specify placement for ', game.ends
                print '(0 for first end or 1 for second end):'
                placement = int(raw_input("").strip())
                if placement == 0 or placement == 1:
                    print "You played a " + str(move)
                    game.update(move, player, placement)
                    return
        if game.ends[0] in move or game.ends[1] in move:
            if Domino(*move) in actions:
                print "You played a " + str(move)
                game.update(move, player)
                return
        print "Move not valid"

def greedyStarts(my_tiles):
    maximum = 0
    ret = my_tiles[0]
    for domino in my_tiles:
        if domino[1] + domino[0] > maximum:
            maximum = domino[1] + domino[0]
            ret = domino
    return ret

def greedyPlays(game):
    '''
    @params:
        - game (Dominoes)
    '''
    print "My turn! :D"
    possible_moves = game.possible_actions(None, False)   # list of moves
    maximum = 0
    ret = possible_moves[0]
    for domino in possible_moves:
        if domino.vals[1] + domino.vals[0] > maximum:
            maximum = domino.vals[1] + domino.vals[0]
            ret = domino
    if (game.ends[0] in ret and game.ends[1] in ret and game.ends[0] != game.ends[1]):
        placement = random.choice((0, 1))
        game.update(ret, 0, placement)
    else:
        game.update(ret, 0)
    print "I played a " + str(ret) + ", yay!"

def smartPlays(game):
    actions = game.possible_actions(0)
    if len(actions) == 1:
        game.update(actions[0][0])
        print "I played a " + str(actions[0][0]) + ", yay!"
    else:
        pnm = ProbabilisticNegaMax(game)
        max_move, max_score = pnm.p_negamax(5, 0)
        game.update(max_move[0], placement=max_move[1])
        print "I played a " + str(max_move[0]) + ", yay!"

if __name__ == '__main__':
    '''
    Plays one game.
    '''
    game = setupGame()
    while not game.is_end():
        player = game.curr_player
        humanPlays(game, player) if player > 0 else smartPlays(game)
        print "Player " + str(player) + " just played, ends of tiles " + \
            "are " + str(game.ends[0]) + " and " + str(game.ends[1])
        print
        game.debugging_fml()
    print "Game ended."

